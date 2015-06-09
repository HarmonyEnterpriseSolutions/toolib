class MGridMessaging(object):
	"""
	Overrides SetTable
	inherit before Grid
	"""
	def SetTable(self, table, takeOwnership=False):
		"""
		Messaging
		"""
		oldTable = self.GetTable()
		if oldTable:
			# let old table to forget control
			oldTable.removeGridTableListener(self)		
		super(MGridMessaging, self).SetTable(table, takeOwnership)
		if table is not None:
			# allow new table to notify control
			table.addGridTableListener(self)				
