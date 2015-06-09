import wx
from XTips import XTips

class XCustomTreeColumnsTips(XTips):

	def hitTest(self, pos):
		hit = super(XCustomTreeColumnsTips, self).hitTest(pos)

		column = None
		if hit[1] & wx.TREE_HITTEST_ONITEMRIGHT:
			x = pos[0]
			x -= self.getColumnsBaseX()
			if x >= 0:
				for col in xrange(self.getColumnCount()):
					w = self.getColumnWidth(col)
					if x < w:
						column = col
						break
					else:
						x -= w

		# insert Custom tree column number as third parameter - 
		# HyperTreeList column number will move to 4 position (+3)
		hit.insert(2, column)
		return hit

	def getTipValue(self, item, hit, column):
		return "%s, column=%s" % (
			super(XCustomTreeColumnsTips, self).getTipValue(item, hit), 
			column
		)
