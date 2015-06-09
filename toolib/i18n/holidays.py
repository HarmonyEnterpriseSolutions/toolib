from config import HOLIDAYS
import datetime

class Holiday(object):

	def __init__(self, month, day, name, firstYear=None, lastYear=None):
		self.month = month
		self.day   = day
		self.name  = name
		self.firstYear = firstYear
		self.lastYear = lastYear
		
	def isActual(self, year, month=None, day=None):
		"""
		TODO: optimize query
		"""
		return (self.firstYear is None or year >= self.firstYear) \
			and (self.lastYear  is None or year <= self.lastYear) \
			and (month          is None or self.month == month  ) \
			and (day            is None or self.day   == day)


_locales = {}

class Holidays(object):

	def __init__(self, country):
		"""
		country is 'UA', 'RU'
		"""
		self.country = country
		self.holidays = [Holiday(*args) for args in HOLIDAYS.get(country, ())]

	def getHolidays(self, year, month=None, day=None):
		return [holiday for holiday in self.holidays if holiday.isActual(year, month, day)]

	def skipWorkingDays(self, date, count, weekends=(5,6), move_holidays=True):
		"""
		Skip count of working days
		TODO: optimize loop
		"""
		if count:
			if count < 0:
				delta = datetime.timedelta(-1)
				count = -count
			else:
				delta = datetime.timedelta(1)

			while count > 0:
				date += delta
				count -= 1

				is_weekend = date.weekday() in weekends	

				if is_weekend:
					count += 1

				if not is_weekend or is_weekend and move_holidays:
					count += len(self.getHolidays(date.year, date.month, date.day))


			return date
		else:
			return date
		


if __name__ == '__main__':
	#from toolib import startup
	#startup.startup()
	h = Holidays('UA')
	def test(date):
		date2 = h.skipWorkingDays(date, -3)
		print date, date2, date - date2
	
	for i in xrange(20):
		test(datetime.date(2011, 01, 21) - datetime.timedelta(i))

