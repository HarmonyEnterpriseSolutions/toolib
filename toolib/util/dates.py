import datetime


PERIODS = set(('day', 'week', 'month', 'quarter', 'year'))


class Date(datetime.date):
	"""
	Same as datetime.date but
		- have methods add, startof, endof
		__add__ and __sub__ can also accept str (e.g. "2 month") and int
	"""

	@classmethod
	def from_date(cls, date):
		return Date(date.year, date.month, date.day)

	
	date = property(lambda self: datetime.date(self.year, self.month, self.day))


	def __add__(self, interval):
		"""
		interval can be str 
		"1 day"
		"2 week"
		"-1 month"
		"quarter"
		"37 year"

		interval can be int and float, this means days
		"""
		if isinstance(interval, basestring):
			return self.add(*_split_interval(interval))

		if isinstance(interval, int):
			interval = datetime.timedelta(interval)

		return Date.from_date(super(Date, self).__add__(interval))


	def __sub__(self, interval):

		if isinstance(interval, basestring):
			n, period = _split_interval(interval)
			return self.add(-n, period)

		if isinstance(interval, int):
			interval = datetime.timedelta(interval)

		return Date.from_date(super(Date, self).__sub__(interval))



	def add(self, n, period='day'):
		"""
		adds n periods to date
		n can be negative
		period:
			day
			month
			week
			quarter
			year
		"""
		return getattr(self, '_add_' + period)(n)
	

	def startof(self, period):
		"""
		Returns Date, first day of period
		period:
			day (self)
			week (last monday)
			month
			quarter
			year
		"""
		return getattr(self, '_startof_' + period)()


	def endof(self, period):
		"""
		Returns Date, last day of period
		period:
			day (self)
			week (next sunday)
			month
			quarter
			year
		"""
		return (self + period).startof(period) - 1


	def _add_day(self, n): return self + datetime.timedelta(n)
	def _add_week(self, n): return self + datetime.timedelta(n*7)
	
	def _add_month(self, n):
		m = self.month + n - 1
		return Date(
			self.year + m // 12, 
			m % 12 + 1, 
			self.day
		)

	def _add_quarter(self, n): return self._add_month(n * 3)
	def _add_year(self, n): return self._add_month(n * 12)

	def _startof_day(self): return self
	def _startof_week(self): return self - self.weekday()
	def _startof_month(self): return Date(self.year, self.month, 1)
	def _startof_quarter(self):	return Date(self.year, (self.month-1) // 3 * 3 + 1, 1)
	def _startof_year(self): return Date(self.year, 1, 1)


def today():
	return Date.today()


def _split_interval(interval):
	
	try:
		n, period = interval.rsplit(' ', 1)
	except ValueError:
		n = 1
		period = interval
	else:
		n = int(n)

	if not period in PERIODS:
		raise ValueError, period
	
	return n, period



if __name__ == '__main__':
	print today() - "1 day"
	print today() - "1 week"
	print today() - "1 month"
	print today() - "1 quarter"
	print today() - "1 year"
	print
	print today().startof('week')
	print today().startof('month')
	print today().startof('quarter')
	print today().startof('year')
	print
	print today().endof('week')
	print today().endof('month')
	print today().endof('quarter')
	print today().endof('year')
