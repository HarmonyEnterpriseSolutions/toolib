
"""
HTML writing objects

TODO: remove from __init__
"""

import types

TAB_SIZE = 4

def write_html(out, object):
	if hasattr(object, '__write_html__'):
		return object.__write_html__(out)
	else:
		if isinstance(object, types.StringTypes):
			out.write(escape(object))
		else:
			out.write(escape(str(object)))

def escape(s):
	"""
	convert string to HTML
	"""
	assert isinstance(s, types.StringTypes), "%s, %s" % (repr(i), type(i))
	
	return (
		s.replace('&',          '&amp;')
		 .replace('<',          '&lt;')
		 .replace('>',          '&gt;')
		 .replace('"',          '&quot;')
		 .replace('\n',         '<br>\n')
		 .replace(' '*TAB_SIZE, '&nbsp;' * TAB_SIZE)
		 .replace('\t',         '&nbsp;' * TAB_SIZE)
	)
	
class inline(object):

	def __init__(self, html, parameters=None):
		if parameters:
			self.text = html % tuple(map(escape, parameters))
		else:
			self.text = html

	def __write_html__(self, out):
		out.write(self.text)

class Tag(object):

	TAG = None

	def __init__(self, content):
		self._content = content

	def __write_html__(self, out):
		assert self.TAG is not None
		out.write('<%s>' % self.TAG)
		write_html(out, self._content)
		out.write('</%s>\n' % self.TAG)

class bold(Tag):
	TAG = 'b'

class pre(Tag):
	TAG = 'pre'

class table(object):

	def __init__(self, headers, data, border=1):
		self.headers = tuple(headers)
		self.data = tuple(data)
		self.border = border

	def __write_html__(self, out):

		out.write("<TABLE border=%s>\n<TR>\n" % (self.border,))
	
		for i in self.headers:
			out.write('<TH>')
			if i is None: i = nbsp
			write_html(out, i)
			out.write('</TH>\n')

		out.write("</TR>\n")

		for row in self.data:
			out.write("<TR>\n")

			for i in row:
				out.write('<TD>')
				if i is None: i = nbsp
				write_html(out, i)
				out.write('</TD>')

			out.write("</TR>\n")

		out.write("</TABLE>\n")

nbsp = inline("&nbsp;")
