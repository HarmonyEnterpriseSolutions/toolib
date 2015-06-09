class TCellEditing(object):
	"""
	Requires:
		SaveEditControlValue
		MoveCursorLeft
		MoveCursorRight
		MoveCursorUp
		MoveCursorDown

	Provides:
		stopCellEditing
	"""
	def stopCellEditing(self):
		"""
		TODO: stop editing more gentle
		now must have more than one columns to work
		"""
		self.SaveEditControlValue()

		# hack to close editor
		if self.MoveCursorLeft(False):
			self.MoveCursorRight(False)
		else:
			if self.MoveCursorRight(False):
				self.MoveCursorLeft(False)
