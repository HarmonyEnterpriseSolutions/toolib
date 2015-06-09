import wx
import wx.grid

class _Delegator(wx.grid.GridCellAttr):
	
	def __init__(self, attr):
		self.attr = attr

	def __getattr__(self, name):
		return getattr(self.attr, 'Set%s%s' % (name[0].upper(), name[1:]))

	def hAlign(self, hAlign):
		if self.attr.HasAlignment():
			self.attr.SetAlignment(hAlign, self.attr.GetAlignment()[1])
		else:
			self.attr.SetAlignment(hAlign, wx.ALIGN_TOP)
	
	def vAlign(self, vAlign):
		if self.attr.HasAlignment():
			self.attr.SetAlignment(self.attr.GetAlignment()[0], vAlign)
		else:
			self.attr.SetAlignment(wx.ALIGN_LEFT, vAlign)

	def alignment(self, alignment):
		self.attr.SetAlignment(*alignment)


class TAttrCreator(object):

	def newAttr(self, **args):
		"""
		Creates new GridCellAttr

		Available named args is
			* hAlign (if set, vAlign will default to wx.ALIGN_TOP)
			* vAlign (if set, hAlign will default to wx.ALIGN_LEFT)

			* textColour
			* backgroundColour
			* font
			* readOnly
			* any other property wx.grid.GridCellAttr has setter for

		Corresponding setter will be used
		"""
		a = _Delegator(wx.grid.GridCellAttr())	# constructor with params seems to be deprecated
		for key, value in args.iteritems():
			getattr(a, key)(value)
		return a.attr

	
if __name__ == '__main__':
	wx.App()
	f = TAttrCreator()
	print f.newAttr(hAlign=wx.ALIGN_RIGHT).GetAlignment()
	print f.newAttr(vAlign=wx.ALIGN_BOTTOM).GetAlignment()

	print f.newAttr(hAlign=wx.ALIGN_RIGHT, vAlign=wx.ALIGN_BOTTOM).GetAlignment()

	print f.newAttr(textColour="#102030").GetTextColour()
	print f.newAttr(backgroundColour="#102030").GetBackgroundColour()
	print f.newAttr(font=wx.Font(10, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)).GetFont().GetFamily()
	print f.newAttr(readOnly=True).IsReadOnly()

