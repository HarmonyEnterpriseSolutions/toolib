from toolib.util.Configurable import Configurable

class TConfigurable(Configurable):
	"""
	adds column size persistence
	call .saveConfig() on grid close

	Requires:
		getCore
			with getDomain
			with getProjectPath

		Table.getColumnId

		or 

		getDomain
		getProjectPath


	"""

	def applyConfig(self):
		for i in xrange(self.GetNumberCols()):
			try:
				self.SetColSize(i, self.getSetting('col[%s].size' % self.GetTable().getColumnId(i), self.GetDefaultColSize()))
			except IndexError:
				pass

	def getDefaultUserConfig(self):
		d = {}
		for i in xrange(self.GetNumberCols()):
			try:
				d['col[%s].size' % self.GetTable().getColumnId(i)] = self.GetDefaultColSize()
			except IndexError:
				pass
		return d

	def saveConfig(self):
		for i in xrange(self.GetNumberCols()):
			try:
				self.setSetting('col[%s].size' % self.GetTable().getColumnId(i), self.GetColSize(i))
			except IndexError:
				pass
		# do not save local conf
		return self.saveUserConfig()
