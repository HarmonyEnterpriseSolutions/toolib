from TWindowProperty import TWindowProperty

class TResourcesHolderWindow(TWindowProperty):
	"""
	Requires:
		GetParent
	Provides:
		getResources
		getParentWindowProperty
	"""
	def getResources(self):
		if not hasattr(self, '_TResourcesHolderWindow__resources'):
			self.__resources = self.getParentWindowProperty('resources')
		return self.__resources
