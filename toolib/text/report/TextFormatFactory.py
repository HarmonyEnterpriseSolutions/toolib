import re

#(?!%)

REC_FIELD = re.compile("""
%
(?:
	\(
	(?P<field>
		[^\:\)]+
	)?
	(?P<converters>
		\:
		[^\)]*
	)?
	\)
)?
(?P<percent_format>[-#0-9 +*.hlL]*?[eEfFgGdiouxXcrs%])
""", re.VERBOSE)

REC_CONVERTER = re.compile("""
\:
(?P<name>\w+)
(?:
	\{
		\s*
		(?P<args>[^\}]*)
		\s*
	\}
)?
""", re.VERBOSE)


class YieldText(Exception):
	"""
	converter can throw it to return value immediately
	"""
	pass

class TextFormatField(object):
	"""
	This flyweight object passed to converter to make context
	"""

	def __init__(self, textFormat):
		self._textFormat = textFormat

	def init(self, name):
		self._name = name

	def getTextFormat(self):
		return self._textFormat

	def getName(self):
		return self._name

	def yieldText(self, text):
		raise YieldText(text)

class TextFormat(object):

	def __init__(self, factory, converters, format):
		self._converters  = converters
		self._format = format
		self._factory = factory
		self.__textFormatField = None

	def getFactory(self):
		return self._factory

	def format(self, values=None):
		"""
		works like %
		but added date formatting

		${@<expression>@|<field>[:<converter>[:<comma-separated-converter-args>]]}

		TextFormatFactory().newInstance("Date is %(x:strftime:%d.%m.%Y)s").format(datetime.date(2000, 11, 22))
		-> Date is 22.11.2000
		"""
		values = values or {}
		def subst(m):
			try:

				d = m.groupdict()
    
				field = d['field']
				if field is not None:
					value = values.get(field, NotImplemented)
				else:
					value = NotImplemented
				
				converters = d['converters']
				for converter, args in REC_CONVERTER.findall(m.groupdict()['converters'] or ''):
    
					if converter in self._converters:
						if args:
							args = eval(''.join(("(", args, ",)")), {}, {})
						else:
							args = ()

						if self.__textFormatField is None:
							self.__textFormatField = TextFormatField(self)
						self.__textFormatField._field = field
						
						# convert value
						value = self._converters[converter](self.__textFormatField, value, *args)
					else:
						raise NameError, converter
    			
				return ("%(value)" + d['percent_format']) % {'value' : value}

			except YieldText, e:
				return e[0]

			except Exception, e:
				d['ec'] = e.__class__.__name__
				d['e']  = e
				#raise
				return "%%(%(field)s%(converters)s!%(ec)s: %(e)s)%(percent_format)s" % d

		return REC_FIELD.sub(subst, self._format)


	def getFieldNames(self):
		"""
		returns list of fields, excluding evaluated fields
		"""
		return [f for f in (m.groupdict()['field'] for m in REC_FIELD.finditer(self._format)) if f is not None]


class TextFormatFactory(object):

	def __init__(self, converters={}):
		self._converters  = converters

	def newInstance(self, format):
		return TextFormat(self, self._converters, format)
	
	def format(self, format, values=None):
		"""
		shortcut to use factory as formatter
		"""
		return self.newInstance(format).format(values)


if __name__ == '__main__':
	import locale
	locale.setlocale(locale.LC_ALL, '')
	import datetime
	import decimal
		
	from config import TEXT_FORMAT_FACTORY_CONFIG
	f = TextFormatFactory(**TEXT_FORMAT_FACTORY_CONFIG)

	def test(format, value=NotImplemented):
		text = f.format(format, {'x' : value })
		print "%-30s %-20s %s" % (format, repr(value) if value is not NotImplemented else '', text)

	vdate = datetime.date(2000, 11, 22)
	vdatetime = datetime.datetime(2000, 11, 22, 22, 33, 44)
	vfloat = 123456789.4567
	vdecimal = decimal.Decimal('123456789.4567')

	test("%(x)s"                       , "Test value")
	print
	test("%(x:date)s"                  , vdate)
	test("%(x:date)s"                  , vdatetime)
	test("%(x:datetime)s"              , vdatetime)
	test("%(x:time)s"                  , vdatetime)
	print
	test("%(x:date)s" 				   , None)
	test("%(x:date)s"                  , )
	print
	test("%(x:blanknull:date)s"        , None)
	print
	test("%(:today:date{'%d!%m!%Y'})s", )
	test("%(:now:datetime)s"          , )
	print
	test("%(x:decimal)s"               , vfloat)
	test("%(x:decimal{3,False})s"      , vfloat)
	test("%(x:decimal{3,True})s"       , vfloat)
	print
	test("%(x:decimal)s"               , vdecimal)
	test("%(x:decimal{3,False})s"      , vdecimal)
	test("%(x:decimal{3,True})s"       , vdecimal)
	print
	test("%(x:zuzba)s"                   , )
	test("%(x:date{=zuzba})s"       , )
	test("%(x:date{1/0})s"          , )
	test("%(x:date{zuzba})s"        , )
	test("this is %% sign"          , )
	test("%(x:iif{'true','false'})s", 1)
	test("%(x:iif{'true'}:blanknull)s", 0)
