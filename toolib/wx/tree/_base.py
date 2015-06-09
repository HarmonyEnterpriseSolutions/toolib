class TExpansion(object):

	"""
	Requires:
		iterNodes

	Provides:
		setExpandedNodeIds
		getExpandedNodeIds
		findNode
	"""

	def getExpandedNodeIds(self):
		s = set()
		for node in self.iterNodes():
			if node.isExpanded():
				id = node.getId()
				if id is not NotImplemented:
					s.add(node.getId())
		return s

	def setExpandedNodeIds(self, ids):
		for node in self.iterNodes():
			if node.getId() in ids:
				node.setExpanded(True)

	def findNode(self, id):
		for node in self.iterNodes():
			if node.getId() == id:
				return node
