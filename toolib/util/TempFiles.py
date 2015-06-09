#################################################################
# Program:   toolib
"""
	Generates temp file names and automatically 
	removes all potentially created temp files on __del__
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2005/08/03 13:26:49 $"
__version__ = "$Revision: 1.1 $"
# $Source: D:/HOME/cvs/toolib/util/TempFiles.py,v $
#																#
#################################################################

import os, sys, tempfile

from toolib.debug import *

class TempFiles(object):

	def __init__(self):
		self.__tempFiles = []

	def newTempFile(self, name):
		tf = tempfile.mktemp(name)
		self.__tempFiles.append(tf)
		return tf

	def removeTempFile(self, name):
		if os.path.exists(name): 
			try:
				os.remove(name)
				try:
					self.__tempFiles.remove(name)
				except ValueError:
					pass
			except OSError, e:
				warning("Can't remove temp file: %s (reason is %s)" % (name, strexc(e)))

	def removeTempFiles(self):
		for tf in self.__tempFiles:
			self.removeTempFile(tf)

	def __del__(self):
		self.removeTempFiles()
			
