#!/usr/bin/env python3

import spotipy
import spotipy.util as util
import logging
import io
import urllib
from PIL import ImageTk
from PIL import Image as imImage
from Tkinter import *
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
	raw_data = urllib.urlopen(res.coverurl).read()
	im = imImage.open(io.BytesIO(raw_data))
	im = im.resize((350, 350), imImage.ANTIALIAS)
	image = ImageTk.PhotoImage(im)
	imageLabel = Label(window, image=image)
	imageLabel.image = image
	imageLabel.grid(column=0, row=id + 5)
	currAlbumWidgets.append(imageLabel)

	return currAlbumWidgets

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

		playbtn = Button(self.controlframe, text="pause", command=self.pause, bg=self.bgcolor)
		playbtn.grid(sticky=W, column=1, row=1)

		self.master.bind('<Return>', self.search2)
		self.master.bind('<Command-a>', self.selectall)
		#self.master.bind('<Control-a>', self.selectall) Will work for Windows?


	# control commands: search, play, etc.

	def search(self):
		for w in self.currentWidgets:
			w.destroy()
		album_uri = self.txt.get()
		#album_uri = "spotify:album:07RagZtMuBbLBnaWJbD52h"
		try:
			if album_uri != "spotify:track:4wupMhFWAQzP8CGROC1D2r":
				results = self.sp.album(album_id=album_uri)
				logging.info("Showing info for following album:\n%s" % results)
				self.currentWidgets = showresults(self.resultframe, results)
			else:
				results = self.sp.audio_features(tracks=["spotify:track:4wupMhFWAQzP8CGROC1D2r"])
				#results = self.sp.audio_analysis(track_id="spotify:track:4wupMhFWAQzP8CGROC1D2r")
				logging.INFO(results)
		except spotipy.SpotifyException:
			self.errorText.pack()

	def play(self):
		params = {'country': None, 'album_type': None, 'limit': 20, 'offset': 0}
		payload = None
		urlcurr = 'https://api.spotify.com/v1/me/player'
		urlpause = 'https://api.spotify.com/v1/me/player/pause'
		urlplay = 'https://api.spotify.com/v1/me/player/play'
		self.sp._internal_call('PUT', urlplay, payload, params)

	def pause(self):
		params = {'country': None, 'album_type': None, 'limit': 20, 'offset': 0}
		payload = None
		urlpause = 'https://api.spotify.com/v1/me/player/pause'
		self.sp._internal_call('PUT', urlpause, payload, params)

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