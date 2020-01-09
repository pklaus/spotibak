#!/usr/bin/env python

import argparse
import json
import addict

parser = argparse.ArgumentParser()
parser.add_argument('--print-tracks', '-t', action='store_true')
parser.add_argument('--print-albums', '-a', action='store_true')
parser.add_argument('--print-playlists', '-p', action='store_true')
parser.add_argument('--print-artists', '-r', action='store_true')
parser.add_argument('infile')
args = parser.parse_args()

with open(args.infile, 'r') as f:
    d = json.load(f)

d = addict.Dict(d)

if args.print_tracks:
    for track in d.tracks:
        print(track.track.artists[0].name, " - ", end='')
        print(track.track.name)
        print()

if args.print_albums:
    for album in d.albums:
        print(album.album.name)

if args.print_playlists:
    for playlist in d.playlists:
        print(playlist.name)
        print("Number of tracks:", len(playlist.all_tracks))
        print()

if args.print_artists:
    for artist in d.artists:
        print(artist.name)
