"""
TODO: hide on escape
"""
import wx
import wx.calendar
from datetime						import datetime
from PopupControl					import PopupControl
from toolib.util.DateTimePattern	import DateTimePattern
from CalendarPanel					import CalendarPanel

try: _
except NameError: _ = lambda x: x

__all__ = ['DateControl']


class DateControl(PopupControl):
	"""
	datetime: datetime constructor
	          must accept year, month, day, h, m, s
	          default is datetime.datetime

	format:
		%c - locale datetime
		%x - locale date (default)
		%X - locale time
	"""
	datetime = datetime

	def __init__(self, *args, **kwargs):
		format = kwargs.pop('format', '%x')
		#kwargs['noneButton'] = True
		PopupControl.__init__(self, *args, **kwargs)
		self._pattern = DateTimePattern(format, datetime=self.datetime)

	def CreatePopupWindow(self, title, style):
		return PopupControl.CreatePopupWindow(self, title, style & ~wx.RESIZE_BORDER & ~wx.CAPTION)

	def CreatePopupContent(self, parent, id):
		c = CalendarPanel(parent)
		c.Bind(wx.calendar.EVT_CALENDAR, self.OnCalendar)
		return c

	def getDateTime(self):
		"""
		returns datetime or None empty string
		throws ValueError
		"""
		return self._pattern.parse(self.GetValue() or "")

	def setDateTime(self, value):
		self.SetValue(self._pattern.format(value))

	def	getPattern(self):
		return self._pattern

	# Method called when a day is selected in the calendar
	def OnCalendar(self, evt):
		date = self.GetPopupContent().GetDate()

		# preserve time if was entered
		oldDate = self.getDateTime()
		if oldDate:
			date.Hour   = oldDate.hour
			date.Minute = oldDate.minute
			date.Second = oldDate.second
			date.Millisecond = oldDate.microsecond / 1000

		self.SetValue(self._pattern.format(date))
		# workaround: in gfd selection was broken after
		wx.CallAfter(self.SetSelection, -1, -1)
		self.PopDown()
		evt.Skip()

	def FormatContent(self):
		"""
		Method overridden from PopupControl
		This method is called just before the popup is displayed
		"""
		# seems that wx.DateTime gets broken after parsing incorect date
		# do not use it for parsing
		try:
			d = self.getDateTime() 
		except ValueError:
			d = None

		if d:
			date = wx.DateTime()
			date.Set(d.day, d.month-1, d.year)
		else:
			date = wx.DateTime_Today()
		
		self.GetPopupContent().SetDate(date)

	# deprecated stuff
	try:
		import mx.DateTime
		
		def getDate(self):
			"""
			deprecated
			"""
			try:
				return self._pattern.parse(self.GetValue() or "", mx.DateTime.DateTime)
			except ValueError:
				return None

		setDate = setDateTime
	except ImportError:
		pass



def test():
	import locale
	locale.setlocale(locale.LC_ALL, '')

	def oninit(self):
		self.panel = wx.Panel(self, -1)
		self.panel.SetSizer(wx.BoxSizer(wx.VERTICAL))

		self.d = DateControl(
			self.panel, 
			popupModal = False,
			#format='%c'
		)

		self.t = wx.TextCtrl(
			self.panel, 
		)

		self.d.EnableButton(False)
		#self.d.EnableTextControl(False)
		self.d.Enable(False)
		self.d.Enable(True)

		self.panel.GetSizer().Add(self.d, 0, wx.GROW)
		self.panel.GetSizer().Add(self.t, 0, wx.GROW)

		from toolib.wx.debug.dump import dumpWindowSizes
		dumpWindowSizes(self.d)
		dumpWindowSizes(self.t)
			
	def ondestroy(self):
		pass

	def ontimer(self):
		#self.d.GetParent().Hide()
		#self.d.SetValue("")
		#self.d.WriteText("1")
		#self.d.GetParent().Show()
		#self.d.SetValue("1.02.2007")
		pass

	from toolib.wx.TestApp import TestApp
	TestApp(oninit, ondestroy, ontimer = ontimer).MainLoop()

if __name__ == '__main__':
	test()
