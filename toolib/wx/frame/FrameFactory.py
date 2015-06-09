import wx

class FrameFactory(object):
	"""
	delegates parent frame 
	"""

	__id__ = NotImplemented

	def __init__(self, parentFrame):
		self.__parentFrame = parentFrame

	def getId(self):
		return self.__id__

	def getParentFrame(self):
		return self.__parentFrame

	def processCommand(self, event, *args):
		raise NotImplementedError, 'abstract'

	def __getattr__(self, name):
		return getattr(self.__parentFrame, name)

