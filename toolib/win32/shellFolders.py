#################################################################
# Program: Toolib
"""

"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2009/09/03 18:57:58 $"
__version__ = "$Revision: 1.5 $"
# $Source: D:/HOME/cvs/toolib/win32/shellFolders.py,v $
#
#################################################################
from toolib.debug import deprecation
deprecation("use function toolib.win32.shell.getSpecialFolderPath")

import registry

__all__ = ["ShellFolders", "getShellFolder", "getUserShellFolder", "getCommonShellFolder"]

HKEY_SHELL_FOLDERS		  = "HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders";
HKEY_COMMON_SHELL_FOLDERS = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders";

class ShellFolders:
	def __init__(self, key):
		self.__hkey = key
		self.__regkey = None

	def getShellFolder(self, key, defVal=None):
		if self.__regkey is None:
			self.__regkey = registry.RegKey(None, self.__hkey)
		val = self.__regkey.value(key).getValue()
		if val is None:
			val = defVal
		return val

def getUserShellFolder(key, defVal = None):
	return shellFolders.getShellFolder(key, defVal)

def getCommonShellFolder(key, defVal = None):
	return commonShellFolders.getShellFolder(key, defVal)

def getShellFolder(key, defVal = None):
	val = shellFolders.getShellFolder(key, None)
	if val is None:
		val = commonShellFolders.getShellFolder(key, None)
	if val is None:
		val = defVal
	return val

# static
shellFolders = ShellFolders(HKEY_SHELL_FOLDERS)
commonShellFolders = ShellFolders(HKEY_COMMON_SHELL_FOLDERS)

if __name__ == '__main__':
	#import toolib.utils as utils
	#print utils.strdict(shellFolders)
	print getShellFolder("Common Desktop")

