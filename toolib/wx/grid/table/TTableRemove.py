class TTableRemove(object):

	def removeColumns(self, indices):
		indices.sort()
		indices.reverse()
		for i in indices:
			self.DeleteCols(i, 1)

	def removeRows(self, indices):
		indices.sort()
		indices.reverse()
		for i in indices:
			self.DeleteRows(i, 1)
