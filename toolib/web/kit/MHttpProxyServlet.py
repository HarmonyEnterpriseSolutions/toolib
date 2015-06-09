import sys
import urllib
import urllib2
from urlparse import urlparse, urlunparse
from cookielib import CookieJar
from TRespondToAny import TRespondToAny
from toolib import debug

DEBUG = 0


class MHttpProxyServlet(TRespondToAny):
	"""
		override createDefaultUrlOpener for http proxy support
	"""	

	def __init__(self, 
			targetUrl = None,
			methods   = ('GET', 'POST'),
			timeout   = None,
		):
		self.__targetUrl = targetUrl
		self.__methods = set(methods)
		self.__timeout = timeout

		# can't store it in session because of pickling problems
		self.__urlOpenerCache = {}
		self.__cookieJarCache = {}


	def respondToAny(self, trans):
		if trans.request().method() in self.__methods:

			try:
				url = urlunparse(
					urlparse(self.getTargetUrl()  )[:3] + 
					urlparse(trans.request().uri())[3:]
				)

				if DEBUG: print '[REQUEST] %s %s' % (trans.request().method(), url)

				if trans.request().method() == 'GET':
					data = None
				else:
					raw = trans.request().rawInput(True)
					if raw:
						data = raw.read()
					else:
						data = urllib.urlencode(trans.request().fields())
			
					if DEBUG: print '[REQUEST] Post-data: %s' % data

				if sys.version[:3] >= '2.6':
					response = self.__getUrlOpener(trans).open(url, data, self.__timeout)
				else:
					if self.__timeout is not None:
						debug.warning('urlopen timeout not supported in python version < 2.6')
					response = self.__getUrlOpener(trans).open(url, data)

				trans.response().setHeader('Status', "%s %s" % (response.code, response.msg))
				if DEBUG: print '[RESPONSE] %s %s' % (response.code, response.msg)

				for name, value in response.headers.items():
					if DEBUG: print '[RESPONSE] %s: %s' % (name, value),
					if name not in ('transfer-encoding', 'set-cookie'):
						trans.response().setHeader(name, value)
						if DEBUG: print '[PASSED]'
					else:
						if DEBUG: print '[SKIPPED]'

				resp = response.read()
				if DEBUG: print '[RESPONSE] Body: %s..., length=%s' % (resp[:4], len(resp))
				trans.response().write(resp)

			except urllib2.HTTPError, e:
				trans.response().setHeader('Status', "%s %s" % (e.code, e.msg))
				trans.response().write(e.read())
			except urllib2.URLError, e:
				trans.response().setHeader('Status', "502 Bad Gateway (%s: %s)" % (e[0][0], e[0][1]))
			except IOError, e:
				trans.response().setHeader('Status', "502 Bad Gateway (%s: %s)" % (e.__class__.__name__, e))
				#trans.response().write("%s: %s" % (e.__class__.__name__, e))
		else:
			self.notImplemented()

	def __getUrlOpener(self, trans):
		sid = trans.session().identifier()
		opener = self.__urlOpenerCache.get(sid)
		if opener is None:
			self.__urlOpenerCache[sid] = opener = urllib2.build_opener(
				urllib2.HTTPCookieProcessor(self.getCookieJar(trans)),
				*self.createAdditionalUrlHandlers(trans)
			)
		return opener

	def createAdditionalUrlHandlers(self, trans):
		"""overrideable, returns tuple of handlers"""
		return ()

	def getCookieJar(self, trans):
		sid = trans.session().identifier()
		cj = self.__cookieJarCache.get(sid)
		if cj is None:
			self.__cookieJarCache[sid] = cj = CookieJar()
		return cj

	def getTargetUrl(self):
		return self.__targetUrl

	def setTargetUrl(self, url):
		self.__targetUrl = url
