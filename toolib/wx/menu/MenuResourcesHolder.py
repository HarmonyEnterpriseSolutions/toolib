class MenuResourcesHolder(object):
	def __init__(self, menuResources):
		self._resources = menuResources

	def getMenuResources(self):
		return self._resources

	def getButtonResource(self, key):
		return self._resources.getButtonResource(key)
