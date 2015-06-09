
class TClickSelection(object):
	"""
	Requires:
		GetSelectionMode
		SelectBlock
		SelectCol
		SelectRow
		SetGridCursor
	
		wxGridSelectCells
		wxGridSelectColumns
		wxGridSelectRows

	Provides:
		makeClickSelection

	"""
	
	def makeClickSelection(self, row, col):
		"""
		makes same selection as when clicking on grid or labels
		"""
		if row >= 0 and col >= 0:
			self.SetGridCursor(row, col)
		else:
			#hide cursor?
			pass

		if self.GetSelectionMode() == self.wxGridSelectCells:
			if row == -1:
				if col == -1:
					self.SelectAll()
				else:
					self.SelectCol(col)
			else:
				if col == -1:
					self.SelectRow(row)
				else:
					self.SelectBlock(row, col, row, col)

		elif self.GetSelectionMode() == self.wxGridSelectRows:
			if row == -1:
				if col == -1:
					self.SelectAll()
				else:
					self.ClearSelection()
			else:
				self.SelectRow(row)

		elif self.GetSelectionMode() == self.wxGridSelectColumns:
			if col == -1:
				if row == -1:
					self.SelectAll()
				else:
					self.ClearSelection()
			else:
				self.SelectCol(col)
