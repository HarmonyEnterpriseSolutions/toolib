DIR=r"Z:\projects\wm"
INCLUDE="Root"
EXCLUDE=""

FIND_STRING = ':pserver:oleg@212.109.59.18:/cvs'

REPLACE_STRING = ':pserver:212.109.59.18:/cvs'

MATCH_CASE=1
MATCH_WHOLE_WORDS=0

BACKUP=0

###############################################################################
# Program:   Replace Utility
"""
Replaces content of files recursively
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2008/11/11 13:06:19 $"
__version__ = "$Revision: 1.6 $"
# $Source: C:/HOME/cvs/toolib/scripts/freplace.py,v $
###############################################################################

import re

def __strsplit(src, splitstr, matchcase):
	"""
	splits a string with splitstr
	returns: list
	"""
	#if not matchcase:
	flags = 0
	if not matchcase:
		flags = flags | re.IGNORECASE
	rg = re.compile(re.escape(splitstr), flags)
	return rg.split(src)
	#else:
	#	return src.split(splitstr)

__WORDCHAR = re.compile('\w')
def __iswholeword(word, prevs, posts):
	"""
	returns nonzero if the word is whole
	"""
	if len(prevs) == 0:
		prevs = word
	if len(posts) == 0:
		posts = word
	return not __WORDCHAR.match(prevs[-1]) and not __WORDCHAR.match(posts[0])

def __joinlist(list, joinstr, matchwholewords, splitstr=None):
	"""
	joins list into joined list.
	if matchwholewords is nonzero, joins non-wole-words with splitstr
	returns <result list>, <count>
	"""
	result = []
	prevs = None
	ctr = 0
	for s in list:
		if not (prevs is None):
			if matchwholewords and not __iswholeword(splitstr, prevs, s):
				result.append(splitstr)
			else:
				result.append(joinstr)
				ctr = ctr + 1
		result.append(s)
		prevs = s
	return result, ctr

def strReplace(source, findstr, replacestr, matchcase, matchwholewords):
	list = __strsplit(source, findstr, matchcase)
	return __joinlist(list, replacestr, matchwholewords, findstr)

def replaceFromFile(infilename, findstr, replacestr, matchcase, matchwholewords):
	f = open(infilename, "rb")
	source = f.read()
	f.close()
	return strReplace(source, findstr, replacestr, matchcase, matchwholewords)

def bakFile(file):
	import os
	path, file = os.path.split(file)
	return os.path.join(path, ".%s.bak" % file)

def renameFile(file, newfile):
	import os
	if os.path.exists(newfile):
		os.remove(newfile)
	os.rename(file, newfile)

def replaceInFile(file, findstr, replacestr, matchcase, matchwholewords, keepbackups=0):
	import os
	data, count = replaceFromFile(file, findstr, replacestr, matchcase, matchwholewords)
	if count > 0:
		## make backup
		bak = bakFile(file)
		renameFile(file, bak)
		try:	# try to save list
			f = open(file, "wb")
			for i in data:
				f.write(i)
			f.close()
			print "%4s replaces: %s" % (count, file)
		except:
			print "! Error writing %s" % file
			try:
				f.close()
			except:
				pass
			renameFile(bak, file)
			print "* Do not worry, %s was not changed " % file
			import sys
			e = sys.exc_info()
			raise e[0], e[1], e[2]
		if not keepbackups:
			os.remove(bak)
	return count

def main():

	import distutils.filelist

	includeList=INCLUDE.split('|')
	excludeList=EXCLUDE.split('|')

	fl = distutils.filelist.FileList()
	fl.findall(DIR)

	for i in includeList:
		print "+ include pattern: '%s'" % i
		fl.include_pattern(i, anchor=0)

	for i in excludeList:
		if i:
			print "- exclude pattern: ", i
			fl.exclude_pattern(i)

	replaced = 0
	for f in fl.files:
		print f
		if replaceInFile(f, FIND_STRING, REPLACE_STRING, MATCH_CASE, MATCH_WHOLE_WORDS, BACKUP) > 0:
			replaced = replaced + 1

	print "%s files processed, %s replaced." % (len(fl.files), replaced)

if __name__=="__main__":
	main()
