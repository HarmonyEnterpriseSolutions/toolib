import wx
from errors import GridHitSpace
from THitTest import THitTest

class XTips(THitTest):
	"""
	Adds hit testing functionality to wx.grid.Grid

	Requires:
		getColLabelTipValue
	"""
	
	LINDENT = 5
	RINDENT = 5

	TINDENT = 2
	BINDENT = 2

	def __init__(self, *args, **kwargs):
		super(XTips, self).__init__(*args, **kwargs)
		
		allowed = self.tipsAllowed()

		if 'rowlabel' in allowed or 'labels' in allowed:
			self.GetGridRowLabelWindow().Bind(wx.EVT_MOTION, self.__onMotion)
		if 'collabel' in allowed or 'labels' in allowed:
			self.GetGridColLabelWindow().Bind(wx.EVT_MOTION, self.__onMotion)
		if 'grid' in allowed:
			self.GetGridWindow().Bind(wx.EVT_MOTION, self.__onMotion)
		
		self.__lastPos = None

	def getTipValue(self, row, col):
		return None

	def tipsAllowed(self):
		return ('rowlabel', 'collabel', 'labels', 'grid')

	def __onMotion(self, event):
		if not event.Dragging():
			try:
				if self.CanDragRowSize():
					topIndent, bottomIndent = self.TINDENT, self.BINDENT
				else:
					topIndent, bottomIndent = 0, 0

				if self.CanDragColSize():
					leftIndent, rightIndent = self.LINDENT, self.RINDENT
				else:
					leftIndent, rightIndent = 0, 0

				row, col = self.hitTest(event.GetPosition(), leftIndent, rightIndent, topIndent, bottomIndent, window=event.GetEventObject())
				#rint row, col

 				if (row, col) != self.__lastPos:

					text = self.getTipValue(row, col)
					
					tip = event.GetEventObject().ToolTip
					if text:
						if tip:
							tip.SetTip(text)
						else:
							tip = event.GetEventObject().ToolTip = wx.ToolTip(text)
					elif tip:
							tip.SetTip("")

					self.__lastPos = (row, col)

			except GridHitSpace:
				#rint 'space'
				if event.GetEventObject().ToolTip:
					event.GetEventObject().ToolTip.SetTip('')

				self.__lastPos = None

		event.Skip()

