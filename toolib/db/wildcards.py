#-*- coding: cp1251 -*-
"""
seems to be similar
	select * from spr_prod where prod_name_short ILIKE '%Canon%' OR prod_name_short ILIKE '%Epson%';
	select * from spr_prod where upper(prod_name_short) SIMILAR TO UPPER('%Canon%|%Epson%');
	select * from spr_prod where prod_name_short SIMILAR TO '%(C|c)(A|a)(N|n)(O|o)(N|n)%|%(E|e)(P|p)(S|s)(O|o)(N|n)%';
	select * from spr_prod where prod_name_short ~* 'Canon|Epson';
"""

COMMANDS_WILDCARD = '*?|'
COMMANDS_LIKE     = '%_'
COMMANDS_SIMILAR  = '%_|*+()[]'

def convertPattern(p, inCommands, outCommands, inQuote, outQuote):

	#rint 1, p
	
	# temporary replace self quotes
	p = p.replace(inQuote * 2, '\0')

	# temporary replace input qouted commands to unused char(0), char(1), ...
	for i, char in enumerate(inCommands):
		p = p.replace(inQuote + char, chr(1+i))

	#rint 1.1, p

	# ? replace quotes left to doublequotes
	p = p.replace(inQuote, inQuote * 2)

	#rint 1.2, p
	
	n = len(inCommands) + 1

	# temporary replace input commands to unused char(n), char(n+1), ...
	for i, char in enumerate(inCommands):
		p = p.replace(char, chr(n + i))

	#rint 2, p

	# escape all output quoted characters
	for char in outCommands:
		p = p.replace(char, outQuote + char)

	#rint 3, p

	# translate commands
	for i in xrange(min(len(inCommands), len(outCommands))):
		p = p.replace(chr(n+i), outCommands[i])

	#rint 4, p

	# restore input quoted characters
	for i, char in enumerate(inCommands):
		p = p.replace(chr(1+i), outQuote + char if char in outCommands else char)

	# restore self quotes
	p = p.replace('\0', outQuote * 2)

	#rint 5, p

	return p

def makeCaseInsensitivePattern(char):
	u = char.upper()
	l = char.lower()
	if u != l:
		return '(%s|%s)' % (u, l)
	else:
		return char

def convertWildcardToSimilar(pattern, search=True):
	"""
	Create case insesnsive pattern to use with SQL 99 SIMILAR TO
	pattern for search substring, not match

	*	Any sequence of characters
	?	Any single character
	|	or
	\*	*
	\?	?
	\|	|
	\\	\
	"""
	if pattern:
		pattern = pattern.replace('\\|', '\0')
		parts = pattern.split('|')

		parts = map(lambda p: convertPattern(
				p.replace('\0', '\\|'), 
				COMMANDS_WILDCARD, 
				COMMANDS_SIMILAR, 
				'\\', 
				'\\'
			), 
			parts
		)

		if search:
			# make start before and after text
			pattern = ''.join(('%', '%|%'.join(parts), '%'))
		else:
			if len(parts) > 1:
				pattern = '(%s)' % ')|('.join(parts) 
			else:
				pattern = '|'.join(parts) 

		# convert a to (A|a)
		pattern = ''.join(map(makeCaseInsensitivePattern, pattern))
	
		return pattern
	

def convertWildcardToLike(pattern, search=True):
	if pattern:
		if search:
			pattern = ''.join(('*', pattern, '*'))
		return convertPattern(
			pattern, 
			'*?', 
			'%_', 
			'\\', 
			'\\'
		)

def convertWildcardToInteger(pattern):
	"""
	returns int if only pattern is integer number
	"""
	if pattern:
		try:
			a = int(pattern.strip())
			if a >= 0 and a <= 0x7FFFFFFF:
				return a
		except:
			pass




if __name__ == '__main__':
	for test in (
		'?',
		'*',
		'1|2',
		'\\?',
		'\\*',
		'\\|',
		'\\',
		'40%',
		u'ба?а|д?д',
	):
		print "%-10s %s" % (test, convertWildcardToSimilar(test))
