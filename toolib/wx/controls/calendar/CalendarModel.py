from toolib.event.ListenerList import ListenerList
import datetime

class CalendarModel(object):

	def __init__(self, 
			date=None, 
			getCellFlags = lambda date: (), 
			getCellText = lambda date: str(date.day), 
			getCellTip = lambda date: str(date.day),
		):
		self.__date = None
		self.__date1 = None
		self.__date0 = None

		self.__selection = None
		
		self.listeners = ListenerList()
		self.setDate(date or datetime.date.today())

		self.getCellFlags = getCellFlags
		self.getCellText  = getCellText
		self.getCellTip   = getCellTip


	def setDate(self, date, selecting=False):
		if selecting:
			# do not set date, just set selection end
			self.setSelection((self.getSelectionStart() or self.__date, min(max(date, self.getDateStart()), self.getDateEnd())))
		else:
			oldDate = self.__date
			if date != oldDate:
				self.__date = date
    
				oldDate0 = self.__date0
				oldDate1 = self.__date1
    
				if oldDate is None or oldDate.year != date.year or oldDate.month != date.month:
					self.__date1 = date - datetime.timedelta(date.day-1)
					self.__date0 = self.__date1 - datetime.timedelta(self.__date1.weekday())
    
				self.setSelection(None)
    
				self.listeners.firePropertyChanged(self, 'date', oldValue=oldDate, value=date)
    
				if oldDate0 != self.__date0:
					self.listeners.firePropertyChanged(self, 'dateStart', oldValue=oldDate0, value=self.__date0)
					self.listeners.firePropertyChanged(self, 'dateFirst', oldValue=oldDate1, value=self.__date1)

	
	def getDate(self):
		return self.__date

	
	def getDateFirst(self):
		return self.__date1

	def getDateLast(self):
		y = self.__date1.year + self.__date1.month / 12
		m = (self.__date1.month % 12) + 1
		return datetime.date(y, m, 1) - datetime.timedelta(1)

	
	def getDateStart(self):
		return self.__date0

	def getDateEnd(self):
		return self.getDateAt(5, 6)
	

	def getDateAt(self, row, col):
		return self.__date0 + datetime.timedelta(row * 7 + col)


	def _getCell(self, date):
		day = (date - self.__date0).days
		return day / 7, day % 7

	def _getCells(self, period):
		if period:
			date1, date2 = period
			if date1 > date2:
				date2, date1 = period
			return [(day / 7, day % 7) for day in xrange((date1 - self.__date0).days, (date2 - self.__date0).days + 1)]
		else:
			return ()

	def getWeekAt(self, row):
		date = self.getDateAt(row, 0)
		#if date < self.__date1:
		#	date = self.__date1
		return date.isocalendar()[1]
	
	def incDay(self, day, selecting=False):
		self.setDate(
			((self.getSelectionEnd() or self.__date) if selecting else self.__date) + datetime.timedelta(day), 
			selecting
		)

	def incMonth(self, month):
		absmonth = self.__date.year * 12 + self.__date.month - 1
		absmonth += month
		day = self.__date.day

		for day in xrange(self.__date.day, -1, -1):
			try:
				newDate = datetime.date(absmonth / 12, absmonth % 12 + 1, day)
				break
			except:
				pass

		self.setDate(newDate)

	def isThisMonth(self, date):
		return self.__date1.year == date.year and self.__date1.month == date.month

	def _makeInMonth(self, date):
		return min(max(date, self.getDateFirst()), self.getDateLast())

	#######################################################
	# Selection
	
	def setSelection(self, selection):
		oldSelection = self.__selection
		if oldSelection != selection:
			self.__selection = selection
			#rint "SET SEL:", selection
			self.listeners.firePropertyChanged(self, 'selection', oldValue=oldSelection, value=selection)

	def getSelection(self):
		return self.__selection

	def addSelection(self, selection):
		sel = list(self.getSelection() or ())
		sel.extend(selection)
		sel.sort()
		self.setSelection((sel[0], sel[-1]))

	def isSelected(self, date):
		sel = self.getSelection()
		if sel:
			date1, date2 = sel
			if date1 <= date2:
				return date1 <= date <= date2
			else:
				return date2 <= date <= date1
		else:
			return False

	def getSelectionStart(self):
		if self.__selection:
			return self.__selection[0]

	def getSelectionEnd(self):
		if self.__selection:
			return self.__selection[1]


		


if __name__ == '__main__':
	from Calendar import test
	test()
