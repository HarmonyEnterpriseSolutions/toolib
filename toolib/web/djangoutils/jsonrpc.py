# jsonrpc.py
#   original code: http://trac.pyworks.org/pyjamas/wiki/DjangoWithPyJamas
#   also from: http://www.pimentech.fr/technologies/outils
import sys
import traceback
from django.utils import simplejson
from django.http import HttpResponse

# JSONRPCService and jsonremote are used in combination to drastically
# simplify the provision of JSONRPC services.  use as follows:
#
# from jsonrpc import JSONRPCService, jsonremote
#
# jsonservice = JSONRPCService()
#
# @jsonremote(jsonservice)
# def test(request, echo_param):
#	  return "echoing the param back: %s", echo_param
#
# then dump jsonservice into urlpatterns:
#  (r'^service1/$', 'djangoapp.views.jsonservice'),

DEBUG = 0


def error(id, message):
	return {
		'id': id, 
		'code': -1,
		'error': message,
	}

class RPCServiceError(Exception):
	pass


class Transaction(object):
	def __init__(self, request, response):
		self.request = request
		self.response = response


class JSONRPCService(object):
	def __init__(self, method_map={}, encoding='UTF8'):
		self.method_map = method_map
		self._encoding = encoding

	def add_method(self, name, method):
		self.method_map[name] = method

	def __call__(self, request, extra=None):
		
		# We do not yet support GET requests, something pyjamas does
		# not use anyways.
		try:
			body = request.body
		except AttributeError:
			# django 1.3 support
			body = request.raw_post_data

		data = simplejson.loads(body, encoding=self._encoding)

		response = HttpResponse()

		# Altered to forward the request parameter when a member method
		# is invoked <julien@pimentech.net>
		id, method, params = data["id"], data["method"], [Transaction(request, response)] + data["params"]
		
		if method in self.method_map:
			try:
				rc = self.method_map[method](*params)
			except RPCServiceError, e:
				# expected RPC error
				result = error(id, "%s: %s" % (e.__class__.__name__, decode_exception(str(e))))
			except:
				# unexpected
				result = error(id, '%s was called, but encountered an error: %s' % (method, decode_exception(traceback.format_exc())))
			else:
				result = {
					'id': id,
					'result': rc,
				}
		else:
			result = error(id, 'method "%s" does not exist' % method)

		if DEBUG:
			self._check(result)

		response.write(simplejson.dumps(result, encoding=self._encoding))

		return response


	def _check(self, o):
		if o is None:
			pass
		elif isinstance(o, dict):
			self._check_dict(o)
		elif isinstance(o, (list, tuple)):
			self._check_list(o)
		elif isinstance(o, str):
			try:
				unicode(o)
			except:
				raise RuntimeError, "str value %s cannot be coerced to unicode" % repr(o)
		elif isinstance(o, (int, long, float, unicode)):
			pass
		else:
			raise RuntimeError, 'Unknown type: %s (value: %s)' % (type(o), repr(o))

	def _check_dict(self, d):
		print ">>> check dict"
		for k, v in d.iteritems():
			print '>>>', k, repr(v)
			self._check(k)
			self._check(v)

	def _check_list(self, l):
		print ">>> check list"
		for v in l:
			print '>>>', v
			self._check(v)


def jsonremote(service):
	"""Make JSONRPCService a decorator so that you can write :

	from jsonrpc import JSONRPCService
	chatservice = JSONRPCService()

	@jsonremote(chatservice)
	def login(request, user_name):
		(...)
	"""
	def remotify(func):
		if isinstance(service, JSONRPCService):
			service.add_method(func.__name__, func)
		else:
			emsg = 'Service "%s" not found' % service.__name__
			raise NotImplementedError, emsg
		return func
	return remotify


def decode_exception(s):
	try:
		return s.decode(sys.getdefaultencoding())
	except UnicodeDecodeError:
		try:
			return s.decode('cp1251')
		except UnicodeDecodeError:
			return s.decode('ascii', 'replace')
