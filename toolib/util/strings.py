# -*- coding: Cp1251 -*-
#################################################################
# Program:   toolib
"""
	Extended string function
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2011/09/02 16:20:43 $"
__version__ = "$Revision: 1.14 $"
# $Source: D:/HOME/cvs/toolib/util/strings.py,v $
#																#
#################################################################

import re
from toolib import debug
from types import StringTypes


def indentText(text, char='\t', count=1, noJoin=False):

	if isinstance(text, StringTypes):
		text = text.split('\n')
	
	text = [indentLine(line, char, count) for line in text]
	
	if noJoin:
		return text
	else:
		return "\n".join(text)

def stripText(text, lchars = None, rchars=None, preserveIndent=False, stripTopLines=False, stripBottomLines=False, stripLines=False, noJoin=False):

	if isinstance(text, StringTypes):
		text = text.split('\n')

	lines = [line.rstrip(rchars) for line in text]

	if preserveIndent:
		minIndent = None
		for i, line in enumerate(lines):
			strippedLine = line.lstrip(lchars)
			if strippedLine:
				indent = len(line) - len(strippedLine)
				if minIndent is None or minIndent > indent:
					minIndent = indent
			else:
				lines[i] = ''
		minIndent = minIndent or 0

		lines = [line[minIndent:] for line in lines]
	else:
		lines = [line.lstrip(lchars) for line in lines]

	if stripLines or stripTopLines:
		while lines and not lines[0]:
			del lines[0]

	if stripLines or stripBottomLines:
		while lines and not lines[-1]:
			del lines[-1]

	if noJoin:
		return lines
	else:
		return "\n".join(lines)

def lstripText(text, chars=None):
	debug.deprecation('Use stripText (without l)')
	return stripText(text, chars)

def indentLine(line, char='\t',  count=1):
	if len(line) > 0:
		if count > 0:
			line = char*count + line
		else:
			for i in xrange(count):
				if line.startswith(char):
					line = line[1:]
				else:
					raise ValueError, "Can't unindent text"
	return line

RE_QUOTED		= r"'(\\\'|[^'])*'"
RE_DOUBLEQUOTED	= r'"(\\\"|[^"])*"'
RE_COMMENT		= r"\/\*.*\*\/"

REC_IGNORE = re.compile("|".join((
	RE_QUOTED,
	RE_DOUBLEQUOTED,
	RE_COMMENT,
)))

def splitEx(s, substr, ignoredRegions=REC_IGNORE):
	"""
	Splits string using substr
	ignoring matched ignoredRegions
	(usable for strings and comments)
	ignore is "..." '...' and /*...*/ by default
	"""
	res = []
	start = 0
	for m in ignoredRegions.finditer(s):
		l = s[start: m.start()].split(substr)
		try:
			res[-1] += l[0]
			res.extend(l[1:])
		except IndexError:
			res.extend(l)
		res[-1] += s[m.start():m.end()]
		start = m.end()
	tail = s[start:].split(substr)
	try:
		res[-1] += tail[0]
		res.extend(tail[1:])
	except IndexError:
		res.extend(tail)
	return res

def splitExRe(s, splitRec, ignoredRegions=REC_IGNORE):
	"""
	Splits string using substr
	ignoring matched ignoredRegions
	(usable for strings and comments)
	ignore is "..." '...' and /*...*/ by default
	"""
	res = []
	start = 0
	for m in ignoredRegions.finditer(s):
		l = splitRec.split(s[start: m.start()])
		try:
			res[-1] += l[0]
			res.extend(l[1:])
		except IndexError:
			res.extend(l)
		res[-1] += s[m.start():m.end()]
		start = m.end()
	tail = splitRec.split(s[start:])
	try:
		res[-1] += tail[0]
		res.extend(tail[1:])
	except IndexError:
		res.extend(tail)
	return res

def indexOfAnyChar(s, chars, start=0):
	"""
	looks for any char in chars 
	returns char and position of first occurence
	throws ValueError if none found
	"""
	poses = [s.find(char, start) for char in chars]
	try:
		i = poses.index(min(filter(lambda pos: pos != -1, poses)))
	except TypeError, e: # min expected 1 arguments, got 0
		if str(e) != "min expected 1 arguments, got 0":	raise
		raise ValueError, "no char from '%s' found" % chars
	else:
		return chars[i], poses[i]
		

def findParentheses(s, start=0, parentheses="()"):
	"""
	returns tuple
		pos of first '(' found,
		pos of corresponding ')'
	"""
	lp, rp = parentheses
	start = pos = s.index(lp, start) + 1
	level = 1
	try:
		while level > 0:
			char, pos = indexOfAnyChar(s, parentheses, pos)
			if char == lp:
				level += 1
			elif char == rp:
				level -= 1
			pos += 1
	except ValueError:
		raise ValueError, "%s parentheses needs to be closed" % level
	
	return start-1, pos-1


def splitParentheses(s, start=0, parentheses="()"):
	"""
	returns 
	(
		prefix
		substring inside first parentheses found
		postfix
	)
	"""
	start, end = findParentheses(s, start, parentheses)
	return s[:start], s[start+1:end], s[end+1:]


def makeTranslationTable(s1, s2):
	"""
	makes translation table from two strings (from, to)
	table can be used in str.translate
	"""
	tt = map(chr, range(256))
	for i in xrange(min(len(s1), len(s2))):
		tt[ord(s1[i])] = s2[i]
	return ''.join(tt)

def rsplit(s, length=3):
	"""
	splits string from right into substrings 
	lenght is length of substring
	"""
	l = len(s)
	n = (l-1)/length+1
	return [ s[-(i+1)*length:l-i*length] for i in xrange(n-1,-1,-1) ]

def quote(s, pattern='\s+', lquote='"', rquote=None):
	"""
	"""
	if re.search(pattern, s):
		return ''.join((lquote, s, rquote or lquote))
	else:
		return s

def unbracket(s, left='(', right=')'):
	if s.startswith(left) and s.endswith(right):
		return s[len(left) : -len(right)]
	else:
		return s

FILE_SYSTEM_TT = '_' * 32 + makeTranslationTable(
	r'"*/:<>?\|',
	r"'#~;''_~~",
)[32:]

def makeFileName(s):
	return str(s).translate(FILE_SYSTEM_TT)

def remove(s, chars):
	for c in chars:
		s = s.replace(c, '')
	return s

def srange(a, b):
	return ''.join(map(chr, range(ord(a), ord(b)+1)))

def shorten(s, n):
	if s is not None and n is not None:
		if len(s) > n:
			s = s[:n-3] + "..."
	return s

if __name__== '__main__':
	#print "hello\n" + indentText("word\nis\n\tnot\n\tenough")
	#for s in (
	#	""",s,d,',f,g,',z,x,",c,v,",b,n,/*,p,o,*/,t,r,""",
	#	""",,,',,,""",
	#	'12,23,"34,56"',
	#	):
	#	print s
	#	print ';'.join(splitEx(s, ","))
	#
	#	print makeFileName('Припіваючи')

	s = "hello(bebe) -> bebe"
	print repr(s)
	print splitParentheses(s)
	print findParentheses(s)

