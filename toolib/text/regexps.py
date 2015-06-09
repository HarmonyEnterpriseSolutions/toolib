#-*- coding: cp1251 -*-
import re

REC_LETTER = re.compile(r'(?u)([\w])')

def _sub_letter(m):
	letter = m.groups()[0]
	u = letter.upper()
	l = letter.lower()
	if u == l:
		return letter
	else:
		return '(%s|%s)' % (u, l)

def wildcard_to_re(w, ignore_case=False):
	"""
	'*', '?', '\*', '\?', '|'
	"""
	if ignore_case:
		w = REC_LETTER.sub(_sub_letter, w)
	return (
		re.escape(w)
		.replace(r'\\\?', '\0')
		.replace(r'\\\*', '\1')
		.replace(r'\\\|', '\2')
		.replace(r'\\\(', '\3')
		.replace(r'\\\)', '\4')
		
		.replace(r'\?',   '.?')
		.replace(r'\*',   '.*')
		.replace(r'\|',   '|')
		.replace(r'\(',   '(')
		.replace(r'\)',   ')')
		
		.replace('\0',   r'\?')
		.replace('\1',   r'\*')
		.replace('\2',   r'\|')
		.replace('\3',   r'\(')
		.replace('\4',   r'\)')
	)


def like_to_re(s):

	if s.startswith('%'):
		s = s[1:]

	if s.endswith('%') and not s.endswith(r'\%'):
		s = s[:-1]

	return (re.escape(s)
		.replace(r'\\\%', '\0')
		.replace(r'\\\_', '\1')
		.replace(r'\%',   '.*')
		.replace(r'\_',   '.')
		.replace('\0',    r'\%')
		.replace('\1',    '_')
	)
	
if __name__ == '__main__':

	print wildcard_to_re(u'(баба|дэд)', True)