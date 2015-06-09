# -*- coding: Cp1251 -*-
#################################################################
# Program:   toolib
"""
	Stream Writers
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2009/08/20 13:20:51 $"
__version__ = "$Revision: 1.8 $"
# $Source: D:/HOME/cvs/toolib/util/streams.py,v $
#																#
#################################################################

import sys
import codecs
from toolib import debug

IDX_ENCODE = 0
IDX_DECODE = 1
IDX_READER = 2
IDX_WRITER = 3

DEFAULT_ERROR_METHOD = "replace"

def getSystemDefaultEncoding():
	import locale
	return locale.getdefaultlocale()[1]

class DecodeWriter(codecs.StreamWriter):
	"""
	encoding -> unicode
	writes unicode to subsequent stream
	"""
	def __init__(self, out, encoding, errors=DEFAULT_ERROR_METHOD):
		codecs.StreamWriter.__init__(self, out, errors)
		self.decode = codecs.lookup(encoding)[IDX_DECODE]

	def write(self, object):
		if isinstance(object, unicode):
			data = object
		else:
			data = self.decode(object, self.errors)[0]
		self.stream.write(data)
		return len(data)

def EncodeWriter(unicodeOutputStream, encoding, errors=DEFAULT_ERROR_METHOD):
	"""
	Writes unicode to output
	"""
	return codecs.lookup(encoding)[IDX_WRITER](unicodeOutputStream, errors)


def Rewriter(out, inputEnc=None, outputEnc=None, errors=DEFAULT_ERROR_METHOD):
	"""
	Stream used to recode output, e.g. 1251 to console 866
	It can be done better using low-level python encoding tools
	"""
	inputEnc  = inputEnc or getSystemDefaultEncoding()
	outputEnc = outputEnc or getattr(out, 'encoding', None)

	if inputEnc and outputEnc and inputEnc != outputEnc:
		out = DecodeWriter(EncodeWriter(out, outputEnc, errors), inputEnc, errors)
	#else:
	#	debug.warning("Stream unchanged: %s" % out)
	return out

if __name__ == '__main__':
	from toolib.dbg.Timer import Timer

	s = 'Hello Мазафака!'

	print >> Rewriter(sys.stdout), s
	Rewriter(sys.stdout).writelines(["Hello ", "Мазафака!"])

	print "\n\nTesting rewriter speed:"

	nul = file("NUL", "wt")
	
	def test(stream, descr):
		timer = Timer()
	
		for i in xrange(20000):
			print >> stream, s

		print '\t%-20s %s' % (descr, timer)

	test(nul, "nul output")
	test(Rewriter(nul, "Cp1251", "Cp866"), "Rewriter")

	print "\nTesting ukrainian i:"
	print >>           Rewriter(sys.stdout, "Cp1251", "Cp866"), "\tRewriter says: 'і'"

