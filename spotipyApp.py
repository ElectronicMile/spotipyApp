import spotipy
import spotipy.util as util
import logging
import argparse
import sys
from spotipyGUI import *

logging.basicConfig(level=logging.INFO)

"""parser = argparse.ArgumentParser(description="Input mode: artist, playlist, etc.")
parser.add_argument("-s", "--source", help="The source from which you want to take album covers. Options are 'artist' and 'playlist'",
					required=True)
parser.add_argument("-u", "--uri", help="The URI of the artist or playlist for which you want to collect the album covers",
					required=True)
args = parser.parse_args()

if args.source != "artist" and args.source != "playlist":
	logging.error("Not a valid input source. Choose 'artist' or 'playlist'.")
	sys.exit(0)

source = args.source
uri = args.uri

if source not in uri:
	logging.error("URI does not match source: needs to be an artist or a playlist.")
	sys.exit(0)
"""

def login():
	client_id = "580cb72fd1364d10aa8bd0f8d4bf5c32"
	client_secret = "fa391051c65748b7b7b35d7d6d4faa93"
	redirect_uri = "https://www.google.be/"
	scope = 'user-modify-playback-state user-library-read'

	username = "1136425634"

	token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
	if token:
		sp = spotipy.Spotify(auth=token)
	else:
		logging.ERROR("Cannot login with this user account")
		sys.exit(0)

	return sp

params = {'country': None, 'album_type': None, 'limit': 20, 'offset': 0}
payload = None
urlcurr = 'https://api.spotify.com/v1/me/player'
urlpause = 'https://api.spotify.com/v1/me/player/pause'
urlplay = 'https://api.spotify.com/v1/me/player/play'

# currentlyplaying = sp._internal_call('GET', urlcurr, payload, params)
# print currentlyplaying

try:
	sp = login()
	rungui(sp)
except spotipy.SpotifyException:
	logging.error("Could not log in. Check user data.")
	sys.exit(0)

