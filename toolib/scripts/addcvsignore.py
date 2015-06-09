import os
import re
import sys

REC_CVSIGNORE_ITEM=re.compile('[^\s]+')

IGNORED = {
	'.py' : ['*.pyc', '*.pyo'],
	#'.po' : ['*.mo'],
}


def iterDirs(dir):
	yield dir
	for i in os.listdir(dir):
		f = os.path.join(dir, i)
		if os.path.isdir(f):
			for j in iterDirs(f):
				yield j


def getDirExtensions(dir):
	ext = set()

	for i in os.listdir(dir):
		f = os.path.join(dir, i)
		if not os.path.isdir(f):
			ext.add(os.path.splitext(i)[1].lower())

	ext = list(ext)
	ext.sort()

	return ext


def readCvsIgnore(dir):
	try:
		text = open(os.path.join(dir, '.cvsignore'), 'rt').read()
	except IOError:
		return []
	else:
		l = list(set(REC_CVSIGNORE_ITEM.findall(text)))
		l.sort()
		return l

def writeCvsIgnore(dir, ignored):
	if ignored:
		ignored = list(ignored)	
		ignored.sort()

		if readCvsIgnore(dir) != ignored:
			open(os.path.join(dir, '.cvsignore'), 'wt').write('\n'.join(ignored))
			return 'writen'
	else:
		try:
			os.remove(os.path.join(dir, '.cvsignore'))
			return 'removed'
		except:
			pass



def main(dir='.'):

	for d in iterDirs(os.path.abspath(dir)):
		ignored = set(readCvsIgnore(d))

		for ext in getDirExtensions(d):
			ignored.update(IGNORED.get(ext, ()))

		ignored = list(ignored)
		ignored.sort()

		if ignored:
			print d, ignored
		
		res = writeCvsIgnore(d, ignored)

		if os.path.exists(os.path.join(d, '.cvsignore')):
			os.chdir(d)
			os.system('cvs add .cvsignore')
			os.system('cvs commit -m "no message" -- .cvsignore')
		elif res == 'removed':
			os.chdir(d)
			os.system('cvs remove .cvsignore')
			os.system('cvs commit -m "no message" -- .cvsignore')

if __name__ == '__main__':
	main(*sys.argv[1:])
	