#!/usr/bin/python
# -*- coding: Cp1251 -*-
#
# XMLBuffer.py

from cStringIO import StringIO
import types

## helper functions
from xml.sax.saxutils import escape, quoteattr

def cdataSection(value) :
	return "<![CDATA[%s]]>" % (value,)

class XmlWriter:

	# Creates new XMLBuffer
	def __init__(self, out=None, encoding=None, pretty = 0, indent='\t', noDocType=0):

		if out is None: out = StringIO()
		if encoding is None: encoding = "iso-8859-1"

		self._out = out
		self._encoding = encoding
		self._pretty = pretty
		self._ident = 0
		self._identString = indent

		self._tagStack = []
		if not noDocType:
			self._out.write('<?xml version="1.0" encoding="%s"?>' % self._encoding)

########################################################

	def escape(self, text):
		return escape(text)

	def openElement(self, name, attributes=None):
		self.indent()
		self._out.write("<")
		self._out.write(name)
		self._writeAttributes(attributes, name)
		self._out.write(">")
		self._ident+=1
		self._tagStack.append(name)
		return self


	def writeElement(self, name, attributes=None):
		self.indent()
		self._out.write("<"+name)
		self._writeAttributes(attributes, name)
		self._out.write("/>")
		return self

	def writeElementWithText(self, name, text, attributes=None):
		self.indent()
		self._out.write("<"+name)
		self._writeAttributes(attributes, name)
		self._out.write(">")
		self._out.write(self.escape(text))
		self._out.write("</%s>" % (name,))
		return self


	def _writeAttributes(self, attributes, elementName=None):
		if attributes:
			if isinstance(attributes, dict):
				for key in attributes.keys():
					value = attributes[key]
					if not isinstance(value, types.StringTypes):
						value = str(value)
					self._out.write(" %s=%s" % (key, quoteattr(value)))
			else:
				self._out.write(" %s" % (attributes,))


	def closeElement(self, name=None):
		self._ident-=1
		self.indent()
		expected = self._tagStack.pop()
		assert name is None or name == expected, "Invalid element to close: %s. Expecting: %s" % (name, expected)
		self._out.write("</%s>" % expected)
		return self

	def closeElements(self):
		while len(self._tagStack):
			self.closeElement()
		return self

	def newLine(self, count=1):
		if self._pretty:
			self._out.write('\n' * count)
		return self

	def indent(self) :
		if self._pretty:
			self._out.write('\n')
			self._out.write(self._identString*self._ident)
		return self

	def writeTextSection(self, text):
		self.indent()
		self._out.write(self.escape(text))
		return self

	def continueTextSection(self, text):
		self._out.write(self.escape(text))
		return self

	def writeLines(self, text, sep=None):
		"""
		this function strips every line and puts it out.
		Attention:
			not-pretty mode: it can remove valuable newline delimiter!
		"""
		if not sep: sep = self._identString
		for line in text.split('\n'):
			line = line.rstrip()
			n = len(line)
			line = line.lstrip()
			if self._pretty:
				indent = (n - len(line)) / len(sep)
				self.indent()
				self._out.write(self._identString * indent)
			self._out.write(line)
		return self

	def writeComment(self, text):
		lines = text.split('\n')
		if len(lines) == 1:
			self.indent()
			self._out.write("<!-- ");
			self._out.write(text);
			self._out.write(" -->");
		else:
			self.indent()
			self._out.write("<!--");
			for line in lines:
				self.indent()
				self._out.write(line);
			self.indent()
			self._out.write("-->");
		return self

	def writeProcessingInstruction(self, name, attributes={}):
		self.indent()
		self._out.write("<?");
		self._out.write(name);
		self._writeAttributes(attributes)
		self._out.write("?>");
		return self


	def __str__(self):
		if hasattr(self._out, "getvalue"):
			return self._out.getvalue()
		else:
			return "<%s on %s>" % (self.__class__.__name__, str(self._out))

	def toxml(self):
		if hasattr(self._out, "getvalue"):
			return self._out.getvalue()
		else:
			raise Exception, "Can't return xml - output stream is not StringIO"

	def toprettyxml(self):
		return self.toxml()

	def writexml(self, out):
		out.write(self.toxml())

	def close(self):
		self._out.close()

	def flush(self):
		self._out.flush()

if __name__ == '__main__':
	import sys
	b = XmlWriter(sys.stdout, pretty=1)
	b.writeProcessingInstruction("xml", {"version":"1.0"})
	b.openElement("xxxxxx")
	b.openElement("root", {"a":10, "b":11, "c":13})
	b.writeTextSection("Hello ");
	b.continueTextSection("World");
	b.continueTextSection("Жопа<tag>&<?fuck?/>");
	b.continueTextSection("World");
	b.writeTextSection("Hello ");
	b.continueTextSection("World");
	b.continueTextSection("World");
	b.continueTextSection("World");
	b.writeElement("tag", {"a":"\"10'", "b":11, "c":13})
	b.writeComment("bebe lksdf\njsdkl\nfjnsldk\nfjsdklfj")
	b.closeElements()
	print
	print b

