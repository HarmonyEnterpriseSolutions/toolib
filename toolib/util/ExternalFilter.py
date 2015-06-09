#################################################################
# Program:   toolib
"""
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2008/03/20 19:03:07 $"
__version__ = "$Revision: 1.6 $"
# $Source: D:/HOME/cvs/toolib/util/ExternalFilter.py,v $
#																#
#################################################################

import os, sys
import Pump				as Pumn
from cStringIO		import StringIO
from Process		import Process
from TempFiles		import TempFiles
from toolib.debug	import *

class ExternalFilterException(Exception):
	pass

class ExternalFilter(TempFiles):

	def __init__(self, use_stdin=0, use_stdout=0, normalReturnCodes=(0,), separate_stderr=1, name="external filter", verbose=0):
		TempFiles.__init__(self)

		self.__use_stdin = use_stdin
		self.__use_stdout = use_stdout
		self.__separate_stderr = separate_stderr

		self.__normalReturnCodes = normalReturnCodes
		self.__name = name
		self.__verbose = verbose

	def handleErrorOutput(self, errStream):
		errors = errStream.read()
		if errors:
			raise ExternalFilterException, "stderr: %s" % errors

	def handleOutput(self, outStream):
		line = outStream.readline()
		while line:
			if self.__verbose: print "[%s] %s" % (self.__name, line),
			line = outStream.readline()

	def runExternalFilter(self, inputStream, outputStream):
		if self.__use_stdin:
			inFile = None
		else:
			inFile = self.newTempFile("%s.in" % self.__class__.__name__)
			Pump.stream2file(inputStream, inFile)

		if self.__use_stdout:
			outFile = None
		else:
			outFile = self.newTempFile("%s.out" % self.__class__.__name__)

		cmd = self.getCommandLine(inFile, outFile)

		try:
			assert trace("Starting %s: %s" % (self.__name, cmd))
			xfilter = Process(cmd, separate_stderr=self.__separate_stderr)
			if self.__use_stdin:
				assert trace("Writing file to %s stdin" % self.__name)
				Pump.stream2stream(inputStream, xfilter.getInputStream())
			
			if self.__use_stdout:
				# output 
				assert trace("Pumping %s stdout to outputStream" % self.__name)
				Pump.stream2stream(xfilter.getOutputStream(), outputStream)

				if self.__separate_stderr:
					assert trace("Handling %s stderr" % self.__name)
					self.handleErrorOutput(xfilter.getErrorStream())
			else:
				assert trace("Handling %s stdout" % self.__name)
				self.handleOutput(xfilter.getOutputStream())

				if self.__separate_stderr:
					assert trace("Handling %s stderr" % self.__name)
					self.handleErrorOutput(xfilter.getErrorStream())

			rc = xfilter.waitFor()
			assert trace("%s finished with exit code: 0x%X" % (self.__name, rc))
			if not (rc in self.__normalReturnCodes):
				raise ExternalFilterException, "Return code 0x%X" % (rc,)

			if not self.__use_stdout:
				if os.path.exists(outFile):
					try:
						if os.path.getsize(outFile) > 0:
							Pump.file2stream(outFile, outputStream, "b")
						else:
							raise ExternalFilterException, "Output file is empty: %s" % (outFile,)
					finally:
						self.removeTempFile(outFile)
				else:
					raise ExternalFilterException, "Output file not found: %s" % (outFile,)

		finally:
			if inFile is not None:
				self.removeTempFile(inFile)
				pass

		return rc

	def getCommandLine(self, inputFile, outputFile):
		raise NotImplementedError, 'abstract'

