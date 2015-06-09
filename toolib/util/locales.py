# -*- coding: Cp1251 -*-

import locale

HOLIDAYS = {
	'Ukrainian_Ukraine' : (
		( 1,  1,	u"Новий рік"),
		( 1,  7,	u"Різдво Христове"),
		( 3,  8,	u"Міжнародний Жіночий День", 1966),
		( 5,  1,	u"День Праці"),
		( 5,  2,	u"День Праці"),
		( 5,  9,	u"День Перемоги", 1945),
		( 6, 15,	u"Трійця"),
		( 6, 28,	u"День Конституції", 1997),
		( 8, 24,	u"День Незалежності",  1991),
	),
	'Russian_Russia' : (
		( 1,  1,	u"Новый год"),
		( 1,  7,	u"Православное Рождество"),
		( 2, 23,	u"День Защитника Отечества", 2002),
		( 3,  8,	u"Международный Женский День", 1966),
		( 5,  1,	u"Праздника весны и труда"),
		( 5,  9,	u"День Победы", 1945),
		( 6, 12,	u"День России", 1992),
		(11,  4,	u"День народного единства", 2005),
	),
}

HOLIDAYS['uk_UA'] = HOLIDAYS['Ukrainian_Ukraine']
HOLIDAYS['ru_RU'] = HOLIDAYS['Russian_Russia']

class Holiday(object):

	def __init__(self, month, day, name, firstYear=None, lastYear=None):
		self.month = month
		self.day   = day
		self.name  = name
		self.firstYear = firstYear
		self.lastYear = lastYear
		
	def isActual(self, year, month=None, day=None):
		return (self.firstYear is None or year >= self.firstYear) \
			and (self.lastYear  is None or year <= self.lastYear) \
			and (month          is None or self.month == month  ) \
			and (day            is None or self.day   == day)

	def __str__(self):
		return self.name

	def __repr__(self):
		return self.name

_locales = {}

class Locale(object):

	def __init__(self, name, encoding):
		self.name = name
		self.encoding = encoding
		self.holidays = [Holiday(*args) for args in HOLIDAYS.get(name, ())]

	def getHolidays(self, year, month=None, day=None):
		return [holiday for holiday in self.holidays if holiday.isActual(year, month, day)]

def getLocale(pyLocale=None):
	if pyLocale is None:
		pyLocale = locale.getlocale()

	l = _locales.get(pyLocale)
	if l is None:
		_locales[pyLocale] = l = Locale(*pyLocale)
	return l


if __name__ == '__main__':
	from toolib import startup
	startup.startup()
	locale.setlocale(locale.LC_ALL, '')
	print getLocale().getHolidays(2008, 1)
