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

	def __init__(self, master):
		self.client_id = "580cb72fd1364d10aa8bd0f8d4bf5c32"
		self.client_secret = "fa391051c65748b7b7b35d7d6d4faa93"
		self.redirect_uri = "https://www.google.be/"
		self.scope = 'user-library-read'

		self.username = "1136425634"

		token = util.prompt_for_user_token(self.username, self.scope, client_id=self.client_id,
										   client_secret=self.client_secret,
										   redirect_uri=self.redirect_uri)
		if token:
			self.sp = spotipy.Spotify(auth=token)
		else:
			logging.ERROR("Cannot login with this user account")
			sys.exit(0)

		self.master = master

		self.currentWidgets = []
		self.bgcolor = "#2ECC71"

		master.configure(background=self.bgcolor)

		master.title("Spotipy GUI")
		master.geometry("800x800")

		self.queryframe = LabelFrame(master, text="Query", borderwidth=3, padx=5, pady=5, relief=GROOVE, bg=self.bgcolor)
		self.queryframe.grid(row=0, column=0, sticky=E + W + N + S)

		self.resultframe = LabelFrame(master, text="Result", borderwidth=3, padx=5, pady=5, relief=GROOVE, bg=self.bgcolor)
		self.resultframe.grid(row=1, column=0, sticky=E + W + N + S)

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


		self.master.bind('<Return>', self.search2)
		self.master.bind('<Command-a>', self.selectall)
		#self.master.bind('<Control-a>', self.selectall) Will work for Windows?


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

	def search2(self, Event):
		self.search()

	def selectall(self, Event):
		print('event.widget.get():', Event.widget.get())

		# select text
		Event.widget.select_range(0, 'end')
		# move cursor to the end
		Event.widget.icursor('end')

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	window = Tk()
	spotipyApp = App(window)
	window.mainloop()

