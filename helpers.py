def format_album_artists(l):
	outp = ""
	for el in l[:-1]:
		outp += "%s & " % el
	outp += l[-1]

	return outp

def rdpprep(rdp):
	if rdp == "day":
		return "on"
	elif rdp == "year":
		return "in"
	else:
		return "in"