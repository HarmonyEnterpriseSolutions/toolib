# -*- coding: cp1251 -*-
import wx
import datetime
from GridDrawing import GridDrawing
from CellAttributes import CellAttributes

try:	_
except:	_ = lambda x: x


class CalendarDrawing(GridDrawing):
	
	def __init__(self, model, cellAttributesDict):

		super(CalendarDrawing, self).__init__(7, 8, cellAttributesDict)

		self.__model = model
		self.__headerRow = 0
		self.__weekCol = 0
		self.__dayBaseRow = 1
		self.__dayBaseCol = 1
		self.__dayNames = (_("Mo"), _("Tu"), _("We"), _("Th"), _("Fr"), _("Sa"), _("Su"))
		self.__focus = False

	def setFocus(self, focus):
		self.__focus = focus

	def translateDayCell(self, cell):
		return cell[0] + self.__dayBaseRow, cell[1] + self.__dayBaseCol

	def getDateAt(self, row, col):
		row -= self.__dayBaseRow
		col -= self.__dayBaseCol
		if row >= 0 and row < 6 and col >= 0 and col < 7:
			return self.__model.getDateAt(row, col)
	
	def getDatePeriodAt(self, row, col):
		if col == self.__weekCol:
			if row == self.__headerRow:
				return (self.__model.getDateFirst(), self.__model.getDateLast()), 'month'
			else:
				return (self.getDateAt(row, self.__dayBaseCol), self.getDateAt(row, self.__dayBaseCol+6)), 'week'
		return None, None
	
	def getCellFlagsAndText(self, row, col):
		flags = []

		if row == self.__headerRow:
			flags.append('header')
			if col == self.__weekCol:
				flags.append('week')
				text = _('Week #')
			else:
				text = self.__dayNames[col - self.__dayBaseCol]
		else:
			if col == self.__weekCol:
				flags.append('week')
				text = str(self.__model.getWeekAt(row - self.__dayBaseRow))
			else:
				date = self.__model.getDateAt(row - self.__dayBaseRow, col - self.__dayBaseCol)
				
				flags.extend(self.__model.getCellFlags(date))

				if date == datetime.date.today():
					flags.append('today')

				if date.weekday() >= 5:
					flags.append('holiday')

				if not self.__model.isThisMonth(date):
					flags.append('otherMonth')

				if self.__model.getDate() == date:
					flags.append('currentDay' if self.__focus else 'currentDayUnfocused')

				if self.__model.isSelected(date):
					flags.append('selectedDay' if self.__focus else 'selectedDayUnfocused')

				text = self.__model.getCellText(date)

		return flags, text


	def hitDateTest(self, pos):
		cell = self.hitCellTest(pos)
		if cell:
			row = cell[0] - self.__dayBaseRow
			col = cell[1] - self.__dayBaseCol
			if row >= 0 and col >=0 and row < 6 and col < 7:
				return self.__model.getDateAt(row, col)


if __name__ == '__main__':
	from Calendar import test
	test()
