import sys, re
import logging
import spotipy
import spotipy.util as util
from Tkinter import *

"""
User ID = 1136425634
"""


class App:

	def __init__(self, master):
		self.scope = 'user-library-read'
		self.client_id = "580cb72fd1364d10aa8bd0f8d4bf5c32"
		self.client_secret = "fa391051c65748b7b7b35d7d6d4faa93"
		self.redirect_uri = "https://www.google.be/"

		self.username = ""

		self.UIelements = {}

		self.master = master

		master.title("Spotipy GUI")
		master.geometry("500x200")

		welcome = Label(master, text="Welcome.")
		welcome.grid(column=0, row=0)

		lbl = Label(master, text="Enter your username:")
		lbl.grid(column=0, row=2)

		txt = Entry(master, width=10)
		txt.grid(column=1, row=2)
		self.UIelements["usernameEntry"] = txt

		btn = Button(master, text="Enter", command=lambda: self.login(txt))
		btn.grid(column=2, row=2)
		self.UIelements["usernameButton"] = btn

		artistEntry = Entry(master, width=25)
		artistEntry.bind("<Return>", self.search)
		self.UIelements["artistEntry"] = artistEntry
		artistLbl = Label(master, text="Artist")
		self.UIelements["artistLabel"] = artistLbl

		albumEntry = Entry(master, width=25)
		albumEntry.bind("<Return>", self.search)
		self.UIelements["albumEntry"] = albumEntry
		albumLbl = Label(master, text="Album")
		self.UIelements["albumLabel"] = albumLbl

		searchBtn = Button(master, text="Search", state="disabled", command=self.search)
		self.UIelements["searchButton"] = searchBtn

		#searchRes = Text(master)
		#self.UIelements

	def preparequeryGUI(self):
		self.UIelements["usernameButton"].config(state="disabled")
		self.UIelements["usernameEntry"].config(state="disabled")
		self.UIelements["artistEntry"].config(state="normal")
		self.UIelements["artistEntry"].grid(column=1, row=3)
		self.UIelements["artistEntry"].focus()
		self.UIelements["artistLabel"].grid(column=0, row=3)
		self.UIelements["albumEntry"].config(state="normal")
		self.UIelements["albumEntry"].grid(column=1, row=4)
		self.UIelements["albumLabel"].grid(column=0, row=4)
		self.UIelements["searchButton"].config(state="normal")
		self.UIelements["searchButton"].grid(column=2,row=4)


	def makespotipyobj(self):
		token = util.prompt_for_user_token(self.username, self.scope, client_id=self.client_id,
										   client_secret=self.client_secret,
										   redirect_uri=self.redirect_uri)
		if token:
			self.sp = spotipy.Spotify(auth=token)
			self.preparequeryGUI()


	def login(self, txt):
		self.username = txt.get()
		if self.username == "":
			self.username = "1136425634"
		if re.search("\d+", self.username):
			logging.info("Logging in with %s" % self.username)
			self.makespotipyobj()

	def displayResults(self, dict):
		alb = dict["album"]["name"]
		#artist = dict["album"]["tracks"]["items"][0]["artists"][0]["name"]
		result = "The first match in your library is the album %s by %s" % alb#(alb, artist)
		searchRes = Text(self.master)
		searchRes.insert(END, result)
		searchRes.grid(column=1, row=5)


	def search(self):
		album = self.UIelements["albumEntry"].get()
		artist = self.UIelements["artistEntry"].get()
		albums = self.sp.current_user_saved_albums(limit=200)
		logging.info("Looking for %s" % album)
		for alb in albums["items"]:
			print alb["album"]
			if album in alb["album"]["name"]:# and artist in alb["album"]["tracks"]["items"][0]["artists"][0]["name"]:
				print "found sth"
				self.displayResults(alb)
				break


if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	window = Tk()
	spotipyApp = App(window)
	window.mainloop()

