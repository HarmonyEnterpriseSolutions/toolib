import wx

import datetime
from CalendarDrawing import CalendarDrawing
from CalendarModel import CalendarModel


class Calendar( wx.PyControl ):

	def __init__(self, parent, id, pos=wx.DefaultPosition, size=wx.Size(200,200),
				   style= 0, validator=wx.DefaultValidator,
				   name= "calendar", model = None, cellAttributesDict = None):

		wx.PyControl.__init__(self, parent, id, pos, size, style, validator, name)

		self.BackgroundColor = 'WHITE'

		self.__model = model or CalendarModel()

		if cellAttributesDict is None:
			import config
			cellAttributesDict = config.CELL_ATTRIBUTES_DICT

		self.__drawing = CalendarDrawing(self.__model, cellAttributesDict)

		self.Bind(wx.EVT_SET_FOCUS,    lambda event: self.__onFocus(event, True), self)
		self.Bind(wx.EVT_KILL_FOCUS,   lambda event: self.__onFocus(event, False), self)

		self.Bind(wx.EVT_KEY_DOWN,     self.__onKeyDown, self)
		self.Bind(wx.EVT_MOUSE_EVENTS, self.__onMouse, self)
		self.Bind(wx.EVT_PAINT,        self.__onPaint)
		self.Bind(wx.EVT_SIZE,         self.__onSize)
		self.Bind(wx.EVT_MOTION,       self.__onMotion, self)

		self.__oldDragCell = None

		self.__model.listeners.bind('propertyChanged', self.__onPropertyChanged)

		self.__lastMotionCell = None

		# refresh state members
		self.__refreshPending = False
		self.__refreshCells = set()
		self.__refreshFull = False



	def AcceptsFocus(self):
		return self.IsShown() and self.IsEnabled()

	def __onFocus(self, event, focus):
		self.__drawing.setFocus(focus)
		cells = set(self.__getPeriodCells(self.__model.getSelection()))
		cells.add(self.__getDateCell(self.__model.getDate()))
		self.refresh(cells)
		event.Skip()

	def __onKeyDown(self, event):

		key_code = event.GetKeyCode()
		
		if key_code == wx.WXK_UP:
			self.__model.incDay(-7, event.ShiftDown())
		elif key_code == wx.WXK_DOWN:
			self.__model.incDay(7, event.ShiftDown())
		elif key_code == wx.WXK_LEFT:
			self.__model.incDay(-1, event.ShiftDown())
		elif key_code == wx.WXK_RIGHT:
			self.__model.incDay(1, event.ShiftDown())
		elif key_code == wx.WXK_HOME:
			self.__model.setDate(datetime.date.today(), event.ShiftDown())
		elif key_code == wx.WXK_PAGEUP:
			self.__model.incMonth(-12 if event.ControlDown() else -1)
		elif key_code == wx.WXK_PAGEDOWN:
			self.__model.incMonth(12 if event.ControlDown() else 1)
		else:
			event.Skip()

	
	####################################################################
	# REFRESH

	def __onPropertyChanged(self, event):
		# schedule refresh changed cells
		if event.propertyName == 'dateStart':
			self.refresh(full=True)
		elif event.propertyName == 'date':
			self.refresh(map(self.__getDateCell, (event.oldValue, event.value)))
		elif event.propertyName == 'selection':
			cells = set(self.__getPeriodCells(event.oldValue))
			cells.symmetric_difference_update(self.__getPeriodCells(event.value))
			self.refresh(cells)


	def refresh(self, cells=(), full=False):
		self.__refreshFull = full
		self.__refreshCells.update(cells)

		if not self.__refreshPending and (self.__refreshFull or self.__refreshCells):
			wx.CallAfter(self._doRefresh)
			self.__refreshPending = True

	
	def _doRefresh(self):
		self.__refreshPending = False
		self.__drawing.draw(wx.ClientDC(self), self.GetClientRect(), cells=None if self.__refreshFull else self.__refreshCells)
		self.__refreshFull = False
		self.__refreshCells.clear()

	def __getDateCell(self, date):
		return self.__drawing.translateDayCell(self.__model._getCell(date))

	def __getPeriodCells(self, period):
		return map(self.__drawing.translateDayCell, self.__model._getCells(period))

	def __onSize(self, evt):
		self.Refresh(False)
		evt.Skip()

	def __onPaint(self, event):
		self.__drawing.draw(wx.PaintDC(self), self.GetClientRect())

	####################################################################

	def hitTest(self, pos):
		"""
		returns ((startDate, endDate), periodType)
			periodType is one of
				day
				week
				month
		"""
		cell = self.__drawing.hitCellTest(pos)
		if cell:
			date = self.__drawing.getDateAt(*cell)
			if date:
				return (date, date), 'day'
			else:
				return self.__drawing.getDatePeriodAt(*cell)
		
	def __onMouse(self, event):
		if event.ButtonDown():
			cell = self.__drawing.hitCellTest(event.GetPosition())
			if cell:
				date = self.__drawing.getDateAt(*cell)
				if date:
					self.__model.setDate(date, event.ShiftDown())
				else:
					# some label clicked
					period, periodType = self.__drawing.getDatePeriodAt(*cell)
					if period:
						if event.ShiftDown():
							self.getModel().addSelection(period)
						else:
							self.getModel().setSelection(period)
				self.__oldDragCell = cell

		if event.Dragging():
			cell = self.__drawing.hitCellTest(event.GetPosition())
			if cell and self.__oldDragCell != cell:
				date = self.__drawing.getDateAt(*cell)
				if date:
					#self.__model.setDate(self.__model._makeInMonth(date), True)
					self.__model.setDate(date, True)
				else:
					period, periodType = self.__drawing.getDatePeriodAt(*cell)
					if period and periodType != 'month':
						self.getModel().addSelection(period)

				self.__oldDragCell = cell
		event.Skip()
			
	def __onMotion(self, event):
		if not event.Dragging():

			try:
				cell = self.__drawing.hitCellTest(event.GetPosition())
			except ValueError:
				pass
			else:
				if cell != self.__lastMotionCell:

					flags = self.__drawing.getCellFlagsAndText(*cell)[0]

					date = self.__drawing.getDateAt(*cell)
					
					text = self.__model.getCellTip(date) if date else ""

					tip = event.GetEventObject().ToolTip
					if text:
						if tip:
							tip.SetTip(text)
							tip.Enable(False)
							tip.Enable(True)
						else:
							tip = event.GetEventObject().ToolTip = wx.ToolTip(text)
					elif tip:
							tip.SetTip("")
							tip.Enable(False)

					self.__lastMotionCell = cell

		event.Skip()

	def getModel(self):
		return self.__model

	def getCellAttributes(self):
		return self.__drawing.getCellAttributes()


def test():

	def oninit(self):
		self.Size = 800, 600
		c = Calendar(self, -1)#, (100, 50), (200, 180))
		b = wx.Button(self, -1, "hello")
		self.SetSizer(wx.BoxSizer(wx.VERTICAL))
		self.GetSizer().Add(c, 1, wx.GROW)
		self.GetSizer().Add(b)

			
	def ondestroy(self):
		pass

	def ontimer(self):
		pass

	from toolib.wx.TestApp import TestApp
	TestApp(oninit, ondestroy, ontimer = ontimer).MainLoop()

if __name__ == '__main__':
	test()
