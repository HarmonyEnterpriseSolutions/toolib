#################################################################
# Program:   Scripts
"""
	Copies files to Release directory, as listed in list file
	Target OS: WINDOWS ONLY

---BEGIN List File --->
RELEASE: <release-tag>

./py/xlbookmarks/bin/ExcelBookmarks.bat
./py/xlbookmarks/bin/pythonpathes.py
./py/xlbookmarks/bin/msgbox.exe
./py/xlbookmarks/*.pyc  -r
<---END---

	-r means recursive
	wildcards is acceptable
	list file name passed to script by firs argument

	creates directory in ./Release/<release-tag>/ and copies there
	listed files

"""
__author__  = "All"
__date__	= "$Date: 2003/11/18 13:02:02 $"
__version__ = "$Revision: 1.2 $"
# $Source: D:/HOME/cvs/toolib/scripts/release.py,v $
#																#
#################################################################
import sys, os

MAGIC = "RELEASE:"
REMOVE_ALL = "RMDIR /S /Q %s 1>NUL 2>NUL"
COPY = "XCOPY %s %s 1>NUL"
COPY_RECURSIVE = "XCOPY %s %s /S 1>NUL"

def main(lst):
	f = open(lst, 'rt')
	try:
		line = f.readline()
		if not line.startswith(MAGIC):
			print ".lst file should start with ", MAGIC
			return

		release = line[len(MAGIC):].strip()
		print "\nMaking Release:", release

		releasePath = os.path.join('.', 'Release', release)
		print "Target path   :", releasePath

		if os.path.exists(releasePath):
			os.system(REMOVE_ALL % releasePath)

		os.makedirs(releasePath)

		line = f.readline()
		while line:
			line = line.strip()

			if line:
				recursive = line.endswith('-r')
				if recursive:
					copy_pattern = COPY_RECURSIVE
					line = line[:-2].strip()
				else:
					copy_pattern = COPY

				line = line.replace('/', os.sep)
				destPath = os.path.split(line)[0]
				copycmd = copy_pattern % ( line, os.path.join(releasePath,destPath) + os.sep)

				if recursive:
					print "  copy -r", line
				else:
					print "  copy   ", line
				os.system(copycmd)

			line = f.readline()

	finally:
		f.close()

if __name__ == '__main__':
	try:
		listFile = sys.argv[1]
	except IndexError:
		print "Usage: release <list-file>"
		print __doc__
	else:
		main(listFile)
