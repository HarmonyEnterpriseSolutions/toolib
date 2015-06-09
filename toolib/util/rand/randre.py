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


# Begin -- grammar generated by Yapps
import re
import toolib.text.yapps.yappsrt as yappsrt

class RegenGrammarScanner(yappsrt.Scanner):
    patterns = [
        ("'$'", re.compile('$')),
        ("r'\\}'", re.compile('\\}')),
        ("r'\\{'", re.compile('\\{')),
        ("r'\\]'", re.compile('\\]')),
        ("r'\\['", re.compile('\\[')),
        ("r'\\-'", re.compile('\\-')),
        ('CHAR', re.compile('[^\\[\\]\\{\\}\\-\\\\]|\\\\([^\\w\\d])')),
        ('ANYDIGIT', re.compile('\\\\d')),
        ('NUMBER', re.compile('\\d+')),
    ]
    def __init__(self, str):
        yappsrt.Scanner.__init__(self,None,[],str)

class RegenGrammar(yappsrt.Parser):
    Context = yappsrt.Context
    def char(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'char', [])
        CHAR = self._scan('CHAR')
        return CHAR[-1]

    def setitem(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'setitem', [])
        _token = self._peek('ANYDIGIT', 'CHAR', "r'\\-'")
        if _token == 'ANYDIGIT':
            ANYDIGIT = self._scan('ANYDIGIT')
            return Appender(srange('0', '9'))
        elif _token == 'CHAR':
            char = self.char(_context)
            return Appender(char)
        else: # == "r'\\-'"
            self._scan("r'\\-'")
            char = self.char(_context)
            return Prolongator(char)

    def set(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'set', [])
        self._scan("r'\\['")
        s = ''
        while self._peek('ANYDIGIT', 'CHAR', "r'\\-'", "r'\\]'", "r'\\{'", "r'\\['", "'$'") not in ["r'\\{'", "r'\\['", "'$'"]:
            _token = self._peek('ANYDIGIT', 'CHAR', "r'\\-'", "r'\\]'")
            if _token != "r'\\]'":
                setitem = self.setitem(_context)
                s = setitem.appendTo(s)
            else: # == "r'\\]'"
                self._scan("r'\\]'")
                return ItemGenerator(s)
        if self._peek() not in ['ANYDIGIT', 'CHAR', "r'\\-'", "r'\\]'", "r'\\{'", "r'\\['", "'$'"]:
            raise yappsrt.SyntaxError(self._scanner, charpos=self._scanner.get_prev_char_pos(), context=_context, msg='Need one of ' + ', '.join(['ANYDIGIT', 'CHAR', "r'\\-'", "r'\\]'", "r'\\{'", "r'\\['", "'$'"]))

    def item(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'item', [])
        _token = self._peek("r'\\['", 'ANYDIGIT', 'CHAR')
        if _token == "r'\\['":
            set = self.set(_context)
            g = set
        elif _token == 'ANYDIGIT':
            ANYDIGIT = self._scan('ANYDIGIT')
            g = RangeGenerator('0', '9')
        else: # == 'CHAR'
            char = self.char(_context)
            g = Constant(char)
        _token = self._peek("r'\\{'", "r'\\['", 'ANYDIGIT', 'CHAR', "'$'")
        if _token == "r'\\{'":
            self._scan("r'\\{'")
            NUMBER = self._scan('NUMBER')
            g = Repeater(g, int(NUMBER))
            self._scan("r'\\}'")
        else: # in ["r'\\['", 'ANYDIGIT', 'CHAR', "'$'"]
            pass
        return g

    def generate(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'generate', [])
        l = []
        while 1:
            _token = self._peek("r'\\['", 'ANYDIGIT', 'CHAR', "'$'")
            if _token != "'$'":
                item = self.item(_context)
                l.append(item.rand())
            else: # == "'$'"
                self._scan("'$'")
                return ''.join(l)
        if self._peek() not in ["r'\\['", 'ANYDIGIT', 'CHAR', "'$'"]:
            raise yappsrt.SyntaxError(self._scanner, charpos=self._scanner.get_prev_char_pos(), context=_context, msg='Need one of ' + ', '.join(["r'\\['", 'ANYDIGIT', 'CHAR', "'$'"]))

    def compile(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'compile', [])
        g = SequenceGenerator()
        while 1:
            _token = self._peek("r'\\['", 'ANYDIGIT', 'CHAR', "'$'")
            if _token != "'$'":
                item = self.item(_context)
                g.append(item)
            else: # == "'$'"
                self._scan("'$'")
                return g
        if self._peek() not in ["r'\\['", 'ANYDIGIT', 'CHAR', "'$'"]:
            raise yappsrt.SyntaxError(self._scanner, charpos=self._scanner.get_prev_char_pos(), context=_context, msg='Need one of ' + ', '.join(["r'\\['", 'ANYDIGIT', 'CHAR', "'$'"]))


def parse(rule, text):
    P = RegenGrammar(RegenGrammarScanner(text))
    return yappsrt.wrap_error_reporter(P, rule)

# End -- grammar generated by Yapps


def generate(pattern):
	return parse('generate', pattern)

def compile(pattern):
	return parse('compile', pattern)