import urllib2

class UrlResource(object):

	def __init__(self, url):
		self._url = url

	def __str__(self):
		return urllib2.urlopen(self._url).read()