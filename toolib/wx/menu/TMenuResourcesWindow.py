from toolib.wx.mixin.TWindowProperty import TWindowProperty

class TMenuResourcesWindow(TWindowProperty):
	"""
	Requires:
		GetParent
	Provides:
		getResources
		getParentWindowProperty
	"""
	def getMenuResources(self):
		if not hasattr(self, '_TMenuResourcesWindow__menuResources'):
			self.__menuResources = self.getParentWindowProperty('menuResources')
		return self.__menuResources

