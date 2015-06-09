import wx
import wx.calendar
import datetime
import locale
from toolib.util import locales

BORDER = 5
CALENDAR_DELTA_WIDTH = 4
TODAY_BORDER = wx.calendar.CAL_BORDER_NONE
TODAY_BORDER_COLOUR = "blue"
TODAY_BG_COLOUR = wx.Colour(0xD0, 0xD0, 0xD0)


def iterWeekdays(year, month, weekday = 6):
	d = datetime.date(year, month, 1)
	res = d + datetime.timedelta((7 - d.weekday() + weekday) % 7)
	week = datetime.timedelta(7)
	while res.month == d.month:
		yield res
		res = res + week


class CalendarPanel(wx.Panel):
	"""
	Use instead wx.calendar.CalendarCtrl
	pos already set
	MinSize, MaxSize, Size set
	fixed behaviour:
		year selection
		tab traversing

	today selected
	holidays selected
	"""

	def __init__(self, parent, id=-1, date = wx.DefaultDateTime, pos=(BORDER, BORDER), style = wx.calendar.CAL_MONDAY_FIRST, holidays=None): # | wx.calendar.CAL_SHOW_HOLIDAYS
		wx.Panel.__init__(self, parent, -1)
		self.calendarCtrl = wx.calendar.CalendarCtrl(self, id, date, pos, style=style)
		
		self.monthComboBox = None
		self.yearSpinCtrl = None

		# look for month and year controls in children
		for c in self.GetChildren():
			if isinstance(c, wx.ComboBox):
				self.monthComboBox = c
			elif isinstance(c, wx.SpinCtrl):
				self.yearSpinCtrl = c
			
		# selects current date and holidays
		self.calendarCtrl.Bind(wx.calendar.EVT_CALENDAR_MONTH, self.__onCalendarMonth, self.calendarCtrl)
		self.calendarCtrl.Bind(wx.calendar.EVT_CALENDAR_YEAR,  self.__onCalendarMonth, self.calendarCtrl)

		#tips
		self.calendarCtrl.Bind(wx.EVT_MOTION, self.__onMotion, self.calendarCtrl)

		#selection color
		self.calendarCtrl.Bind(wx.EVT_SET_FOCUS, self.__on_set_focus, self.calendarCtrl)
		self.calendarCtrl.Bind(wx.EVT_KILL_FOCUS, self.__on_kill_focus, self.calendarCtrl)

		# fixes focus
		self.calendarCtrl.Bind(wx.EVT_CHAR, self.__onCalendarChar)
		# sets selection on whole text
		self.yearSpinCtrl.Bind(wx.EVT_SET_FOCUS, self.__selectYear)
		self.yearSpinCtrl.Bind(wx.EVT_SPIN,      self.__selectYear)

		size = self.calendarCtrl.GetEffectiveMinSize()

		if wx.Platform == '__WXMSW__':
			# cosmetic fix, year not fits
			self.calendarCtrl.MinSize = (size[0] + CALENDAR_DELTA_WIDTH, size[1])
			self.calendarCtrl.Size = self.calendarCtrl.EffectiveMinSize
		
		size = (size[0] + BORDER * 2 + CALENDAR_DELTA_WIDTH, size[1] + BORDER * 2)

		self.MinSize = size
		self.MaxSize = size
		self.Size = size

		self.__prevHit = None
		self.__onCalendarMonth()	# force show current date
		self.__highlightColours     = self.calendarCtrl.HighlightColourFg, self.calendarCtrl.HighlightColourBg
		#self.__idleHighlightColours = self.calendarCtrl.ForegroundColour,  wx.Colour(0,0,0,0xFF) #, self.calendarCtrl.BackgroundColour
		#self.__idleHighlightColours = self.calendarCtrl.HighlightColourFg, wx.Colour(0x80, 0x80, 0x80)


	def __onCalendarMonth(self, event=None):
		curMonth = self.calendarCtrl.Date.Month + 1   # convert wxDateTime 0-11 => 1-12
		curYear  = self.calendarCtrl.Date.Year
		today = datetime.date.today()

		holidays = set()
		holidays.update([i.day for i in iterWeekdays(curYear, curMonth, 5)])
		holidays.update([i.day for i in iterWeekdays(curYear, curMonth, 6)])
		holidays.update([holiday.day for holiday in locales.getLocale().getHolidays(curYear, curMonth)])
	
 		for day in xrange(1, 32):
			self.__setAttrs(day, day in holidays, day == today.day and curYear == today.year and curMonth == today.month)

		if event:
			event.Skip()

	def __setAttrs(self, day, isHoliday, isToday):
		attr = self.GetAttr(day)
		
		if (isHoliday or isToday) and attr is None:
			attr = wx.calendar.CalendarDateAttr()
			self.SetAttr(day, attr)
		
		if isToday:
			attr.Border = TODAY_BORDER
			attr.SetBackgroundColour(TODAY_BG_COLOUR)
			attr.SetBorderColour(TODAY_BORDER_COLOUR)
		elif attr is not None:
			attr.SetBorder(wx.calendar.CAL_BORDER_NONE)
			attr.SetBackgroundColour(None)
			attr.SetBorderColour(None)
		
		if attr is not None:
			attr.SetHoliday(isHoliday)

	def __onMotion(self, event):
		hit, date = self.calendarCtrl.HitTest(event.GetPosition())[:2]
		if self.__prevHit != (hit, date):
			self.__prevHit = (hit, date)
			if hit == wx.calendar.CAL_HITTEST_DAY:
				tip = u'\n'.join([h.name for h in locales.getLocale().getHolidays(date.Year, date.Month+1, date.Day)])
			else:
				tip = ""
			if self.calendarCtrl.ToolTip:
				self.calendarCtrl.ToolTip.SetTip(tip)
			elif tip:
				self.calendarCtrl.ToolTip = wx.ToolTip(tip)
		event.Skip()

	def __onCalendarChar(self, event):
		code = event.GetKeyCode()
		if event.GetKeyCode() == wx.WXK_TAB and not event.MetaDown() and not event.ControlDown() and not event.AltDown():
			if event.ShiftDown():
				self.monthComboBox.SetFocus()
			else:
				self.yearSpinCtrl.SetFocus()
		else:
			event.Skip()

	def __selectYear(self, event):
		self.yearSpinCtrl.SetSelection(-1,-1)
		event.Skip()

	def __on_set_focus(self, event):
		# simulates cursor return
		self.calendarCtrl.SetHighlightColours(*self.__highlightColours)
		self.calendarCtrl.Refresh()
		event.Skip()

	def __on_kill_focus(self, event):
		# simulates cursor away
		fg = bg = None

		attr = self.calendarCtrl.GetAttr(self.calendarCtrl.Date.Day)
		
		if attr:

			if attr.HasTextColour():
				fg = attr.TextColour
			
			if attr.HasBackgroundColour():
				bg = attr.BackgroundColour
		
			if attr.IsHoliday():
				fg = fg or self.calendarCtrl.HolidayColourFg
				bg = bg or self.calendarCtrl.HolidayColourBg

		fg = fg or self.calendarCtrl.ForegroundColour
		bg = bg or self.calendarCtrl.BackgroundColour
			
		# like cursor is gone
		self.calendarCtrl.SetHighlightColours(fg, bg)
		self.calendarCtrl.Refresh()
		event.Skip()

	def SetDate(self, date):
		oldDate = self.calendarCtrl.GetDate()
		self.calendarCtrl.SetDate(date)

		# workaround BUG: event EVT_CALENDAR_MONTH and EVT_CALENDAR_YEAR not goes when SetDate
		if oldDate.GetYear() != date.GetYear() or oldDate.GetMonth() != date.GetMonth():
			self.__onCalendarMonth()

	def __getattr__(self, name):
		return getattr(self.calendarCtrl, name)


if __name__ == '__main__':
	from toolib import startup
	startup.startup()
	import DateControl
	DateControl.test()
		
