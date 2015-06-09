import re
from cStringIO import StringIO

REC_VARIABLE = re.compile(r"\$\{([^\}]*)}")

def translateString(s, translationDict):
	for name, replaceName in translationDict.iteritems():
		s = s.replace(name, replaceName)
	return s

def translateDictValues(targetDict, translationDict):
	for key, value in targetDict.iteritems():
		targetDict[key] = translateString(value, translationDict)

def evalVars(text, getter, rec=REC_VARIABLE):
	out = StringIO()
	pos = 0
	while 1:
		m = REC_VARIABLE.search(text, pos)
		if m:
			out.write(text[pos:m.start()])
			key = m.group(1)
			value = getter(key)
			if value is None:
				value = "${%s}" % key
			out.write(str(value))
			pos = m.end()
		else:
			out.write(text[pos:])
			break
	return out.getvalue()


if __name__ == '__main__':
	s = "Hi ${name}, I do ${do} You"

	d = {
		"name" : "girl",
		"do"   : "like",
	}

	print evalVars(s, d.get)

