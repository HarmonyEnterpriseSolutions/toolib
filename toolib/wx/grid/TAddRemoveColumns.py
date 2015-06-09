from toolib.util.iterators import iterContinuousRanges

class TAddRemoveColumns(object):

	def OnRemoveColumns(self, event):
		indices = filter(lambda x: x >= 0, self.GetSelectedCols())
		if indices:
			indices.sort()
			self.ClearSelection()
			for index, size in iterContinuousRanges(indices):
				self.GetTable().DeleteCols(index, size)

	def OnInsertColumn(self, event):
		cols = self.GetSelectedCols()
		if len(cols) == 1 and cols[0] >= 0:
			self.ClearSelection()
			self.GetTable().InsertCols(cols[0], 1)

	def OnAppendColumn(self, event):
		self.GetTable().AppendCols(1)


	