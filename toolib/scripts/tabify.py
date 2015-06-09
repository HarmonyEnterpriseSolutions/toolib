#!/usr/bin/python
# tabify.py -- Convert indentation with spaces to tabs
# 2006-01-23 by Yuce Tekol. www.geocities.com/yucetekol
# Last modification: 2006-07-18

import sys
import os
from stat import ST_MODE
import tokenize
from toolib.util.paths import iterFilePaths
from collections import deque
import re

REC_INDENT = re.compile("([\ \t]*)")
TABSPACE = ' ' * 8

TOKTYPE = {}

for i in dir(tokenize):
	if i.upper() == i:
		TOKTYPE[getattr(tokenize, i)] = i
		

__VERSION__ = "0.5.2"
DEBUG = 0


def tabifyFile(filename, tab):
	mode = os.stat(filename)[ST_MODE]

	bakFileName = filename + ".tabify.bak"

	try:
		os.rename(filename, bakFileName)
	except:
		# already tabified
		return
	
	infile = file(bakFileName, 'rt')
	outfile = file(filename, "wt")

	try:
		try:
			tabify(infile, outfile, tab)
		finally:
			try:
				infile.close()
			except:
				pass
			try:
				outfile.close()
			except:
				pass
		#d, f = os.path.split(os.path.abspath(filename))
		#sys.path.insert(0, d)
		#try:
		#	m = os.path.splitext(f)[0]
		#	__import__(m)
		#finally:
		#	del sys.path[0]
	except:
		os.remove(filename)
		os.rename(bakFileName, filename)
		raise
	else:
		os.remove(bakFileName)
		os.chmod(filename, mode)


def tabify(infile, outfile, tab):
	queue = []

	for toktype, indent, line in iterIndentLines(infile):
		if DEBUG: print '-----------> ', line
		if toktype in (tokenize.COMMENT, tokenize.NL):
			queue.append(line)
		else:
		
			for i in queue:
				if i:
					outfile.write(tab * indent)
					outfile.write(i)
				outfile.write("\n")
			del queue[:]
		
			if line:
				outfile.write(tab * indent)
				outfile.write(line)
			outfile.write("\n")


def textColAndStrip(line, tabsize=8):
	"""
	returns tuple(text column, text position in line)
	"""
	line = line.rstrip()
	space = REC_INDENT.match(line).groups()[0]

	# calc position
	col = 0
	for char in space:
		if char == ' ':
			col += 1
		elif char == '\t':
			col = col + tabsize - col % tabsize

	return col, line[len(space):]


def expandTabs(line, tabsize=8):
	col, line = textColAndStrip(line, tabsize)
	return ' ' * col + line


def removeIndent(line, indent):
	return 

def iterIndentLines(infile):
	indent = 0
	bracketDepth = 0
	division = 0

	y_max = -1
	prevline = ''

	for toktype, token, start, (y, x), line in tokenize.generate_tokens(infile.readline):
		if DEBUG: print '>>> %-10s %s' % (TOKTYPE[toktype], repr(token))

		if   toktype == tokenize.INDENT:
			indent += 1
		elif toktype == tokenize.DEDENT:
			indent -= 1
		elif toktype == tokenize.ENDMARKER:
			pass
		elif y > y_max:
			y_max = y

			line = line.strip()
		
			# \ inside brackets is superfluous (buggy)
			#if line.endswith('\\') and bracketDepth > 0:
			#	line = line[:-1]

			if toktype == tokenize.STRING and (token.startswith("'''") or token.startswith('"""')):
				lines = line.split('\n')

				colsAndLines = map(textColAndStrip, lines)

				try:
					mincol = min([c for c, l in colsAndLines[1:] if l])
				except ValueError:	# all lines is empty
					mincol = 0
				
				l = colsAndLines[0][1]
				if not prevline.endswith(l):
					yield toktype, indent, l
					for c, l in colsAndLines[1:]:
						yield toktype, indent, ' ' * (c - mincol) + l
				else:
					# do not reindent strings which is not docstrings
					for l in lines[1:]:
						yield toktype, 0, l

			else:
				prevline = line
				if line and line[0] in ')]}':
					yield toktype, indent + bracketDepth - 1 + division, line
				else:
					yield toktype, indent + bracketDepth + division, line

			# reset \ division each line
			division = 0
			if line.endswith('\\') and line.rfind('#') == -1:
				division = 1

		if toktype == tokenize.OP and token in '([{':
			bracketDepth += 1
		elif toktype == tokenize.OP and token in ')]}':
			bracketDepth -= 1

def test():
	tabify(open('test.py', 'rt'), open('test2.py', 'wt'), '    ') #sys.stdout)
			

def main(path, indent=None):
	if indent is None:
		tab = '\t'
	else:
		tab = ' ' * indent

	for filename in iterFilePaths(sys.argv[1]):
		try:
			tabifyFile(filename, tab)
		except Exception, e:
			print '! Error tabifying: %s. %s: %s' % (filename, e.__class__.__name__, e)
			raise
		else:
			print '  Processing: %s' % (filename,)

			
	
if __name__ == "__main__":
	try:
		main(*sys.argv[1:])
	except TypeError:
		print "usage: %s ./**/*.py [<space indent>]" % sys.argv[0]
		

