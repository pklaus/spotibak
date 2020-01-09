#!/usr/bin/env python

import spotipy
import spotipy.util as util
import attr

import os
import sys
import pprint
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--user', required=True)
parser.add_argument('--output_folder', default='.')
args = parser.parse_args()

REQ_ENV_VARS = ('SPOTIPY_CLIENT_ID', 'SPOTIPY_CLIENT_SECRET', 'SPOTIPY_REDIRECT_URI')
if not all(env in os.environ for env in REQ_ENV_VARS):
    parser.error('Please set all required environment variables:\n' +
                 '\n'.join(REQ_ENV_VARS))

ALL_SCOPES = [
    'ugc-image-upload',
    'user-read-playback-state',
    'user-modify-playback-state',
    'user-read-currently-playing',
    'streaming',
    'app-remote-control',
    'user-read-email',
    'user-read-private',
    'playlist-read-collaborative',
    'playlist-modify-public',
    'playlist-read-private',
    'playlist-modify-private',
    'user-library-modify',
    'user-library-read',
    'user-top-read',
    'user-read-recently-played',
    'user-follow-read',
    'user-follow-modify',
]

print("### CONNECTING")

token = util.prompt_for_user_token(args.user, ' '.join(ALL_SCOPES))
sp = spotipy.Spotify(auth=token)

LIMIT = 50

@attr.s
class Task(object):
    name = attr.ib()
    fetch = attr.ib()
    extract_items = attr.ib(default=lambda x: x['items'])
    next_items = attr.ib(default=lambda x: x)
    cleaner = attr.ib(default=None)
    subtask = attr.ib(default=None)

def tracks_cleaner(track_list):
    for track in track_list:
        try:
            del track['track']['available_markets']
            del track['track']['album']
        except:
            print("strange track:")
            pprint.pprint(track)

def playlists_cleaner(playlist_list):
    for playlist in playlist_list:
        tracks_cleaner(playlist['all_tracks'])

def playlist_tracks(playlist):
    tracks = []
    result = sp.user_playlist(playlist['owner']['id'], playlist['id'], fields="tracks,next")
    tracks = result['tracks']
    tracks = result['tracks']
    playlist_tracks = tracks['items']
    print(f" ⮡ adding tracks to playlist \"{playlist['name']}\"   .", end='')
    while tracks['next']:
        print('.', end='')
        sys.stdout.flush()
        tracks = sp.next(tracks)
        playlist_tracks += tracks['items']
    print()
    playlist['all_tracks'] = playlist_tracks

def fetch_artists(limit=20, offset=0):
    """ dummy function as 'followed artists' doesn't offer offset """
    return sp.current_user_followed_artists(limit=limit)

print("### TASK SETUP")

TASKS = [
    Task('tracks', sp.current_user_saved_tracks, cleaner=tracks_cleaner),
    Task('playlists', sp.current_user_playlists, cleaner=playlists_cleaner, subtask=playlist_tracks),
    Task('albums', sp.current_user_saved_albums),
    Task('artists', fetch_artists, extract_items=lambda x: x['artists']['items'], next_items=lambda x: x['artists']),
]

print("### FETCHING")

DATA = {}

for task in TASKS:
    print(f"Fetching {task.name} .", end='')
    result = task.fetch(limit=LIMIT, offset=0)
    items = task.extract_items(result)
    while task.next_items(result)['next']:
        result = sp.next(task.next_items(result))
        print('.', end='')
        sys.stdout.flush()
        items += task.extract_items(result)
    print('')
    if task.subtask:
        for item in items:
            task.subtask(item)
    DATA[task.name] = items

print("### EXPORTING 1/2")

with open(os.path.join(args.output_folder, f"{args.user}_spotify-data.raw.json"), "w") as f:
    json.dump(DATA, f)

print("### CLEANING")

for task in TASKS:
    if not task.cleaner:
        continue
    try:
        task.cleaner(DATA[task.name])
    except Exception as e:
        print("Couln't apply cleaner", task.cleaner)
        print(e)

print("### EXPORTING 2/2")

with open(os.path.join(args.output_folder, f"{args.user}_spotify-data.clean.json"), "w") as f:
    json.dump(DATA, f)
