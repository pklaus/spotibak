## SpotiBak

This is a Python Software to backup your spotify data.
Currently this includes **tracks** and **albums** that you added
to your library, **playlists** that you created or saved (incl.
all tracks they contain each) as well as **artists** that you follow.

### Installation

You need Python3.7+ and install the requirements with pip:

```bash
pip install spotipy attrs addict
```

### Setting Up

To access your Spotify data, we use [spotipy][], a Python package.
It makes use of [Spotify's Web API][]. In order to use it, you need
to get a client ID and client secret from Spotify on their
[Developer Dashboard][] by registering a new application.
Also set the redirect URI associated with that application
to `http://localhost` on their page.

You need the information later when running the script.

### Usage

The CLI of the tool has the following signature:

```
$ python3 ./spotibak.py --help
usage: spotibak.py [-h] --user USER [--output_folder OUTPUT_FOLDER]

optional arguments:
  -h, --help            show this help message and exit
  --user USER
  --output_folder OUTPUT_FOLDER
```

Set some environment variables according to the setup stage above:

```bash
export SPOTIPY_CLIENT_ID='58346006acf84dc68f327323d80e9161'
export SPOTIPY_CLIENT_SECRET='a2270e0397874a34904803ba316134b1'
export SPOTIPY_REDIRECT_URI='http://localhost'
```

Now you're ready to run the backup script:

```bash
./spotibak.py --user your.user.name
```

This leaves you with two files:

```
ls -l

-rw-r--r-- 18087115 your.user.name_spotify-data.clean.json
-rw-r--r-- 38616375 your.user.name_spotify-data.raw.json
```

### Analyzing the Backup

A simple python script to analyze the output json file is also part
of this repository:

```
$ ./analyze.py --help
usage: analyze.py [-h] [--print-tracks] [--print-albums] [--print-playlists]
                  [--print-artists]
                  infile

positional arguments:
  infile

optional arguments:
  -h, --help            show this help message and exit
  --print-tracks, -t
  --print-albums, -a
  --print-playlists, -p
  --print-artists, -r
```

[Spotify's Web API]: https://developer.spotify.com/documentation/web-api
[spotipy]: https://spotipy.readthedocs.io/en/latest/
[Developer Dashboard]: https://developer.spotify.com/dashboard/
