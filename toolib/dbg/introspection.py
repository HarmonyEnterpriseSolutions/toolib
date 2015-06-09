import sys
from toolib.util.strings import stripText, indentText

def resolveClassAndName(klass, name):
	for c in klass.mro():
		try:
			return c, c.__dict__[name]
		except KeyError:
			pass

	raise AttributeError, name
		

def dump_class(klass, out=None, printDoc=True):
	out = out or sys.stdout

	print >> out, "============================================"
	print >> out, "class %s dump" % klass.__name__
	print >> out, "============================================"

	mro = klass.mro()
	mro.reverse()

	res = []

	for i in dir(klass):
		c, m = resolveClassAndName(klass, i)
		res.append((mro.index(c), m.__class__.__name__, i))

	res.sort()

	oldPos = -1
	for classPos, attrType, attrName in res:
		if classPos > 0:
			className = mro[classPos].__name__
			if oldPos != classPos:
				print >> out
				print >> out
				print >> out, "--------------------------------------------------------"
				print >> out, "class:", className
				print >> out, "--------------------------------------------------------"
				print >> out

			attr = getattr(mro[classPos], attrName)
			doc = attr.__doc__

			if printDoc and doc and not isinstance(attr, (str, unicode, int, long, list, tuple, dict)):
				doc = indentText(stripText(doc, preserveIndent=True, stripLines=True))
				if doc.lstrip().startswith(attrName):
					print >> out, "%s %s::%s" % (attrType, className, doc.lstrip())
				else:
					print >> out, "%s %s::%s" % (attrType, className, attrName)
					if not doc[0] == '\n':
						print >> out
					print >> out, doc
				if not doc[-1] == '\n':
					print >> out
			else:
				print >> out, "%s %s::%s" % (attrType, className, attrName)

			oldPos = classPos

	print >> out, "============================================"


def dump_attr(o, name=None, indent=0):
	print "%s.%s = %s" % ('\t' * indent, name, repr(o)[:80])
	for i in dir(o):
		if i.startswith('__') and i.endswith('__'):
			continue
		sub = getattr(o, i)

		if isinstance(sub, (types.MethodType, types.FunctionType, type("".split))):
			continue
			#pass

		if sub is o:
			sub = '<self>'

		if indent < 5:
			dump_attr(sub, i, indent+1)

