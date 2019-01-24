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

def search(self):
	for w in currentWidgets:
		w.destroy()
	album_uri = txt.get()
	#album_uri = "spotify:album:07RagZtMuBbLBnaWJbD52h"
	try:
		results = sp.album(album_id=album_uri)
		logging.info("Showing info for following album:\n%s" % results)
		currentWidgets = showresults(resultframe, results)
	except spotipy.SpotifyException:
		errorText.pack()

def search2(self, Event):
	search()

def selectall(self, Event):
	print('event.widget.get():', Event.widget.get())

	# select text
	Event.widget.select_range(0, 'end')
	# move cursor to the end
	Event.widget.icursor('end')
