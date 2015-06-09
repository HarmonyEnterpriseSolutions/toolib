import datetime
import time
try: _
except NameError: _ = lambda x: x

class DateTimePattern(object):
	"""
	provides formatting/parsing with "" <--> None mapping
	provides user friendly ValueError when fails to parse

	%c - locale datetime
	%x - locale date
	%X - locale time

	TODO: profile, maybe use 're' instead 'in', 'replace'
	"""

	datetime = datetime.datetime

	def __init__(self, format = '%c', datetime = None):
		assert format is not None
		self.__format = None
		self.setFormat(format)
		self.__datetime = datetime or self.datetime

	def getFormat(self):
		return self.__format
	
	def setFormat(self, format):
		if format != self.__format:
			self.__format = format
			# time.strptime does not understand %#H, it raises ValueError: '#' is a bad directive in format
			self.__parseFormat = format.replace('%#', '%')
			self.__extendedFormat = None
			self.__userFormat = None
			self.__javaFormat = None

	def getExtendedFormat(self):
		"""
		reverses strftime to get locale pattern
		"""
		if self.__extendedFormat is None:
			if '%c' in self.__format or '%x' in self.__format or '%X' in self.__format:
				s = datetime.datetime(1978, 04, 06, 23, 27, 51).strftime(self.__format)
				s = s.replace('1978', '%Y')		# YYYY
				s = s.replace('78',   '%y')		# YY
				s = s.replace('04',   '%m')		# month 01-12
				s = s.replace('06',   '%d')		# day 01-31
				s = s.replace('23',   '%H')		# hour 00-23
				s = s.replace('11',   '%I')		# hour 01-12

				for pm in ('PM', 'p.m.', 'nm'):	# (en, qu, af) locale specific
					s = s.replace(pm, '%p')		# PM/AM

				s = s.replace('27',   '%M')		# minute 00-59
				s = s.replace('51',   '%S')		# second 00-61
				s = s.replace('4',   '%#m')		# month 1-12  (no leading zero)
				s = s.replace('6',   '%#d')		# day 1-31    (no leading zero)

				# test2, to detect where is no leading zeros
				s2 = datetime.datetime(2222, 3, 4, 5, 6, 7).strftime(self.__format)

				if not '05' in s2:
					s = s.replace('%H', '%#H')	# hour 0-23   (no leading zero)
					s = s.replace('%I', '%#I')	# hour 1-12   (no leading zero)

				# this code is unreachable but may be reached sometimes
				if not '06' in s2:
					s = s.replace('%M', '%#M')	# minute 0-59 (no leading zero)

				if not '07' in s2:
					s = s.replace('%S', '%#S')	# second 0-61 (no leading zero)

				self.__extendedFormat = s
			else:
				self.__extendedFormat = self.__format
		return self.__extendedFormat

	def hasDate(self):
		"""
		returns True if patern is only for date
		"""
		return (
			'%c'  in self.__format or
			'%x'  in self.__format or
			'%Y'  in self.__format or
			'%y'  in self.__format or
			'%m'  in self.__format or
			'%d'  in self.__format or
			'%#m' in self.__format or
			'%#d' in self.__format
		)

	def hasTime(self):
		"""
		returns True if patern is only for date
		"""
		return (
			'%c'  in self.__format or
			'%X'  in self.__format or
			'%H'  in self.__format or
			'%M'  in self.__format or
			'%S'  in self.__format or
			'%#H' in self.__format or
			'%#M' in self.__format or
			'%#S' in self.__format or
			'%I'  in self.__format or
			'%#I' in self.__format or
			'%p'  in self.__format
		)

	def getUserFormat(self):
		if self.__userFormat is None:
			self.__userFormat = (
				self.getExtendedFormat()
					.replace('%Y',  _('YYYY'))
					.replace('%y',  _('YY'))
					.replace('%m',  _('MM'))
					.replace('%d',  _('DD'))
					.replace('%#m', _('M'))
					.replace('%#d', _('D'))
	
					.replace('%H', _('hh'))
					.replace('%M', _('mm'))
					.replace('%S', _('ss'))

					.replace('%#H', _('h'))
					.replace('%#M', _('m'))
					.replace('%#S', _('s'))

					.replace('%I', _('hh'))
					.replace('%#I', _('h'))
					.replace('%p', _('AM/PM'))
			)
		return self.__userFormat

	def getJavaFormat(self):
		if self.__javaFormat is None:
			self.__javaFormat = (
				self.getExtendedFormat()
					.replace('%Y',  'yyyy')
					.replace('%y',  'yy')
					.replace('%m',  'MM')
					.replace('%d',  'dd')
					.replace('%#m', 'M')
					.replace('%#d', 'd')

					.replace('%H',  'HH')
					.replace('%M',  'mm')
					.replace('%S',  'ss')

					.replace('%#H', 'H')
					.replace('%#M', 'm')
					.replace('%#S', 's')

					.replace('%I',  'hh')
					.replace('%#I', 'h')
					.replace('%p',  'a')
			)
			assert '%' not in self.__javaFormat, 'Java format conversion failed: ' + format
		return self.__javaFormat

	def format(self, value):
		if value is None:
			return ""
		elif hasattr(value, 'strftime'):
			return value.strftime(self.__format)
		elif hasattr(value, 'Format'):
			return value.Format(self.__format)
		else:
			raise ValueError, _('Do not know how to format %s') % value.__class__

	def parse(self, value, datetime=None):
		if value == "":
			return None
		else:
			try:
				return (datetime or self.__datetime)(*time.strptime(value, self.__parseFormat)[:6])
			except ValueError:
				raise ValueError, _("Invalid date: '%s'. Expected format is %s") % (value, self.getUserFormat())

	def __str__(self):
		return self.__format


if __name__ == '__main__':

	def test():
		import locale
		locales = list(set(map(lambda s: s[:2], locale.windows_locale.values())))
		locales.sort()
		for l in locales:
			try:
				locale.setlocale(locale.LC_TIME, l)
			except:
				continue
	
			p = DateTimePattern('%c')

			print "%s: %-30s %-30s %-30s" % (l, p.getExtendedFormat(), p.getUserFormat(), p.getJavaFormat())

			for d in (
				datetime.datetime(1978, 12, 21, 23, 27, 51), 
				datetime.datetime(2222,  3,  4,  5,  6,  7),
			):
				f = d.strftime(p.getFormat())
				xf = d.strftime(p.getExtendedFormat())
				if f != xf:
					print '\t==> error: %s != %s' % (f, xf)

	test()
