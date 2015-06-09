import operator


class TColumnExtraWidth(object):
	
	"""
	Requires:
		GetColSize
		GetNumberCols
		GetRowLabelSize
		GetVirtualSize
		SetColSize

	Provides:
		getGridWidth
		distributeExtraWidth

	"""

	def getGridWidth(self):
		"""
		row label width + all cells
		"""
		return self.GetRowLabelSize() + reduce(
			operator.add,
			[self.GetColSize(i) for i in xrange(self.GetNumberCols())],
			0,
		)

	
	def distributeExtraWidth(self, startIndex=0):
		fixScrollWidth=25

		#rint '----------- distributing extra width ------------'

		#rint 'virtual width:', self.GetVirtualSize()[0]
		#rint 'grid width   :', self.getGridWidth()

		extraWidth = self.GetVirtualSize()[0] - self.getGridWidth() - fixScrollWidth

		#rint 'extra wifth:', extraWidth

		if extraWidth > 0:
			n = self.GetNumberCols() - startIndex
			if n > 0:
				eachExtra = extraWidth / n
				for index in xrange(startIndex, self.GetNumberCols()):
					if index == self.GetNumberCols() - 1:
						self.SetColSize(index, self.GetColSize(index) + extraWidth)
					else:
						self.SetColSize(index, self.GetColSize(index) + eachExtra)
						extraWidth -= eachExtra

		#rint 'grid width after:', self.getGridWidth()
