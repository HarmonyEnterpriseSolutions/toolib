from toolib.util.iterators import iterContinuousRanges

class TAddRemoveRows(object):

	def OnRemoveRows(self, event):
		indices = filter(lambda x: x >= 0, self.GetSelectedRows())
		if indices:
			indices.sort()
			self.ClearSelection()
			for index, size in iterContinuousRanges(indices):
				self.GetTable().DeleteRows(index, size)

	def OnInsertRow(self, event):
		rows = self.GetSelectedRows()
		if len(rows) == 1 and rows[0] >= 0:
			self.ClearSelection()
			self.GetTable().InsertRows(rows[0], 1)

	def OnAppendRow(self, event):
		self.GetTable().AppendRows(1)
