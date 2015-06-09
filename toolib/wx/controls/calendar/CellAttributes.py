import wx
from styledtext import StyledTextRenderer

DEFAULT_TEXTINDENT = 3
DEFUALT_TEXTALIGN = wx.ALL | wx.ALIGN_TOP | wx.ALIGN_LEFT


class AbstractCellAttributes(object):

	def drawCell(self, dc, rect, text=None):
		if self.bgBrush   is not None:	dc.SetBrush(self.bgBrush)
		if self.bgColor   is not None:  dc.SetTextBackground(self.bgColor)
		if self.textColor is not None:	dc.SetTextForeground(self.textColor)
	
		for i in xrange(self.borderWidth or 1):
			if self.borderHighlightPen is not None: dc.SetPen(self.borderHighlightPen)
			dc.DrawLines((
				rect.GetBottomLeft(),
				rect.GetTopLeft(),
				rect.GetTopRight(),
			))
			if self.borderShadowPen is not None: dc.SetPen(self.borderShadowPen)
			dc.DrawLines((
				rect.GetTopRight(),
				rect.GetBottomRight(),
				rect.GetBottomLeft(),
			))
			rect.Deflate(1, 1)

		dc.SetPen(wx.TRANSPARENT_PEN)
		dc.DrawRectangleRect(rect)

		rect.Inflate(self.borderWidth or 1, self.borderWidth or 1)

		if text:
			align  = self.textAlign  or DEFUALT_TEXTALIGN
			indent = self.textIndent or DEFAULT_TEXTINDENT

			textRect = wx.Rect(
				rect.x + (indent if align & wx.LEFT else 0), 
				rect.y + (indent if align & wx.TOP  else 0),
				rect.width  - 2 * (indent if align & wx.RIGHT  else 0),
				rect.height - 2 * (indent if align & wx.BOTTOM else 0),
			)

			if self.font:
				dc.SetFont(self.font)

			renderer = getattr(self, '_renderer', None)
			if renderer is None:
				renderer = self._renderer = StyledTextRenderer()

			dc.SetClippingRegion(*textRect)
			
			renderer.attach(dc)
			renderer.renderRect(text, textRect, align)
			renderer.detach()
			
			dc.DestroyClippingRegion()


	def merge(self, cellAttributesList):
		return CompositeCellAttributes(self, *cellAttributesList)
		

class CellAttributes(AbstractCellAttributes):

	def __init__(self, 
		bgColor         = None,
		
		borderColor     = None,
		borderHighlight = None,
		borderShadow    = None,

		borderWidth     = None,

		textColor       = None,
		font            = None,

		textAlign       = None,
		textIndent      = None,	# default is 3

		xWeight         = None,
		yWeight         = None,

		minWidth        = None,
		minHeight       = None,
		maxWidth        = None,
		maxHeight       = None,

	):
		"""
		textAlign
			LEFT                    : 0000 0000 0001 0000
			RIGHT                   : 0000 0000 0010 0000
			TOP                     : 0000 0000 0100 0000
			BOTTOM                  : 0000 0000 1000 0000

			ALIGN_LEFT              : 0000 0000 0000 0000
			ALIGN_TOP               : 0000 0000 0000 0000
			ALIGN_CENTER_HORIZONTAL : 0000 0001 0000 0000
			ALIGN_RIGHT             : 0000 0010 0000 0000
			ALIGN_BOTTOM            : 0000 0100 0000 0000
			ALIGN_CENTER_VERTICAL   : 0000 1000 0000 0000
			ALIGN_MASK              : 0000 1111 0000 0000
		"""
		self.bgColor         = bgColor
		
		self.borderHighlight = borderHighlight or borderColor
		self.borderShadow    = borderShadow    or borderColor
		self.borderWidth     = borderWidth

		self.textColor       = textColor
		self.font            = font

		self.textAlign       = textAlign
		self.textIndent      = textIndent

		self.xWeight         = xWeight
		self.yWeight         = yWeight

		self.minWidth        = minWidth
		self.minHeight       = minHeight

		self.maxWidth        = maxWidth
		self.maxHeight       = maxHeight

		self.bgBrush = wx.Brush(self.bgColor) if self.bgColor is not None else None

		self.borderHighlightPen = wx.Pen(self.borderHighlight) if self.borderHighlight is not None else None
		if self.borderShadow == self.borderHighlight:
			self.borderShadowPen = self.borderHighlightPen
		else:
			self.borderShadowPen = wx.Pen(self.borderShadow) if self.borderShadow is not None else None


class CompositeCellAttributes(AbstractCellAttributes):

	def __init__(self, *cellAtttributes):
		self.__cellAttributestList = cellAtttributes

	def __getattr__(self, name):
		for i in xrange(len(self.__cellAttributestList)-1,-1,-1):
			value = getattr(self.__cellAttributestList[i], name, None)
			if value is not None:
				return value


if __name__ == '__main__':
	from Calendar import test
	test()
