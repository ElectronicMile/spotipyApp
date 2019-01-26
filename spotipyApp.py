#!/usr/bin/env python3

import spotipy
import spotipy.util as util
import logging
import argparse
import sys
#from spotipyGUI import *

logging.basicConfig(level=logging.INFO)


def login():
	print(sys.argv[0])
	scope = 'user-modify-playback-state user-library-read'

	username = "1136425634"

	token = util.prompt_for_user_token(username, scope)
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
	urlplay = 'https://api.spotify.com/v1/me/player/play'
	sp._internal_call('PUT', urlplay, payload, params)
	#rungui(sp)
except spotipy.SpotifyException:
	logging.error("Could not log in. Check user data.")
	sys.exit(0)

