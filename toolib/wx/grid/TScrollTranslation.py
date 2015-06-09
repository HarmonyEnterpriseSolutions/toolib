
class TScrollTranslation(object):
	
	"""
	Provided functionality works for labels

	Requires:
		CalcUnscrolledPosition
		CalcScrolledPosition

	Provides:
		calcUnscrolledPosition
		calcScrolledPosition
	"""

	def calcUnscrolledPosition(self, pos, lockX=False, lockY=False):
		"""
		correct for labels
		Acccepts x < 0, y < 0 for labels, 
		CalcUnscrolledPosition is not correct for labels
		"""
		x, y = self.CalcUnscrolledPosition(pos)
		if lockX or pos[0] < 0:	x = pos[0]
		if lockY or pos[1] < 0:	y = pos[1]
		return x, y

	def calcScrolledPosition(self, pos, lockX=False, lockY=False):
		x, y = self.CalcScrolledPosition(pos)
		if lockX:	x = pos[0]
		if lockY:	y = pos[1]
		return x, y
