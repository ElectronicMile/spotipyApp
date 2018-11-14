def format_album_artists(l):
	outp = ""
	for el in l[:-1]:
		outp += "%s & " % el
	outp += l[-1]

	return outp