#################################################################
# Program: Toolib
"""

"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2007/03/27 14:54:21 $"
__version__ = "$Revision: 1.10 $"
# $Source: D:/HOME/cvs/toolib/wx/menu/ButtonResource.py,v $
#
#################################################################
import wx
from toolib import debug
from toolib.util import lang

class ButtonResource(object):
	def __init__(self, menuResources, command, config=None):
		assert command

		self.__resources = menuResources
		self.__command = command
		self.__config = config
		self.__id = None
		self.__methodName = None

	def getCommand(self):
		return self.__command

	def getAcceleratorString(self):
		"""
		returns accel from config or extract accelerator from name
		"""
		return self.__config.get('accel') or '\t'.join(self.getText().split('\t')[1:])

	def getAcceleratorEntry(self):
		accel = wx.GetAccelFromString("dummy\t" + self.getAcceleratorString())
		if accel is not None:
			accel.Set(accel.GetFlags(), accel.GetKeyCode(), self.getId())
		return accel

	def getText(self):
		return self.__config.get('text') or self.__command

	def getTip(self):
		return self.__config.get('tip') or self.getText()

	def getHelp(self):
		return self.__config.get('help') or self.getTip()

	def getContext(self, name):
		c = self.__config.get('context', {})
		if isinstance(c, dict):
			return c.get(name)
		else:
			debug.deprecation("deprecated unnamed menu context defined: %s" % (c,))
			return c

	def getKind(self):
		return self.__config.get('kind', wx.ITEM_NORMAL)

	def getIconName(self):
		return self.__config.get('icon')

	def getBitmap(self, default=None):
		return self.__resources.getBitmap(self.getIconName(), default)

	def getId(self):
		"""
		returns wxID
		"""
		if self.__id is None:
			if self.getKind() == wx.ID_SEPARATOR:
				self.__id = wx.ID_SEPARATOR
			else:
				self.__id = self.__config.get('id') or wx.NewId()
		return self.__id

	def getSubmenuConfig(self):
		return self.__config.get('submenu')

	def getState(self):
		return self.__config.get('state', False)

	def getMethodName(self):
		if self.__methodName is None:		
			self.__methodName = 'On' + self.__command[0].upper() + self.__command[1:]
			# replace all non _A-Za-z0-9 to underscore
			self.__methodName = ''.join([lang.iif(ch.isalnum() or ch == '_', ch, '_') for ch in self.__methodName])
			self.__methodName.replace(':', '_')
		return self.__methodName

	def isEnabled(self):
		return self.__config.get('enabled', True)

	def getUserValue(self, key, default = NotImplemented):
		try:
			return self.__config['userConfig'][key]
		except KeyError:
			if default is NotImplemented:
				raise
			else:
				return default

	def connect(self, window, eventType):
		method = getattr(window, self.getMethodName(), None) or getattr(window, "OnCommand", None)
		if method:
			window.Connect(self.getId(), -1, eventType, method)
		else:
			debug.warning('No method %s or OnCommand in %s' % (self.getMethodName(), window.__class__.__name__))
	
