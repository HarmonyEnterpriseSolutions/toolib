from toolib.debug import deprecation
deprecation('MLabelCompletionTips is buggy and deprecated. Use XTips')


import wx
from errors import GridHitSpace
from TScrollTranslation import TScrollTranslation
from TCellRect import TCellRect


class MLabelCompletionTips(TScrollTranslation, TCellRect):
	"""
	Adds hit testing functionality to wx.grid.Grid

	NOTE: Still have cosmetic issues for too small columns

	Requires:
		GetNumberRows
		GetNumberCols

		GetRowSize
		GetColSize

		CalcUnscrolledPosition
		CalcScrolledPosition

	Provides:
		hitTest

		ScrollTranslation.*
	"""
	
	LINDENT = -20
	RINDENT = 5

	def __init__(self, row=True, col=True):
		if row:	
			self.GetGridRowLabelWindow().Bind(wx.EVT_MOTION, self.__onLabelMotion)
			self.GetGridRowLabelWindow().Bind(wx.EVT_LEAVE_WINDOW, self.__onLabelLeaveWindow)
			
		if col:	
			self.GetGridColLabelWindow().Bind(wx.EVT_MOTION, self.__onLabelMotion)
			self.GetGridColLabelWindow().Bind(wx.EVT_LEAVE_WINDOW, self.__onLabelLeaveWindow)

		self.__lastPos = None
		self.__tip = None

		self.__rowTipProviders = [self.GetRowLabelValue]
		self.__colTipProviders = [self.GetColLabelValue]

	def getRowLabelTipValue(self, row):
		return '\n'.join(filter(None, [f(row) for f in self.__rowTipProviders]))

	def getColLabelTipValue(self, col):
		return '\n'.join(filter(None, [f(col) for f in self.__colTipProviders]))

	def getRowTipProviderList(self):
		return self.__rowTipProviders

	def getColTipProviderList(self):
		return self.__colTipProviders

	def __onLabelMotion(self, event):
		if not event.Dragging():

			x, y = event.GetPosition()
			window = event.GetEventObject()

			if window is self.GetGridColLabelWindow():
				y -= self.GetColLabelSize()
			elif window is self.GetGridRowLabelWindow():
				x -= self.GetRowLabelSize()
			else:
				assert 0, "unexpected window"

			try:
				row, col = self.hitTest((x, y), self.LINDENT, self.RINDENT)

				if self.__lastPos != (row, col):
		            
					if self.LINDENT < 0:
						if   col != -1: lindent = max(5, self.LINDENT + self.GetColSize(col))
						elif row != -1: lindent = max(5, self.LINDENT + self.GetRowSize(row))
						else: 
							raise NotImplementedError, "lindent undefined"
					else:
						lindent = self.LINDENT
					
					self.__lastPos = (row, col)

					if   row == -1 and col != -1:	value = self.getColLabelTipValue(col)
					elif row != -1 and col == -1:	value = self.getRowLabelTipValue(row)
					else:							value = None

					if value:	
						x,y,w,h = self.getCellRect(row, col)
						x,y = window.ClientToScreen((x,y))

						if col != -1:
							x+=lindent
							w-=lindent+self.RINDENT
						
						if row != -1:
							y+=lindent
							h-=lindent+self.RINDENT

						if self.__tip:
							self.__tip.Destroy()
							self.__tip = None

						x, y = self.calcScrolledPosition((x, y), lockX=col==-1, lockY=row==-1)
	
						self.__tip = wx.TipWindow(window, value)
						self.__tip.SetBoundingRect((x,y,w,h))

			except GridHitSpace:
				pass

		event.Skip()

	def __onLabelLeaveWindow(self, event):
		self.__lastPos = None
		event.Skip()
