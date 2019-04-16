from spotipyApp import login


print ('Why is nothing being printed here?')

try:
	sp = login()
	urlplayer = 'https://api.spotify.com/v1/me/player'
	params = {'country': None, 'album_type': None, 'limit': 20, 'offset': 0}
	payload = None
	currplaying = sp._internal_call('GET', urlplayer, payload, params)
	print('done')

except spotipy.SpotifyException:
	logging.error("Could not log in. Check user data.")
	sys.exit(0)
