#################################################################
# Program:   wlib
"""
Class, providing interface for transaction information, abstracting of
web server version
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2008/06/10 13:24:58 $"
__version__ = "$Revision: 1.1 $"
# $Source: D:/HOME/cvs/toolib/web/kit/TransactionInfo.py,v $
#
#################################################################
import sys, os
from toolib import debug

ENV_DEFAULTS = {
	"HTTPS" : "off",	 # Apatche does not write it for https is off. IIS does
	"QUERY_STRING" : "", # IIS does not write it for no query string. Apache does
}


class XTransactionInfo(object):
	"""
	must be placed before servlet in inheritance chain
	"""

	def awake(self, trans):
		super(XTransactionInfo, self).awake(trans)
		self.__transaction = trans
		if hasattr(self, '_TransactionInfoMixIn__info'):
			self.__info.awake(trans)

	def sleep(self, trans):
		if hasattr(self, '_TransactionInfoMixIn__info'):
			self.__info.sleep(trans)
		self.__transaction = None
		super(XTransactionInfo, self).sleep(trans)

	def info(self):
		if not hasattr(self, '_TransactionInfoMixIn__info'):
			self.__info = TransactionInfo(self.__transaction)
		return self.__info

	# aliases DEPRECATED
	getInfo = info


class TransactionInfo(object):
	def __init__(self, trans=None):
		self.defaults = ENV_DEFAULTS
		if trans:
			self.awake(trans)

	def awake(self, trans):
		#self._transaction = trans
		self._request = trans.request()
		self._env = self._request.environ()
		#self._response = trans.response()

	def sleep(self, trans):
		#self._transaction = None
		self._request = None
		self._env = None
		#self._response = None

	def get(self, key, default=NotImplemented):
		val = self._env.get(key, default)
		if val is NotImplemented:
			val = self.defaults.get(key, NotImplemented)
			if val is NotImplemented:
				raise KeyError, key
		return val

	def getServletPath(self):
		return self._request.servletPath()

	def getServerSoftware(self):
		return self.get("SERVER_SOFTWARE")

	def getServerSoftwareName(self):
		"""
		returns string server name, e.g.
			"Apatche/1.3.26 (win32)"	gives "Apatche"
			"Microsoft-IIS/5.0"			gives "Microsoft-IIS"
		"""
		ss = self.getServerSoftware()
		return ss[:ss.find('/')]

	def getServerSoftwareVersion(self):
		"""
		returns float server version, e.g.
			"Apatche/1.3.26 (win32)"	gives 1.326
			"Microsoft-IIS/5.0"			gives 5.0
		"""
		ss = self.getServerSoftware()
		nums = ss[ss.rfind('/')+1 : ss.find(' ')].split('.')
		return float(nums[0]+'.'+''.join(nums[1:]))

	def getServerName(self):
		return self.get("SERVER_NAME")

	def getServerPort(self):
		return self.get("SERVER_PORT")

	def getServerProtocol(self):
		return self.get("SERVER_PROTOCOL")

	def getScriptName(self):
		return self.get("SCRIPT_NAME")

	def getHttps(self):
		return self.get("HTTPS")

	def getHttpHost(self):
		return self.get("HTTP_HOST")

	def isHttpsOn(self):
		return self.getHttps() == "on"

	def getPathInfo(self):
		""" sula/info """
		return self._request.pathInfo()

	def getServletPath(self):
		""" /sula07/wk.cgi """
		return self._request.servletPath()

	def getAppContext(self):
		pathInfo = self.getPathInfo()
		return pathInfo.split('/')[1]

	def getAppContextUri(self):
		return "%s/%s" % (self.getServletPath(), self.getAppContext())

	def getWebRootUri(self):
		path = self.getServletPath()
		return path[:path.rfind('/')]

	def getRequestMethod(self):
		return self._request.method()

	def getRequestUri(self):
		return self._request.uri()

	def getQueryString(self):
		return self._request.queryString()

	def getAdapterName(self):
		path = self.getServletPath()
		return path[path.rfind('/')+1:]

	def getRemoteAddress(self):
		return self.get("REMOTE_ADDR")

	def getCertSubject(self):
		if self.isHttpsOn():
			serv = self.getServerSoftware()
			if serv.startswith('Apache'):
				return self.get('SSL_CLIENT_S_DN_CN')
			if serv.startswith('Microsoft'):
				return self.get('CERT_SUBJECT')

	def getServerUrl(self):
		if self.getHttps() == "on":
			protocol = "https"
		else:		
			protocol = "http"

		return "%s://%s" % (protocol, self.getHttpHost())


	def getWebRootUrl(self):
		return "%s%s" % (self.getServerUrl(), self.getWebRootUri())

	def getAppContextUrl(self):
		return "%s%s" % (self.getServerUrl(), self.getAppContextUri())

	def asDict(self):
		dict = {}
		methods = self.__class__.__dict__
		for methodName in methods:
			if methodName.startswith('get') and len(methodName) > 3:
				key = methodName[3].lower() + methodName[4:]
				try:
					dict[key] = methods[methodName](self)
				except:
					dict[key] = "ERROR: " + debug.strexc(sys.exc_info())
		return dict

	def getPathTranslated(self):
		return self.get("PATH_TRANSLATED")

	def getWebRootPath(self):
		return os.path.sep.join(self.getPathTranslated().split(os.path.sep)[:-self.getPathInfo().count('/')])

#if __name__ == '__main__':
#   Environment().toDictionary()

