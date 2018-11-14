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

	albumname = results["name"]
	releasedate = results["release_date"]
	albumartists = []
	for art in results["artists"]:
		name = art["name"]
		albumartists.append(name)

	currAlbumWidgets = []

	lbl = Label(window, text="Album \"%s\" by %s, released on %s. Tracks are:" % (albumname, format_album_artists(albumartists), releasedate))
	lbl.configure(bg="grey")
	lbl.grid(column=0, row=4)
	currAlbumWidgets.append(lbl)

	tracks = []
	id = 0
	for tr in results['tracks']["items"]:
		tracks.append(tr["name"])
		id += 1
		label = Label(window, text="%d: %s" %(id, tr["name"]))
		label.configure(bg="grey")
		label.grid(sticky=W, column=0, row=id + 4)
		currAlbumWidgets.append(label)

	coverurl = results["images"][0]["url"]
	logging.info("URL is %s" % coverurl)
	raw_data = urllib.urlopen(coverurl).read()
	im = imImage.open(io.BytesIO(raw_data))
	im = im.resize((350, 350), imImage.ANTIALIAS)
	image = ImageTk.PhotoImage(im)
	imageLabel = Label(window, image=image)
	imageLabel.image = image
	imageLabel.grid(column=0, row=id+5)
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

		master.configure(background="grey")

		master.title("Spotipy GUI")
		master.geometry("800x800")

		self.queryframe = LabelFrame(master, text="Query", borderwidth=3, padx=5, pady=5, relief=GROOVE, bg="green")
		self.queryframe.grid(row=0, column=0, sticky=E + W + N + S)

		self.resultframe = LabelFrame(master, text="Query", borderwidth=3, padx=5, pady=5, relief=GROOVE, bg="green")
		self.resultframe.grid(row=0, column=1, sticky=E + W + N + S)

		welcome = Label(self.queryframe, text="Welcome.")
		welcome.grid(sticky=W, column=0, row=0)

		lbl = Label(self.queryframe, text="Enter an album URI:")
		lbl.grid(sticky=W, column=0, row=1)

		txt = Entry(self.queryframe, width=30)
		txt.grid(sticky=W, column=0, row=2)
		txt.focus()
		self.txt = txt

		btn = Button(self.queryframe, text="Enter", command=self.search)
		btn.configure(background="grey")
		btn.grid(sticky=W, column=0, row=3)
		self.queryframe.bind('<Return>', self.search2)


	def search(self):
		for w in self.currentWidgets:
			w.destroy()
		album_uri = self.txt.get()
		#album_uri = "spotify:album:3NnGeD4rLyOOzmlsb2ZLfO"
		if album_uri != "":
			results = self.sp.album(album_id=album_uri)
			logging.info("Showing info for following album:\n%s" % results)
			self.currentWidgets = showresults(self.resultframe, results)
		else:
			testText = Label(self.resultframe, text="Test layout")
			testText.pack()

	def search2(self, Event):
		self.search()

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	window = Tk()
	spotipyApp = App(window)
	window.mainloop()

