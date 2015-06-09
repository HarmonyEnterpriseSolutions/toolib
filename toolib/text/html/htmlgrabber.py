#-*- coding: cp1251 -*-
import logging
import os
import pickle
import sys
import time
import urllib2
import zlib
import traceback
from cStringIO import StringIO
from BeautifulSoup import BeautifulSoup, NavigableString, Tag
from soupselect import select
from urlparse import urlparse, urlunparse
from unhtml import resolve_char_entities, remove_whitespace
from urllib2 import HTTPError


logger = logging.getLogger('toolib.text.html.htmlgrabber')


class PickledDict(object):

	def __init__(self, filename):
		super(PickledDict, self).__init__()
		self.filename = filename
		if os.path.exists(filename):
			self.data = pickle.load(open(filename, 'rb'))
		else:
			self.data = {}
		self.changes = False

	def save(self):
		if self.changes:
			pickle.dump(self.data, open(self.filename, 'wb'), protocol=2)

	def get(self, name):
		return self.data.get(name)

	def __setitem__(self, key, value):
		self.data.__setitem__(key, value)
		self.changes = True

	#def __del__(self):
	#	if hasattr(self, 'data'):
	#		self.save()


class PretendFirefoxOpener(object):

	def __init__(self, opener=None):
		self.opener = opener or DefaultOpener()
		self.opener.addheaders = [
			('User-Agent',       'Mozilla/5.0 (Windows NT 5.1; rv:22.0) Gecko/20100101 Firefox/22.0'),
			('Accept:',          'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
			('Accept-Language:', 'en-gb,en;q=0.5'),
			('Accept-Encoding:', 'gzip, deflate'),
			('Connection:',      'keep-alive'),
		]

	def open(self, url, **kwargs):
		logger.debug("GET " + url)
		return self.opener.open(urllib2.Request(url, **kwargs))


class CachedOpener(object):

	def __init__(self, opener=None, cache=None):
		self.opener = opener or urllib2.build_opener()
		self.cache = cache or {}

	def open(self, url, **kwargs):
		zdata = self.cache.get(url)
		if zdata is None:
			data = self.opener.open(url, **kwargs).read()
			self.cache[url] = zlib.compress(data)
		else:
			data = zlib.decompress(zdata)
		return StringIO(data)

class RetryOpener(object):

	def __init__(self, opener, retry_count=3, delay=500):
		self.opener = opener
		self._retry_count = retry_count
		self._delay = delay / 1000.

	def open(self, url, *args, **kwargs):
		exc = None	
		delay = self._delay

		for i in range(self._retry_count):
			try:
				return SafeResponse(self.opener.open(url, *args, **kwargs))
			except HTTPError, e:
				logger.warning("error opening %s: %s: %s, retrying..." % (url, e.__class__.__name__, e))
				time.sleep(delay)
				delay *= 2
				exc = sys.exc_info()
		
		if exc:
			raise exc[0], exc[1], exc[2]

class DefaultOpener(object):
	
	def open(self, *args, **kwargs):
		return urllib2.urlopen(*args, **kwargs)


class SafeResponse(object):
	"""
	all data read in constructor
	"""

	def __init__(self, response):
		self.__response = response
		self.__io = StringIO(response.read())

	def read(self, *args, **kwargs):
		return self.__io.read(*args, **kwargs)

	def readline(self):
		return self.__io.readline()

	def readlines(self):
		return self.__io.readlines()

	def __getattr__(self, name):
		return getattr(self.__response, name)
		

class Match(object):

	def __init__(self, element):
		assert not isinstance(element, Match)
		self.element = element

	def __unicode__(self):
		return unicode(self.element)

	def __str__(self):
		return unicode(self).encode(sys.stdout.encoding or 'UTF-8', 'replace')

	def attr(self, name):
		if not hasattr(self, '_attrs'):
			self._attrs = dict(self.element.attrs)
		return self._attrs[name]

	def find(self, *args, **kwargs):
		return Match(self.element.find(*args, **kwargs))

	def findAll(self, *args, **kwargs):
		return map(Match, self.element.findAll(*args, **kwargs))

	def text(self):
		return resolve_char_entities(self.element.text)

	def plain_text(self):
		result = []
		for element in self.element:
			if isinstance(element, NavigableString):
				result.append(resolve_char_entities(remove_whitespace(unicode(element).strip())))
			elif isinstance(element, Tag) and element.name == 'br':
				result.append('\n')
		return ''.join(result)
		


class SelectorError(Exception):
	pass

class SelectorNotFoundError(SelectorError):
	pass

class AmbiguousSelectorError(SelectorError):
	pass


class Selector(object):

	def __init__(self, jquery_selector):
		self.jquery_selector = jquery_selector

	def findAll(self, soup):
		if isinstance(soup, Match):
			soup = soup.element
		return map(Match, select(soup, self.jquery_selector))

	def find(self, soup):
		"""
		search for single
		"""
		if isinstance(soup, Match):
			soup = soup.element
		matches = list(self.findAll(soup))
		if not matches:
			raise SelectorNotFoundError, u'Selector %s: Element not found' % (self,)
		if len(matches) > 1:
			raise AmbiguousSelectorError, u'Selector %s: Expected one match, found %s' % (self, len(matches))
		return matches[0]

	def __unicode__(self):
		return unicode(self.jquery_selector)
			
		
class UrlGrabberExceptionContext(object):

	def __init__(self, page, match):
		self.page = page
		self.match = match


class Page(object):

	def __init__(self, grabber, url):
		self.grabber = grabber
		self.url = url
		try:
			data = grabber.opener.open(url).read()
			if not data:
				logger.error("grabbed page %s is empty" % (url))
		except Exception, e:
			logger.error("error opening %s: %s: %s, assuming page is empty" % (url, e.__class__.__name__, e))
			data = ''
		self.soup = BeautifulSoup(data)
			

	def open(self, url, triggers=None):
		"""
		called from trigger
		can open relative urls
		Triggers: { Selector : function(html, Match) }
		"""
		return self.grabber.open(self.get_absolute_url(url), triggers)

	def get_absolute_url(self, url):
		return urlunparse([item[1] or item[0] for item in zip(urlparse(self.url), urlparse(url))])

	def _process(self, triggers):
		for selector, trigger in triggers.items():
			for match in selector.findAll(self.soup):	
				try:
					trigger(self, match)
				except SelectorError:
					logger.error("skipping trigger because of selector exception:\n%s" % ''.join(traceback.format_exception(*sys.exc_info())))
					logger.error("at url: " + self.url)
				except Exception, e:
					if not hasattr(e, 'urlgrabber_context'):
						e.urlgrabber_context = UrlGrabberExceptionContext(self, match)
					raise



class UrlGrabber(object):

	def __init__(self, opener=None):
		self.opener = RetryOpener(opener or urllib2.build_opener())
	
	def open(self, url,	triggers = None):
		"""
		called initially
		Triggers: { Selector : function(html, Match) }
		"""
		page = Page(self, url)
		if triggers:
			page._process(triggers)
		return page


def url_get_slug(url, index):
	return urlparse(url)[2].strip('/').split('/')[index]

def url_parent_path(url):
	parsed = list(urlparse(url))
	path = parsed[2]
	path = path.split('/')
	del path[-2]
	path = '/'.join(path)
	parsed[2] = path
	parsed[3:] = ('','','')
	return urlunparse(parsed)


if __name__ == '__main__':
	Page(UrlGrabber(), 'http://127.0.0.1:8000/where_to_buy/where_to_buy/')