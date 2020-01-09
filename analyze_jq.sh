#!/bin/bash

cat *_spotify-data.clean.json | jq '.playlists[] | {name: .name}' | less

cat *_spotify-data.clean.json | jq '.artists[] | {name: .name, genres: .genres}' | less
