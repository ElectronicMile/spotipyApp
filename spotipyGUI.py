#!/usr/bin/env python3

import spotipy
import logging
import requests
from PIL import Image as imImage
from io import BytesIO
from tkinter import *
from helpers import *


def showresults(window, results):

	res = QueryResult(results)
	currAlbumWidgets = []

	lbl = Label(window, text=res.parseInfo())
	lbl.configure(bg="grey")
	lbl.grid(column=0, row=4)
	currAlbumWidgets.append(lbl)

	id = 0
	for name in res.tracks["name"]:
		id += 1
		lbltext = "%d: %s" % (id, name)
		label = Label(window, text=lbltext)
		label.configure(bg="grey")
		label.grid(sticky=W, column=0, row=id + 4)
		currAlbumWidgets.append(label)

	logging.info("URL is %s" % res.coverurl)
	raw_data = requests.get(res.coverurl)
	im = imImage.open(BytesIO(raw_data.content))
	image = PhotoImage(im)
	imageLabel = Label(window, image=image)
	imageLabel.image = image
	imageLabel.grid(column=0, row=id + 5)
	currAlbumWidgets.append(imageLabel)

	return currAlbumWidgets

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
		contextname = sp.user_playlist(user=sp.user, playlist_id=uri)["name"]

	if context_is_type:
		out =  "The context is of type %s: '%s'. Currently the track '%s' by '%s' is playing on %s." % (type, contextname, track, artist, device)
	else:
		out = "There is no context, you are listening to your library. Currently the track %s by %s is playing on %s." % (type, track, artist, device)

	return out


class App:

	def __init__(self, master, sp):


		self.master = master
		self.sp = sp

		self.currentWidgets = []
		self.bgcolor = "#2ECC71"

		master.configure(background=self.bgcolor)

		master.title("Spotipy GUI")
		master.geometry("800x800")

		self.queryframe = LabelFrame(master, text="Query", borderwidth=3, padx=5, pady=5, relief=GROOVE, bg=self.bgcolor)
		self.queryframe.grid(row=0, column=0, sticky=E + W + N + S)

		self.resultframe = LabelFrame(master, text="Result", borderwidth=3, padx=5, pady=5, relief=GROOVE, bg=self.bgcolor)
		self.resultframe.grid(row=1, column=0, sticky=E + W + N + S)

		self.controlframe = LabelFrame(master, text="Play", borderwidth=1, padx=5, pady=5, relief=GROOVE, bg=self.bgcolor)
		self.controlframe.grid(row=0, column=1, sticky=E + N)

		self.nowplayingframe = LabelFrame(master, text="Now playing", borderwidth=1, padx=5, pady=5, relief=GROOVE, bg=self.bgcolor)
		self.nowplayingframe.grid(row=0, column=2, sticky=E + W + N + S)

		welcome = Label(self.queryframe, text="Welcome.", bg=self.bgcolor)
		welcome.grid(sticky=W, column=0, row=0)

		lbl = Label(self.queryframe, text="Enter an album URI:", bg=self.bgcolor)
		lbl.grid(sticky=W, column=0, row=1)

		txt = Entry(self.queryframe, width=30, bg="#229954")
		txt.grid(sticky=W, column=0, row=2)
		txt.focus()
		self.txt = txt

		btn = Button(self.queryframe, text="Enter", command=self.search, bg=self.bgcolor)
		btn.configure(background="grey")
		btn.grid(sticky=W, column=0, row=3)

		self.errorText = Label(self.resultframe, text="Invalid URI", bg=self.bgcolor)

		playbtn = Button(self.controlframe, text="play", command=self.play, bg=self.bgcolor)
		playbtn.grid(sticky=W, column=0, row=1)

		pausebtn = Button(self.controlframe, text="pause", command=self.pause, bg=self.bgcolor)
		pausebtn.grid(sticky=W, column=1, row=1)

		nextbtn = Button(self.controlframe, text="next", command=self.nexttrack, bg=self.bgcolor)
		nextbtn.grid(sticky=W, column=1, row=2)

		prevbtn = Button(self.controlframe, text="prev", command=self.prevtrack, bg=self.bgcolor)
		prevbtn.grid(sticky=W, column=0, row=2)

		nowplaying = Button(self.controlframe, text="Now playing", command=self.nowplaying, bg=self.bgcolor)
		nowplaying.grid(sticky=W,column=2,row=2)

		self.master.bind('<Return>', self.search2)
		self.master.bind('<Command-a>', self.selectall)
		#self.master.bind('<Control-a>', self.selectall) Will work for Windows?


	# variables for playback control
	controlparams = {'country': None, 'album_type': None, 'limit': 20, 'offset': 0}
	controlpayload = None
	controlurl = 'https://api.spotify.com/v1/me/player/%s'

	# control commands: search, play, etc.

	def search(self):
		for w in self.currentWidgets:
			w.destroy()
		album_uri = self.txt.get()
		#album_uri = "spotify:album:07RagZtMuBbLBnaWJbD52h"
		try:
			results = self.sp.album(album_id=album_uri)
			logging.info("Showing info for following album:\n%s" % results)
			self.currentWidgets = showresults(self.resultframe, results)
		except spotipy.SpotifyException:
			self.errorText.pack()

	def play(self):
		self.sp._internal_call('PUT', self.controlurl % "play", self.controlpayload, self.controlparams)

	def pause(self):
		self.sp._internal_call('PUT', self.controlurl % "pause", self.controlpayload, self.controlparams)

	def nexttrack(self):
		self.sp._internal_call('POST', self.controlurl % "next", self.controlpayload, self.controlparams)

	def prevtrack(self):
		self.sp._internal_call('POST', self.controlurl % "previous", self.controlpayload, self.controlparams)

	def nowplaying(self):
		urlplayer = 'https://api.spotify.com/v1/me/player'
		params = {'country': None, 'album_type': None, 'limit': 20, 'offset': 0}
		payload = None
		curr = self.sp._internal_call('GET', urlplayer, payload, params)
		if not curr:
			logging.info("Currently not playing anything on Spotify.")
		else:
			logging.info(process_context(curr, self.sp))

	# commands for keyboard shortcuts

	def search2(self, Event):
		self.search()

	def selectall(self, Event):
		# select text
		Event.widget.select_range(0, 'end')
		# move cursor to the end
		Event.widget.icursor('end')

def rungui(sp):
	logging.basicConfig(level=logging.INFO)
	window = Tk()
	spotipyApp = App(window, sp)
	window.mainloop()

#spotify:album:7lOKvvK9dCayXwR7925yk4