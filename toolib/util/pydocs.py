from toolib.util import strings
import lang

class AttrSignature(object):
	
	def __init__(self, sig):
		
		try:
			sig, default = strings.splitEx(sig, '=')
			self.default = default.strip()
		except ValueError:
			# no default
			self.default = None

		sig = sig.strip()

		try:
			type, name = sig.rsplit(' ', 1)
			self.type = type.strip()
			self.name = name.strip()
		except ValueError:
			self.name = sig.strip()
			self.type = None

	def __str__(self):
		return "%s %s = %s" % (self.type, self.name, self.default)

	def isPositional(self):
		return self.default is None

	def isNamed(self):
		return self.default is not None

	def __str__(self):
		return ' '.join(filter(None, (self.type, self.name, lang.iif(self.default, '='), self.default)))

class FunctionSignature(object):

	def __init__(self, doc):
		try:
			self.name, self.sig, self.doc = strings.splitParentheses(doc)
			self.name = self.name.strip()
		except ValueError:
			self.name = None
			self.sig  = None
			self.doc  = doc

		if self.sig:
			self.attributes = map(AttrSignature, strings.splitEx(self.sig, ','))
		else:
			if self.sig is None:
				self.attributes = None
			else:
				self.attributes = []

		if self.attributes is not None:
			self.positionalAttrs = filter(AttrSignature.isPositional, self.attributes)
			self.namedAttrs      = filter(AttrSignature.isNamed,      self.attributes)
		else:
			self.positionalAttrs = None
			self.namedAttrs = None

		for i in xrange(len(self.positionalAttrs or ())):
			assert self.attributes[i].isPositional(), "named before positional"
			
	def __nonzero__(self):
		return self.attributes is not None


if __name__ == '__main__':
	test = """
	Create(self, Window parent, int id=-1, String label=EmptyString,
		Point pos=DefaultPosition, Size size=DefaultSize,
		wxArrayString choices=wxPyEmptyStringArray,
		int majorDimension=0, long style=RA_HORIZONTAL,
		Validator validator=DefaultValidator,
		String name=RadioBoxNameStr) -> bool
	Creates function bla bla bla
	"""

	s = FunctionSignature(test)
	if s:
		print map(str, s.positionalAttrs)
		print map(str, s.namedAttrs)
