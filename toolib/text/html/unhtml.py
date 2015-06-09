# -*- coding: UTF-8 -*-

import re
from BeautifulSoup import BeautifulSoup, Comment, Tag, NavigableString, Declaration

"""
#http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python

using BeautifulSoup to get text elements
	replacing HTML character entity references
	replacing HTML character entity ordinals (&#8888;)
	excluding tags with style "display: none"
	excluding scripts, etc. (EXCLUDE_CHILD_OF)
	excluding comments (EXCLUDE_INSTANCES)

TODO: correct newlines
"""

EXCLUDE_CHILD_OF = set((
	'script',
	'option',
))

EXCLUDE_INSTANCES = (Comment,)

# from http://www.w3.org/TR/html4/sgml/entities.html
HTML_CHAR_ENTITY_REFS = {

	# Character entity set
	#'nbsp'     : u'\u00a0', # ' '	# we are convering to text so do not need different spaces
	'nbsp'     : u' ', # ' '

	'iexcl'    : u'\u00a1', # '¡'
	'cent'     : u'\u00a2', # '¢'
	'pound'    : u'\u00a3', # '£'
	'curren'   : u'\u00a4', # '¤'
	'yen'      : u'\u00a5', # '¥'
	'brvbar'   : u'\u00a6', # '¦'
	'sect'     : u'\u00a7', # '§'
	'uml'      : u'\u00a8', # '¨'
	'copy'     : u'\u00a9', # '©'
	'ordf'     : u'\u00aa', # 'ª'
	'laquo'    : u'\u00ab', # '«'
	'not'      : u'\u00ac', # '¬'
	'shy'      : u'\u00ad', # '­'
	'reg'      : u'\u00ae', # '®'
	'macr'     : u'\u00af', # '¯'
	'deg'      : u'\u00b0', # '°'
	'plusmn'   : u'\u00b1', # '±'
	'sup2'     : u'\u00b2', # '²'
	'sup3'     : u'\u00b3', # '³'
	'acute'    : u'\u00b4', # '´'
	'micro'    : u'\u00b5', # 'µ'
	'para'     : u'\u00b6', # '¶'
	'middot'   : u'\u00b7', # '·'
	'cedil'    : u'\u00b8', # '¸'
	'sup1'     : u'\u00b9', # '¹'
	'ordm'     : u'\u00ba', # 'º'
	'raquo'    : u'\u00bb', # '»'
	'frac14'   : u'\u00bc', # '¼'
	'frac12'   : u'\u00bd', # '½'
	'frac34'   : u'\u00be', # '¾'
	'iquest'   : u'\u00bf', # '¿'
	'Agrave'   : u'\u00c0', # 'À'
	'Aacute'   : u'\u00c1', # 'Á'
	'Acirc'    : u'\u00c2', # 'Â'
	'Atilde'   : u'\u00c3', # 'Ã'
	'Auml'     : u'\u00c4', # 'Ä'
	'Aring'    : u'\u00c5', # 'Å'
	'AElig'    : u'\u00c6', # 'Æ'
	'Ccedil'   : u'\u00c7', # 'Ç'
	'Egrave'   : u'\u00c8', # 'È'
	'Eacute'   : u'\u00c9', # 'É'
	'Ecirc'    : u'\u00ca', # 'Ê'
	'Euml'     : u'\u00cb', # 'Ë'
	'Igrave'   : u'\u00cc', # 'Ì'
	'Iacute'   : u'\u00cd', # 'Í'
	'Icirc'    : u'\u00ce', # 'Î'
	'Iuml'     : u'\u00cf', # 'Ï'
	'ETH'      : u'\u00d0', # 'Ð'
	'Ntilde'   : u'\u00d1', # 'Ñ'
	'Ograve'   : u'\u00d2', # 'Ò'
	'Oacute'   : u'\u00d3', # 'Ó'
	'Ocirc'    : u'\u00d4', # 'Ô'
	'Otilde'   : u'\u00d5', # 'Õ'
	'Ouml'     : u'\u00d6', # 'Ö'
	'times'    : u'\u00d7', # '×'
	'Oslash'   : u'\u00d8', # 'Ø'
	'Ugrave'   : u'\u00d9', # 'Ù'
	'Uacute'   : u'\u00da', # 'Ú'
	'Ucirc'    : u'\u00db', # 'Û'
	'Uuml'     : u'\u00dc', # 'Ü'
	'Yacute'   : u'\u00dd', # 'Ý'
	'THORN'    : u'\u00de', # 'Þ'
	'szlig'    : u'\u00df', # 'ß'
	'agrave'   : u'\u00e0', # 'à'
	'aacute'   : u'\u00e1', # 'á'
	'acirc'    : u'\u00e2', # 'â'
	'atilde'   : u'\u00e3', # 'ã'
	'auml'     : u'\u00e4', # 'ä'
	'aring'    : u'\u00e5', # 'å'
	'aelig'    : u'\u00e6', # 'æ'
	'ccedil'   : u'\u00e7', # 'ç'
	'egrave'   : u'\u00e8', # 'è'
	'eacute'   : u'\u00e9', # 'é'
	'ecirc'    : u'\u00ea', # 'ê'
	'euml'     : u'\u00eb', # 'ë'
	'igrave'   : u'\u00ec', # 'ì'
	'iacute'   : u'\u00ed', # 'í'
	'icirc'    : u'\u00ee', # 'î'
	'iuml'     : u'\u00ef', # 'ï'
	'eth'      : u'\u00f0', # 'ð'
	'ntilde'   : u'\u00f1', # 'ñ'
	'ograve'   : u'\u00f2', # 'ò'
	'oacute'   : u'\u00f3', # 'ó'
	'ocirc'    : u'\u00f4', # 'ô'
	'otilde'   : u'\u00f5', # 'õ'
	'ouml'     : u'\u00f6', # 'ö'
	'divide'   : u'\u00f7', # '÷'
	'oslash'   : u'\u00f8', # 'ø'
	'ugrave'   : u'\u00f9', # 'ù'
	'uacute'   : u'\u00fa', # 'ú'
	'ucirc'    : u'\u00fb', # 'û'
	'uuml'     : u'\u00fc', # 'ü'
	'yacute'   : u'\u00fd', # 'ý'
	'thorn'    : u'\u00fe', # 'þ'
	'yuml'     : u'\u00ff', # 'ÿ'
	'fnof'     : u'\u0192', # 'ƒ'

	# Mathematical, Greek and Symbolic characters for HTML
	'Alpha'    : u'\u0391', # 'Α'
	'Beta'     : u'\u0392', # 'Β'
	'Gamma'    : u'\u0393', # 'Γ'
	'Delta'    : u'\u0394', # 'Δ'
	'Epsilon'  : u'\u0395', # 'Ε'
	'Zeta'     : u'\u0396', # 'Ζ'
	'Eta'      : u'\u0397', # 'Η'
	'Theta'    : u'\u0398', # 'Θ'
	'Iota'     : u'\u0399', # 'Ι'
	'Kappa'    : u'\u039a', # 'Κ'
	'Lambda'   : u'\u039b', # 'Λ'
	'Mu'       : u'\u039c', # 'Μ'
	'Nu'       : u'\u039d', # 'Ν'
	'Xi'       : u'\u039e', # 'Ξ'
	'Omicron'  : u'\u039f', # 'Ο'
	'Pi'       : u'\u03a0', # 'Π'
	'Rho'      : u'\u03a1', # 'Ρ'
	'Sigma'    : u'\u03a3', # 'Σ'
	'Tau'      : u'\u03a4', # 'Τ'
	'Upsilon'  : u'\u03a5', # 'Υ'
	'Phi'      : u'\u03a6', # 'Φ'
	'Chi'      : u'\u03a7', # 'Χ'
	'Psi'      : u'\u03a8', # 'Ψ'
	'Omega'    : u'\u03a9', # 'Ω'
	'alpha'    : u'\u03b1', # 'α'
	'beta'     : u'\u03b2', # 'β'
	'gamma'    : u'\u03b3', # 'γ'
	'delta'    : u'\u03b4', # 'δ'
	'epsilon'  : u'\u03b5', # 'ε'
	'zeta'     : u'\u03b6', # 'ζ'
	'eta'      : u'\u03b7', # 'η'
	'theta'    : u'\u03b8', # 'θ'
	'iota'     : u'\u03b9', # 'ι'
	'kappa'    : u'\u03ba', # 'κ'
	'lambda'   : u'\u03bb', # 'λ'
	'mu'       : u'\u03bc', # 'μ'
	'nu'       : u'\u03bd', # 'ν'
	'xi'       : u'\u03be', # 'ξ'
	'omicron'  : u'\u03bf', # 'ο'
	'pi'       : u'\u03c0', # 'π'
	'rho'      : u'\u03c1', # 'ρ'
	'sigmaf'   : u'\u03c2', # 'ς'
	'sigma'    : u'\u03c3', # 'σ'
	'tau'      : u'\u03c4', # 'τ'
	'upsilon'  : u'\u03c5', # 'υ'
	'phi'      : u'\u03c6', # 'φ'
	'chi'      : u'\u03c7', # 'χ'
	'psi'      : u'\u03c8', # 'ψ'
	'omega'    : u'\u03c9', # 'ω'
	'thetasym' : u'\u03d1', # 'ϑ'
	'upsih'    : u'\u03d2', # 'ϒ'
	'piv'      : u'\u03d6', # 'ϖ'
	'bull'     : u'\u2022', # '•'
	'hellip'   : u'\u2026', # '…'
	'prime'    : u'\u2032', # '′'
	'Prime'    : u'\u2033', # '″'
	'oline'    : u'\u203e', # '‾'
	'frasl'    : u'\u2044', # '⁄'
	'weierp'   : u'\u2118', # '℘'
	'image'    : u'\u2111', # 'ℑ'
	'real'     : u'\u211c', # 'ℜ'
	'trade'    : u'\u2122', # '™'
	'alefsym'  : u'\u2135', # 'ℵ'
	'larr'     : u'\u2190', # '←'
	'uarr'     : u'\u2191', # '↑'
	'rarr'     : u'\u2192', # '→'
	'darr'     : u'\u2193', # '↓'
	'harr'     : u'\u2194', # '↔'
	'crarr'    : u'\u21b5', # '↵'
	'lArr'     : u'\u21d0', # '⇐'
	'uArr'     : u'\u21d1', # '⇑'
	'rArr'     : u'\u21d2', # '⇒'
	'dArr'     : u'\u21d3', # '⇓'
	'hArr'     : u'\u21d4', # '⇔'
	'forall'   : u'\u2200', # '∀'
	'part'     : u'\u2202', # '∂'
	'exist'    : u'\u2203', # '∃'
	'empty'    : u'\u2205', # '∅'
	'nabla'    : u'\u2207', # '∇'
	'isin'     : u'\u2208', # '∈'
	'notin'    : u'\u2209', # '∉'
	'ni'       : u'\u220b', # '∋'
	'prod'     : u'\u220f', # '∏'
	'sum'      : u'\u2211', # '∑'
	'minus'    : u'\u2212', # '−'
	'lowast'   : u'\u2217', # '∗'
	'radic'    : u'\u221a', # '√'
	'prop'     : u'\u221d', # '∝'
	'infin'    : u'\u221e', # '∞'
	'ang'      : u'\u2220', # '∠'
	'and'      : u'\u2227', # '∧'
	'or'       : u'\u2228', # '∨'
	'cap'      : u'\u2229', # '∩'
	'cup'      : u'\u222a', # '∪'
	'int'      : u'\u222b', # '∫'
	'there4'   : u'\u2234', # '∴'
	'sim'      : u'\u223c', # '∼'
	'cong'     : u'\u2245', # '≅'
	'asymp'    : u'\u2248', # '≈'
	'ne'       : u'\u2260', # '≠'
	'equiv'    : u'\u2261', # '≡'
	'le'       : u'\u2264', # '≤'
	'ge'       : u'\u2265', # '≥'
	'sub'      : u'\u2282', # '⊂'
	'sup'      : u'\u2283', # '⊃'
	'nsub'     : u'\u2284', # '⊄'
	'sube'     : u'\u2286', # '⊆'
	'supe'     : u'\u2287', # '⊇'
	'oplus'    : u'\u2295', # '⊕'
	'otimes'   : u'\u2297', # '⊗'
	'perp'     : u'\u22a5', # '⊥'
	'sdot'     : u'\u22c5', # '⋅'
	'lceil'    : u'\u2308', # '⌈'
	'rceil'    : u'\u2309', # '⌉'
	'lfloor'   : u'\u230a', # '⌊'
	'rfloor'   : u'\u230b', # '⌋'
	'lang'     : u'\u2329', # '〈'
	'rang'     : u'\u232a', # '〉'
	'loz'      : u'\u25ca', # '◊'
	'spades'   : u'\u2660', # '♠'
	'clubs'    : u'\u2663', # '♣'
	'hearts'   : u'\u2665', # '♥'
	'diams'    : u'\u2666', # '♦'
	
	# Special characters for HTML
	'quot'     : u'\u0022', # '"'
	'amp'      : u'\u0026', # '&'
	'lt'       : u'\u003c', # '<'
	'gt'       : u'\u003e', # '>'
	'OElig'    : u'\u0152', # 'Œ'
	'oelig'    : u'\u0153', # 'œ'
	'Scaron'   : u'\u0160', # 'Š'
	'scaron'   : u'\u0161', # 'š'
	'Yuml'     : u'\u0178', # 'Ÿ'
	'circ'     : u'\u02c6', # 'ˆ'
	'tilde'    : u'\u02dc', # '˜'
	'ensp'     : u'\u2002', # ' '
	'emsp'     : u'\u2003', # ' '
	'thinsp'   : u'\u2009', # ' '
	'zwnj'     : u'\u200c', # '‌'
	'zwj'      : u'\u200d', # '‍'
	'lrm'      : u'\u200e', # '‎'
	'rlm'      : u'\u200f', # '‏'
	'ndash'    : u'\u2013', # '–'
	'mdash'    : u'\u2014', # '—'
	'lsquo'    : u'\u2018', # '‘'
	'rsquo'    : u'\u2019', # '’'
	'sbquo'    : u'\u201a', # '‚'
	'ldquo'    : u'\u201c', # '“'
	'rdquo'    : u'\u201d', # '”'
	'bdquo'    : u'\u201e', # '„'
	'dagger'   : u'\u2020', # '†'
	'Dagger'   : u'\u2021', # '‡'
	'permil'   : u'\u2030', # '‰'
	'lsaquo'   : u'\u2039', # '‹'
	'rsaquo'   : u'\u203a', # '›'
}

REC_CHAR_ENTITY_REF = re.compile(u'''(?mu)\&(%s)\;''' % '|'.join(HTML_CHAR_ENTITY_REFS.keys()))
REC_CHAR_ENTITY_ORD = re.compile(u'''(?mu)\&\#(\d+)\;''')

def resolve_char_entities(text):
	text = REC_CHAR_ENTITY_REF.sub(lambda m: HTML_CHAR_ENTITY_REFS[m.groups()[0]], text)
	text = REC_CHAR_ENTITY_ORD.sub(lambda m: unichr(int(m.groups()[0])), text)
	return text

REC_WHITESPACE = re.compile('''\s+''')
def remove_whitespace(text):
	return REC_WHITESPACE.sub(lambda m: ' ', text)

REC_DISPLAY_NONE = re.compile(u'''(?imu)(^|\s)display:\s*none(\s|$)''')

def _is_hidden(element):
	while element:
		for k, v in element.attrs:
			if k == 'style':
				if REC_DISPLAY_NONE.match(v):
					return True
				break
		element = element.parent
	return False

def unhtml_searchable(html):
	if isinstance(html, basestring):
		soup = BeautifulSoup(html)
	else:
		soup = html

	return ' '.join(filter(None, (
		resolve_char_entities(unicode(i)).strip() 
		for i in soup.findAll(text=True)
		if 
			i.parent.name not in EXCLUDE_CHILD_OF 
			and not isinstance(i, EXCLUDE_INSTANCES) 
			and not _is_hidden(i.parent)
	)))


def unhtml_readable(html):

	if isinstance(html, basestring):
		soup = BeautifulSoup(html)
	else:
		soup = html

	result = []

	for node in soup.recursiveChildGenerator():
		if isinstance(node, Tag):
			if node.name in ('br', 'tr'):
				result.append('\n')

		if isinstance(node, Declaration):
			# NavigableString is superclass of Declaration?
			pass

		elif isinstance(node, NavigableString):
			if node.parent.name not in EXCLUDE_CHILD_OF and not isinstance(node, EXCLUDE_INSTANCES) and not _is_hidden(node.parent):
				text = resolve_char_entities(unicode(node).strip())
				if text:
				    # append space if previous is not whitespace
					if result and result[-1] not in (' ', '\n'):
						result.append(' ')

					result.append(text)

					if node.parent.name == 'a':
						if node.parent.has_key('href') and node.parent['href'] != text:
							result.append(' [%s]' % node.parent['href'])

	return u''.join(result)


if __name__ == '__main__':
	import urllib2

	#html = open("1.html").read()
	html = urllib2.urlopen("http://www.wwm.com.ua/rus/news/news/2011/04/28/39/").read()
	
	print unhtml_readable(html)#.encode('UTF8')
	#print unhtml_searchable(html).encode('UTF8')
