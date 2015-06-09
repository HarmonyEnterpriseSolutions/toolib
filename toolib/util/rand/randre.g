"""
	generate(<pattern>)
		
		returns random string

	compile(<pattern>)
		
		returns RandGenerator instance

	RandGenerator.rand() return random string

	pattern format
		pattern ::= item*
		item ::= ( letter | range ) [ {<count>} ]
		letter ::= '\'<special-char> | !<special-char>
		special-char ::= '[' | ']' | '{' | '}' | '-' | '\'
		range ::= '\d' | '[' (letter | letter '-' letter | '\d')* ']'

	Examples:
		ABC		- as is
		[A-Z]	- any character from A till Z
		[AZ]	- A or Z
		[AK-MZ]	- any of A, K, L, M or Z
		[A\d]	- any of A, 0 to 9
		\d		- same as [\d]

		\[\]\{\}\-\\	- []{}-\

		{n}		- repeat previous item n times

	TODO:
		add grouping '(' ')'
		add variant '|'
"""

__all__ = [
	'generate',
	'compile',
	'RandGenerator',
]

from base					import randrange, randbelow
from toolib.util.strings	import srange

class RandGenerator(object):
	def rand(self):
		raise NotImplementedError, 'abstract'

class RangeGenerator(RandGenerator):
	def __init__(self, a, b):
		self._start = ord(a)
		self._stop = ord(b) + 1
	def rand(self):
		return chr(randrange(self._start, self._stop))
	def __str__(self):
		return '[%s-%s]' % (chr(self._start), chr(self._stop-1))

class ItemGenerator(RandGenerator):
	def __init__(self, s):
		assert s
		self._s = s
		self._len = len(s)
	def rand(self):
		return self._s[randbelow(self._len)]
	def __str__(self):
		return '[%s]' % self._s

class SequenceGenerator(RandGenerator):
	def __init__(self):
		self._l = []
		
	def rand(self):
		return ''.join([i.rand() for i in self._l])

	def append(self, item):
		if (self._l 
			and isinstance(item, Constant) 
			and isinstance(self._l[-1], Constant)
			):
			# merge constant (optimization)
			self._l[-1].merge(item)
		else:
			self._l.append(item)

	def __str__(self):
		return ''.join(map(str, self._l))

class Repeater(RandGenerator):
	def __init__(self, generator, count):
		self._generator = generator
		self._count = count
	def rand(self):
		return ''.join([self._generator.rand() for i in xrange(self._count)])
	def __str__(self):
		return '%s{%s}' % (str(self._generator), self._count)

class Constant(RandGenerator):
	def __init__(self, s):
		self._value = s
	def merge(self, constant):
		self._value += constant.rand()
	def rand(self):
		return self._value
	def __str__(self):
		return self._value 

class Appender(object):

	def __init__(self, s):
		self._s = s

	def appendTo(self, buffer):
		return buffer + self._s

class Prolongator(Appender):
	
	def appendTo(self, buffer):
		assert len(buffer) > 0, 'Prolongator called with empty buffer'
		return buffer[:-1] + srange(buffer[-1], self._s)

%%

parser RegenGrammar:

	token CHAR:				r'[^\[\]\{\}\-\\]|\\([^\w\d])'
	token ANYDIGIT:			r'\\d'
	token NUMBER:			r'\d+'

	rule char:
		CHAR			{{ return CHAR[-1] }}

	rule setitem:
		ANYDIGIT		{{ return Appender(srange('0', '9')) }}
		| char			{{ return Appender(char) }}
		| r'\-' char	{{ return Prolongator(char) }}

	rule set:
		r'\['			{{ s = '' }}
		(
		setitem			{{ s = setitem.appendTo(s) }}
		| r'\]'			{{ return ItemGenerator(s) }}
		)*

	rule item:
		(
		set				{{ g = set }}
		| ANYDIGIT 		{{ g = RangeGenerator('0', '9') }}
		| char			{{ g = Constant(char) }}
		)
		(
		r'\{'
		NUMBER			{{ g = Repeater(g, int(NUMBER)) }}
		r'\}'
		|)				{{ return g }}

	rule generate:
						{{ l = [] }}
		(
		item			{{ l.append(item.rand()) }}
		| '$'			{{ return ''.join(l) }}
		)*

	rule compile:
						{{ g = SequenceGenerator() }}
		(
		item			{{ g.append(item) }}
		| '$'			{{ return g }}
		)*
		

%%
def generate(pattern):
	return parse('generate', pattern)

def compile(pattern):
	return parse('compile', pattern)
