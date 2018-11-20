import re
from collections import defaultdict

class QueryResult:

	def __init__(self, json):
		self.albumname = json["name"]
		self.releasedate = json["release_date"]
		self.rdp = json["release_date_precision"]
		self.albumartists = []
		for art in json["artists"]:
			name = art["name"]
			self.albumartists.append(name)
		self.tracks = defaultdict(list)
		for tr in json["tracks"]["items"]:
			self.tracks["id"].append(tr["track_number"])
			self.tracks["name"].append(tr["name"])

		self.coverurl = json["images"][0]["url"]

	def rdpformat(self):
		if self.rdp == "day":
			return "on"
		elif self.rdp == "year":
			return "in"
		else:
			return "in"

	def parseInfo(self):
		albartoutp = ""
		for el in self.albumartists[:-1]:
			albartoutp += "%s & " % el
		albartoutp += self.albumartists[-1]
		rdpprep = self.rdpformat()

		finaloutp = "Album \"%s\" by %s, released %s %s.\nTracks are:" % (self.albumname, albartoutp, rdpprep, self.releasedate)
		return finaloutp



def formattracks(name):
	featartout = ""
	nameout = ""
	feature = re.compile(r"(.*)(\(feat[^)]+\))$")
	featart = re.compile(r"feat(uring)?.? ?(.*)\)$")
	if re.search(feature, name):
		nameout = re.sub(feature, r"\1", name)
		if re.search(featart, name):
			featartout = re.search(featart, name).group(2)

	return nameout, featartout
