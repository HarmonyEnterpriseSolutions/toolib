# -*- coding: Cp1251 -*-

import re
from BeautifulSoup import BeautifulSoup, Comment, Tag, NavigableString, Declaration
from soupselect import select


REC_ATTR = re.compile(r"^\w*\[([^\]]+)\]$")
REC_CLASS = re.compile(r"^(\w*)\.(.+)$")

def html_cleanup(html, remove_list = (), encoding=None, log=False):
	"""
	Returns (str cleaned_html, bool changes)
	``remove_list``: is list of selectors, currently supported only attribute and class selectors,
	e.g. ['p.[lang]', u'p.список-western', '[orphaned-attribute]', '.orphaned-class-name']
	``encoding`` is html encoding, autodetected if not passed
	"""

	soup = BeautifulSoup(html, fromEncoding=encoding)

	changes = False

	for selector in remove_list:
		m = REC_ATTR.match(selector)
		if m:
			attr, = m.groups()
			for element in select(soup, selector):
				if log:
					print "removing %s[%s]" % (element.name, attr)
				element.attrs = [item for item in element.attrs if item[0] != attr]
				changes = True

		else:
			m = REC_CLASS.match(selector)
			if m:
				tag, cls = m.groups()
				selector = (tag or '') + u'[class]'

				for element in select(soup, selector):

					for i, (attr, value) in enumerate(element.attrs):
						if attr == u'class':
							class_index = i

					classes = filter(None, element.attrs[class_index][1].split(' '))
					try:
						classes.remove(cls)
					except ValueError:	# not in list
						pass
					else:
						if log:
							print "removing %s.%s" % (element.name, cls)
						element.attrs[class_index] = (u'class', ' '.join(classes))
						changes = True

	if changes:
		return soup.prettify(encoding=soup.fromEncoding or soup.originalEncoding), changes
	else:
		return html, changes


if __name__ == '__main__':
	import sys
	import locale
	args = [arg.decode(locale.getdefaultlocale()[1] or 'ascii') for arg in sys.argv[1:]]
	sys.stdout.write(html_cleanup(sys.stdin.read(), remove_list=args)[0])
