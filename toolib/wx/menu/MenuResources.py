import wx
import types
from toolib.wx.Resources	import Resources
from ButtonResource			import ButtonResource
from toolib.util.Cache 		import Cache
from toolib					import debug

class MenuResources(object):	# delegates from Resources
	"""
	Resources for menues and toolbar, stored in frame
	"""

	def __init__(self, resources, actionConf):
		assert isinstance(resources, Resources)

		self.__resources = resources
		self.__actionConf = actionConf
		self.__brByCommand = Cache(self._loadButtonResource)
		self.__brById = {}

	def __getattr__(self, name):
		return getattr(self.__resources, name)

	def getButtonResource(self, key):
		"""
		key may be
			action command
			wxId
			event, item, etc. - must have .GetId()
		"""
		if isinstance(key, types.StringTypes):
			return self.__brByCommand[key]
		elif isinstance(key, (int, long)):
			return self.__brById[key]
		elif hasattr(key, 'GetId'):
			return self.__brById[key.GetId()]
		else:
			raise RuntimeError, "Can't get button resource for key type %s" % (type(key))

	def _loadButtonResource(self, command):
		buttonResource = ButtonResource(self, command, self.__actionConf.get(command, {}))
		self.__brById[buttonResource.getId()] = buttonResource
		return buttonResource
