import wx
from toolib.util.lang import isCastable
from FrameFactory import FrameFactory

class FrameFactoryDispatcher(object):
	SEP_COMMAND = ':'

	def __init__(self):
		self.__frameFactories = {}

	def bindFrameFactory(self, frameFactory):
		self.__frameFactories[frameFactory.getId()] = frameFactory

	def getFrameFactory(self, id):
		try:
			return self.__frameFactories[id]
		except KeyError:
			raise KeyError, "No frame factory with id == '%s'" % id

	def OnCommand(self, event):
		command = self.getMenuResources().getButtonResource(event).getCommand()
		l = command.split(self.SEP_COMMAND)
		wx.BeginBusyCursor()
		try:
			return self.getFrameFactory(l[0]).processCommand(event, *l[1:])
		finally:
			wx.EndBusyCursor()

if __name__ == '__main__':
	print FrameFactoryDispatcher().getFrameFactory('objectSet')
