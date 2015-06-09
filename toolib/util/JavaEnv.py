#################################################################
# Program:   Toolib												#
"""
Environment to create Java Processes
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2006/11/22 17:58:18 $"
__version__ = "$Revision: 1.3 $"
# $Source: D:/HOME/cvs/toolib/util/JavaEnv.py,v $
#																#
#################################################################

import sys, os
from Process import Process
import toolib.debug as debug

__all__ = [ "JavaEnv" ]

def winOrUnix(windowsRet, unixRet):
	if sys.platform[:3] == "win":
		return windowsRet
	else:
		return unixRet

class JavaEnv:
	def __init__(self, java_home=None, app_home=None, classpath = [], options=[]):
		self._java_home = java_home or os.environ["JAVA_HOME"]
		self._app_home = app_home
		self._classpath = classpath
		self._options = options

	def getJavaHome(self):
		return self._java_home

	def getClassPath(self):
		"""
		returns list of pathes
		"""
		return self._classpath

	def getOptions(self):
		"""
		returns list of options
		"""
		return self._options

	def getClassPathString(self, additional=[]):
		cp = self._classpath + additional
		res = []
		for p in cp:
			if not os.path.isabs(p):
				p = "%s/%s" % (self._app_home, p)
			if os.path.exists(p):
				res.append(p)
			else:
				debug.warning("* Jar not found: %s. Removed from classpath" % p)
		return winOrUnix(";", ":").join(res)

	def getJavaBinary(self):
		return "%s/bin/%s" % (self._java_home, winOrUnix("java.exe", "java"))

	def getCommandLine(self, javaClass, arguments=[], additional_classpath=[], additional_options=[]):
		cmds = ( 
			  [self.getJavaBinary(), "-classpath", self.getClassPathString(additional_classpath)]
			+ self._options + additional_options
			+ [javaClass]
			+ arguments
			)
		return " ".join(cmds)
		

	def execute(self, javaClass, arguments=[], additional_classpath=[], additional_options=[], mode='t', separate_stderr=1):
		cmd = self.getCommandLine(javaClass, arguments, additional_classpath, additional_options)
		assert debug.trace("execute: %s" % cmd)
		return Process(cmd, mode=mode, separate_stderr=separate_stderr)


if __name__ == "__main__":
	env = JavaEnv("e:/pro/jdk1.3.1", "e:/pro/xt", ["xt.jar", "./lib/xp.jar", "./lib/xml-apis.jar", "1.jar"])
	p = env.execute("com.jclark.xsl.sax.Driver")
	print "".join(p.getErrorStream().readlines())
