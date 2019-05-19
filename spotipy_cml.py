from spotipyApp import login
import spotipy, sys, logging
# from gtts import gTTS

def process_context(curr, sp):

	context_is_type = True
	print(curr)
	try:
		type = curr["context"]["type"]
		uri = curr["context"]["uri"]
		if not curr["is_playing"]:
			return "Currently paused"
	except TypeError:
		context_is_type = False

	track = curr["item"]["name"]
	artist = curr["item"]["artists"][0]["name"]
	device = curr["device"]["name"]

	if type == "artist":
		contextname = sp.artist(uri)["name"]
	elif type == "album":
		contextname = sp.album(uri)["name"]
	elif type == "playlist":
		pl = uri.split(":")
		contextname = sp.user_playlist(pl[2],pl[4], "name")["name"]

	if context_is_type:
		out =  "The context is of type %s: '%s'. Currently the track '%s' by '%s' is playing on %s." % (type, contextname, track, artist, device)
	else:
		out = "There is no context, you are listening to your library. Currently the track %s by %s is playing on %s." % (type, track, artist, device)

	return out

if __name__ == '__main__':
	try:
		sp = login()

	except spotipy.SpotifyException:
		logging.error("Could not log in. Check user data.")
		sys.exit(0)

	try:
		urlplayer = 'https://api.spotify.com/v1/me/player'
		params = {'country': None, 'album_type': None, 'limit': 20, 'offset': 0}
		payload = None
		curr = sp._internal_call('GET', urlplayer, payload, params)
		if not curr:
			logging.info("Currently not playing anything on Spotify.")
		else:
			logging.info(process_context(curr, sp))
	except spotipy.SpotifyException:
		logging.error('Something went wrong. Cancelling.')
		sys.exit(0)