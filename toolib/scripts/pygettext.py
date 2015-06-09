#! /usr/local/bin/python
# -*- coding: Cp1251 -*-
# Originally written by Barry Warsaw <barry@zope.com>
#
# Minimally patched to make it even more xgettext compatible
# by Peter Funk <pf@artcom-gmbh.de>
#
# Options --join-existing, --recursive, wildcards in filenames
# added by Oleg Noga <noga@ukr.net> on 2003-02-18

"""pygettext -- Python equivalent of xgettext(1)

Many systems (Solaris, Linux, Gnu) provide extensive tools that ease the
internationalization of C programs.  Most of these tools are independent of
the programming language and can be used from within Python programs.  Martin
von Loewis' work[1] helps considerably in this regard.

There's one problem though; xgettext is the program that scans source code
looking for message strings, but it groks only C (or C++).  Python introduces
a few wrinkles, such as dual quoting characters, triple quoted strings, and
raw strings.  xgettext understands none of this.

Enter pygettext, which uses Python's standard tokenize module to scan Python
source code, generating .po files identical to what GNU xgettext[2] generates
for C and C++ code.  From there, the standard GNU tools can be used.

A word about marking Python strings as candidates for translation.  GNU
xgettext recognizes the following keywords: gettext, dgettext, dcgettext, and
gettext_noop.  But those can be a lot of text to include all over your code.
C and C++ have a trick: they use the C preprocessor.  Most internationalized C
source includes a #define for gettext() to _() so that what has to be written
in the source is much less.  Thus these are both translatable strings:

	gettext("Translatable String")
	_("Translatable String")

Python of course has no preprocessor so this doesn't work so well.  Thus,
pygettext searches only for _() by default, but see the -k/--keyword flag
below for how to augment this.

 [1] http://www.python.org/workshops/1997-10/proceedings/loewis.html
 [2] http://www.gnu.org/software/gettext/gettext.html

NOTE: pygettext attempts to be option and feature compatible with GNU xgettext
where ever possible.  However some options are still missing or are not fully
implemented.  Also, xgettext's use of command line switches with option
arguments is broken, and in these cases, pygettext just defines additional
switches.

Usage: pygettext [options] <inputfile> ...

Options:

	-a
	--extract-all
		Extract all strings.

	-d name
	--default-domain=name
		Rename the default output file from messages.po to name.po.

	-E
	--escape
		Replace non-ASCII characters with octal escape sequences.

	-j
	--join-existing
		join messages with existing file

	-r
	--recursive
		list files recursive (not GNU gettext compatible)

	-D
	--docstrings
		Extract module, class, method, and function docstrings.  These do not
		need to be wrapped in _() markers, and in fact cannot be for Python to
		consider them docstrings. (See also the -X option).

	-h
	--help
		Print this help message and exit.

	-k word
	--keyword=word
		Keywords to look for in addition to the default set, which are:
		%(DEFAULTKEYWORDS)s

		You can have multiple -k flags on the command line.

	-K
	--no-default-keywords
		Disable the default set of keywords (see above).  Any keywords
		explicitly added with the -k/--keyword option are still recognized.

	--no-location
		Do not write filename/lineno location comments.

	-n
	--add-location
		Write filename/lineno location comments indicating where each
		extracted string is found in the source.  These lines appear before
		each msgid.  The style of comments is controlled by the -S/--style
		option.  This is the default.

	-o filename
	--output=filename
		Rename the default output file from messages.po to filename.  If
		filename is `-' then the output is sent to standard out.

	-p dir
	--output-dir=dir
		Output files will be placed in directory dir.

	-S stylename
	--style stylename
		Specify which style to use for location comments.  Two styles are
		supported:

		Solaris  # File: filename, line: line-number
		GNU		 #: filename:line

		The style name is case insensitive.  GNU style is the default.

	-v
	--verbose
		Print the names of the files being processed.

	-V
	--version
		Print the version of pygettext and exit.

	-w columns
	--width=columns
		Set width of output to columns.

	-x filename
	--exclude-file=filename
		Specify a file that contains a list of strings that are not be
		extracted from the input files.  Each string to be excluded must
		appear on a line by itself in the file.

	-X filename
	--no-docstrings=filename
		Specify a file that contains a list of files (one per line) that
		should not have their docstrings extracted.  This is only useful in
		conjunction with the -D option above.

<inputfile>:
	`-` is standard input.
	supports path and wildcard in file name

Examples:
	gettext -j -r /foo/bar/*.py
		Join existing message.po with all .py files in /foo/bar directory
		and subdirectories
"""

import os
import sys
import time
import getopt
import tokenize
import operator
from distutils.filelist import FileList

# for selftesting
try:
	import fintl
	_ = fintl.gettext
except ImportError:
	def _(s): return s

__version__ = '1.4'

default_keywords = ['_', 'u_']
DEFAULTKEYWORDS = ', '.join(default_keywords)

EMPTYSTRING = ''



# The normal po-file header. msgmerge and Emacs's po-mode work better if it's
# there.

pot_comment = '''\
# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR ORGANIZATION
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
'''

pot_header = '''\
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\\n"
"POT-Creation-Date: %(time)s\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language-Team: LANGUAGE <LL@li.org>\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=CHARSET\\n"
"Content-Transfer-Encoding: ENCODING\\n"
"Generated-By: pygettext.py %(version)s\\n"

'''


def usage(code, msg=''):
	if code:
		fd = sys.stderr
	else:
		fd = sys.stdout
	print >> fd, __doc__ % globals()
	if msg:
		print >> fd, msg
	sys.exit(code)



escapes = []

def make_escapes(use_escapes):
	global escapes
	if use_escapes:
		# Allow iso-8859 characters to pass through so that e.g. 'msgid
		# "H�he"' would result not result in 'msgid "H\366he"'.  Otherwise we
		# escape any character outside the 32..126 range.
		max = 128
	else:
		max = 256

	for i in range(256):
		if 32 <= i < max:
			escapes.append(chr(i))
		else:
			escapes.append("\\%03o" % i)
	escapes[ord('\\')] = '\\\\'
	escapes[ord('\t')] = '\\t'
	escapes[ord('\r')] = '\\r'
	escapes[ord('\n')] = '\\n'
	escapes[ord('\"')] = '\\"'

def escape(s):
	global escapes
	s = list(s)
	for i in range(len(s)):
		s[i] = escapes[ord(s[i])]
	return EMPTYSTRING.join(s)


def safe_eval(s):
	# unwrap quotes, safely
	return eval(s, {'__builtins__':{}}, {})


def normalize(s):
	# This converts the various Python string types into a format that is
	# appropriate for .po files, namely much closer to C style.
	lines = s.split('\n')
	if len(lines) == 1:
		s = '"' + escape(s) + '"'
	else:
		if not lines[-1]:
			del lines[-1]
			lines[-1] = lines[-1] + '\n'
		for i in range(len(lines)):
			lines[i] = escape(lines[i])
		lineterm = '\\n"\n"'
		s = '""\n"' + lineterm.join(lines) + '"'
	return s

def denormalize(s):
	code = '("""%s""")' % (s,)
	try:
		res = eval(code)
		return res
	except:
		print >> sys.stderr, '! Error evaluating string: [%s]' % (code,)
		return ''

def readPoMessage(line, file):
	"""
	returns:
		(<result text>, <translation first line>,)
	"""
	# line starts with msgid
	if line.startswith('msgid'):
		line = line[5:].strip()
	elif line.startswith('msgstr'):
		line = line[6:].strip()
	else: raise ValueError, "Expected msgid or msgtxt"

	text = []

	while line and line.lstrip().startswith('"'):
		text.append(denormalize(line.strip()[1:-1]))
		line = file.readline()  # read next line

	return "".join(text), line

class TokenEater:
	def __init__(self, options):
		self.__options = options
		self.__messages = {}
		self.__translations = {}
		self.__state = self.__waiting
		self.__data = []
		self.__lineno = -1
		self.__freshmodule = 1
		self.__curfile = None

	def loadPoFile(self, f):
		line = f.readline()
		while line:
			if line.startswith("msgid"):
				msgid, line = readPoMessage(line, f)
				while line and not line.startswith("msgstr"):
					line = f.readline()
				if line:
					msgstr, line = readPoMessage(line, f)
					if msgstr:
						self.__translations[msgid] = msgstr
			else:
				line = f.readline()
		#print ' ', "%d translation(s) loaded" % len(self.__translations.keys())
		#for k in self.__translations.keys():
		#   print 'msgid: [%s]' % k
		#   print 'msgstr: {%s}' % self.__translations[k]

	def __call__(self, ttype, tstring, stup, etup, line):
		# dispatch
##		  import token
##		  print >> sys.stderr, 'ttype:', token.tok_name[ttype], \
##				'tstring:', tstring
		self.__state(ttype, tstring, stup[0])

	def __waiting(self, ttype, tstring, lineno):
		opts = self.__options
		# Do docstring extractions, if enabled
		if opts.docstrings and not opts.nodocstrings.get(self.__curfile):
			# module docstring?
			if self.__freshmodule:
				if ttype == tokenize.STRING:
					self.__addentry(safe_eval(tstring), lineno, isdocstring=1)
					self.__freshmodule = 0
				elif ttype not in (tokenize.COMMENT, tokenize.NL):
					self.__freshmodule = 0
				return
			# class docstring?
			if ttype == tokenize.NAME and tstring in ('class', 'def'):
				self.__state = self.__suiteseen
				return
		if ttype == tokenize.NAME and tstring in opts.keywords:
			self.__state = self.__keywordseen

	def __suiteseen(self, ttype, tstring, lineno):
		# ignore anything until we see the colon
		if ttype == tokenize.OP and tstring == ':':
			self.__state = self.__suitedocstring

	def __suitedocstring(self, ttype, tstring, lineno):
		# ignore any intervening noise
		if ttype == tokenize.STRING:
			self.__addentry(safe_eval(tstring), lineno, isdocstring=1)
			self.__state = self.__waiting
		elif ttype not in (tokenize.NEWLINE, tokenize.INDENT,
						   tokenize.COMMENT):
			# there was no class docstring
			self.__state = self.__waiting

	def __keywordseen(self, ttype, tstring, lineno):
		if ttype == tokenize.OP and tstring == '(':
			self.__data = []
			self.__lineno = lineno
			self.__state = self.__openseen
		else:
			self.__state = self.__waiting

	def __openseen(self, ttype, tstring, lineno):
		if ttype == tokenize.OP and tstring == ')':
			# We've seen the last of the translatable strings.  Record the
			# line number of the first line of the strings and update the list
			# of messages seen.  Reset state for the next batch.  If there
			# were no strings inside _(), then just ignore this entry.
			if self.__data:
				self.__addentry(EMPTYSTRING.join(self.__data))
			self.__state = self.__waiting
		elif ttype == tokenize.STRING:
			self.__data.append(safe_eval(tstring))
		# TBD: should we warn if we seen anything else?

	def __addentry(self, msg, lineno=None, isdocstring=0):
		if lineno is None:
			lineno = self.__lineno
		if not msg in self.__options.toexclude:
			entry = (self.__curfile, lineno)
			self.__messages.setdefault(msg, {})[entry] = isdocstring

	def set_filename(self, filename):
		self.__curfile = filename
		self.__freshmodule = 1

	def write(self, fp):
		"""
		returns (<messages count> <unjoined messages>)
		"""
		msg_count = 0
		trans_count = 0
		options = self.__options
		timestamp = time.ctime(time.time())
		# The time stamp in the header doesn't have the same format as that
		# generated by xgettext...
		print >> fp, pot_comment % {'time': timestamp, 'version': __version__}

		header = self.__translations.get("")
		if header:
			print >> fp, 'msgid ""'
			print >> fp, 'msgstr %s\n' % normalize(header)
		else:
			print >> fp, pot_header % {'time': timestamp, 'version': __version__}

		# Sort the entries.  First sort each particular entry's keys, then
		# sort all the entries by their first item.
		reverse = {}
		for k, v in self.__messages.items():
			keys = v.keys()
			keys.sort()
			reverse.setdefault(tuple(keys), []).append((k, v))
		rkeys = reverse.keys()
		rkeys.sort()
		for rkey in rkeys:
			rentries = reverse[rkey]
			rentries.sort()
			for k, v in rentries:
				isdocstring = 0
				# If the entry was gleaned out of a docstring, then add a
				# comment stating so.  This is to aid translators who may wish
				# to skip translating some unimportant docstrings.
				if reduce(operator.__add__, v.values()):
					isdocstring = 1
				# k is the message string, v is a dictionary-set of (filename,
				# lineno) tuples.  We want to sort the entries in v first by
				# file name and then by line number.
				v = v.keys()
				v.sort()
				if not options.writelocations:
					pass
				# location comments are different b/w Solaris and GNU:
				elif options.locationstyle == options.SOLARIS:
					for filename, lineno in v:
						d = {'filename': filename, 'lineno': lineno}
						print >>fp, '# File: %(filename)s, line: %(lineno)d' % d
				elif options.locationstyle == options.GNU:
					# fit as many locations on one line, as long as the
					# resulting line length doesn't exceeds 'options.width'
					locline = '#:'
					for filename, lineno in v:
						d = {'filename': filename, 'lineno': lineno}
						s = ' %(filename)s:%(lineno)d' % d
						if len(locline) + len(s) <= options.width:
							locline = locline + s
						else:
							print >> fp, locline
							locline = "#:" + s
					if len(locline) > 2:
						print >> fp, locline
				if isdocstring:
					print >> fp, '#, docstring'
				print >> fp, 'msgid', normalize(k)
				trans = self.__translations.get(k, "")
				print >> fp, ('msgstr %s\n' % normalize(trans))
				if k:
					msg_count += 1
					if trans: trans_count += 1
		return (msg_count, trans_count)

def list_files(path):
	res = []
	files = os.listdir(path)
	for file in files:
		full=os.path.join(path, file)
		if not os.path.isdir(full):
			res.append(full)
	return res

def pass_file(filename, eater):
	print "  Processing", filename
	if filename == '-':
		fp = sys.stdin
	else:
		try:
			fp = open(filename, 'r')
		except IOError:
			print >> sys.stderr, '! Error opening file:', filename
			return
	eater.set_filename(filename)
	try:
		tokenize.tokenize(fp.readline, eater)
	except tokenize.TokenError, e:
		print >> sys.stderr, '%s: %s, line %d, column %d' % (
			e[0], filename, e[1][0], e[1][1])
	if fp != sys.stdin:
		fp.close()

def main():
	global default_keywords
	try:
		opts, args = getopt.getopt(
			sys.argv[1:],
			'ad:DEhk:Kno:p:S:Vvw:x:X:jr',
			['extract-all', 'default-domain=', 'escape', 'help',
			 'keyword=', 'no-default-keywords',
			 'add-location', 'no-location', 'output=', 'output-dir=',
			 'style=', 'verbose', 'version', 'width=', 'exclude-file=',
			 'docstrings', 'no-docstrings', '--join-existing', '--recursive',
			 ])
	except getopt.error, msg:
		usage(1, msg)

	# for holding option values
	class Options:
		# constants
		GNU = 1
		SOLARIS = 2
		# defaults
		extractall = 0 # FIXME: currently this option has no effect at all.
		escape = 0
		keywords = []
		outpath = ''
		outfile = 'messages.po'
		writelocations = 1
		locationstyle = GNU
		verbose = 0
		width = 78
		excludefilename = ''
		docstrings = 0
		nodocstrings = {}
		joinexisting = 0
		recursive = 0

	options = Options()
	locations = {'gnu' : options.GNU,
				 'solaris' : options.SOLARIS,
				 }

	# parse options
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			usage(0)
		elif opt in ('-a', '--extract-all'):
			options.extractall = 1

		#@ Oleg, options added
		elif opt in ('-j', '--join-existing'):
			options.joinexisting = 1
		elif opt in ('-r', '--recursive'):
			options.recursive = 1

		elif opt in ('-d', '--default-domain'):
			options.outfile = arg + '.po'
		elif opt in ('-E', '--escape'):
			options.escape = 1
		elif opt in ('-D', '--docstrings'):
			options.docstrings = 1
		elif opt in ('-k', '--keyword'):
			options.keywords.append(arg)
		elif opt in ('-K', '--no-default-keywords'):
			default_keywords = []
		elif opt in ('-n', '--add-location'):
			options.writelocations = 1
		elif opt in ('--no-location',):
			options.writelocations = 0
		elif opt in ('-S', '--style'):
			options.locationstyle = locations.get(arg.lower())
			if options.locationstyle is None:
				usage(1, 'Invalid value for --style: %s' % arg)
		elif opt in ('-o', '--output'):
			options.outfile = arg
		elif opt in ('-p', '--output-dir'):
			options.outpath = arg
		elif opt in ('-v', '--verbose'):
			options.verbose = 1
		elif opt in ('-V', '--version'):
			print 'pygettext.py (xgettext for Python) %s' % __version__
			sys.exit(0)
		elif opt in ('-w', '--width'):
			try:
				options.width = int(arg)
			except ValueError:
				usage(1, '--width argument must be an integer: %s' % arg)
		elif opt in ('-x', '--exclude-file'):
			options.excludefilename = arg
		elif opt in ('-X', '--no-docstrings'):
			fp = open(arg)
			try:
				while 1:
					line = fp.readline()
					if not line:
						break
					options.nodocstrings[line[:-1]] = 1
			finally:
				fp.close()

	# calculate escapes
	make_escapes(options.escape)

	# calculate all keywords
	options.keywords.extend(default_keywords)

	# initialize list of strings to exclude
	if options.excludefilename:
		try:
			fp = open(options.excludefilename)
			options.toexclude = fp.readlines()
			fp.close()
		except IOError:
			print >> sys.stderr, '!', "Can't read exclude file:", options.excludefilename
			sys.exit(1)
	else:
		options.toexclude = []

	# slurp through all the files
	eater = TokenEater(options)
	filelist = FileList()

	for filename in args:
		##rint ">>", filename
		if filename == '-' or (not options.recursive and not (filename.find('*') == -1 or filename.find('?') == -1)):
			##print "pass single"
			pass_file(filename, eater)
		else:
			path, file = os.path.split(filename)
			##print ">> path=%s file=%s" % (path, file)
			if not path: path = os.curdir
			if options.recursive:
				##print ">> findall"
				filelist.findall(path)
				# replace 'file.ext' to './file.ext'
				# we will matching with '*/wildcard.ext'
				for i in range(len(filelist.allfiles)):
					__file = filelist.allfiles[i]
					if not os.path.isabs(__file):   # if not full path, windows or unixx
						filelist.allfiles[i] = '.' + os.sep + __file
			else:
				##print ">> list", list_files(path)
				filelist.set_allfiles(list_files(path))
			##print ">> all files", filelist.allfiles
			##print ">> pattern", file
			filelist.include_pattern(file, anchor=0)
			##print ">> final list", filelist.files

			for file in filelist.files:
				pass_file(file, eater)

	# write the output
	if options.outfile == '-':
		fp = sys.stdout
		closep = 0
	else:
		if options.outpath:
			options.outfile = os.path.join(options.outpath, options.outfile)
		#@Oleg + join - existing option
		if options.joinexisting:
			if os.path.exists(options.outfile): # if file not exist, -j has no efect
				print ' ', 'Processing', options.outfile
				try:
					f = open(options.outfile)
					eater.loadPoFile(f)
					f.close()
					bak = options.outfile + ".bak"
					if os.path.exists(bak): os.remove(bak)  # remove old backup
					os.rename(options.outfile, bak)			# backup old po file
				except Exception, e:
					print >> sys.stderr, '!', 'Join with existing message file failed:', e
			else:
				print >> sys.stderr, '*', 'No existing message file found. -j has no effect.'

		fp = open(options.outfile, 'w')
		closep = 1
	try:
		m, t = eater.write(fp)
		print ('Total messages:		  %4d\n'
			   'Translations:		  %4d\n'
			   'Untraslated messages: %4d' % (m,t,m-t))
	finally:
		if closep:
			fp.close()


if __name__ == '__main__':
	main()
