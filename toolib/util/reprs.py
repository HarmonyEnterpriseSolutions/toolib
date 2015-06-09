# -*- coding: Cp1251 -*-
"""
cyrillics for repr
"""
__builtin_repr = repr

def repr(object):
	try:
		f = eval("repr_" + type(object).__name__)
	except NameError:
		f = __builtin_repr
	return f(object)

_STR_REPLACES = (
	('\\', '\\\\'),
	('\t', '\\t'),
	#('\n', '\\n'),		# multiline formatted
	('\r', '\\r'),
	('\"', '\\\"'),
)
	
def repr_str(s):
	if '\n' in s:
		return '"""\\\n%s"""' % s.replace('\\', '\\\\')
	else:
		for t in _STR_REPLACES:
			s = s.replace(*t)
		return '"%s"' % s

def repr_unicode(s):
	return 'u%s' % repr_str(str(s))

def repr_list(l):
	return "[%s]" % ', '.join(map(repr, l))

def repr_tuple(t):
	if len(t) == 1:
		return "(%s,)" % ', '.join(map(repr, t))
	else:
		return "(%s)" % ', '.join(map(repr, t))

def repr_dict(d):
	keys = d.keys()
	keys.sort()
	return "{ %s }" % ', '.join(['%s : %s' % (repr(key), repr(d[key])) for key in keys])

if __name__ == '__main__':
	import toolib.startup
	toolib.startup.hookStd()

	r = { 
	None : (2147352567, '\xce\xf8\xe8\xe1\xea\xe0.', (0, 'Microsoft JET Database Engine', "\xcd\xe5 \xf3\xe4\xe0\xe5\xf2\xf1\xff \xed\xe0\xe9\xf2\xe8 \xf4\xe0\xe9\xeb 'Z:\\projects\\lider\\db\\liderdb.mdb2'.", None, 5003024, -2147467259), None),
	'bubu' : 'baba',
	}
	print repr(r)
	assert eval(repr(r)) == r
