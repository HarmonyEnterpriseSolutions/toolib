
def getWindowChildrenRecursive(window, includeThis=False):
	l = []
	if includeThis:
		l.append(window)
	__addWindowChildrenRecursive(window, l)
	return l

def __addWindowChildrenRecursive(window, l):
	l.extend(window.GetChildren())
	for w in window.GetChildren():
		__addWindowChildrenRecursive(w, l)
