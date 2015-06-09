#################################################################
# Program: Toolib
"""

"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2005/08/03 15:36:41 $"
__version__ = "$Revision: 1.10 $"
# $Source: D:/HOME/cvs/toolib/wx/Resources.py,v $
#
#################################################################
import os
import wx
from imagecaches import CachedImageList, BitmapCache

ICON_SIZE = (16,16)		# default icon size

class PickleStorage(object):
	def __init__(self, picklePath):
		self.__picklePath = picklePath

	def pickleFileName(self, key):
		return os.path.join(self.__picklePath, "%s.pik" % (key,))

	def loadObject(self, name):
		import pickle
		fname = self.pickleFileName(name)
		try:
			f = file(fname, 'rb')
		except: # File not found
			return None
		else:
			try:
				obj = pickle.load(f)
			except:
				# pickle error! Remove file
				f.close()
				os.remove(fname)
			else:
				f.close()
				return obj

	def saveObject(self, name, object):
		import pickle
		fname = self.pickleFileName(name)
		f = file(fname, 'wb')
		pickle.dump(object, f, 1)
		f.close()

class Resources(object):
	"""
	Resouces class, usually singleton, stored in core
	"""
	def __init__(self, imagesPath, iconSize=ICON_SIZE):
		self.__imagesPath = imagesPath
		self.__iconCache = None
		self.__bitmapCache = None
		self.__iconSize = iconSize
		self.__emptyBitmap = None

	def getProjectPath(self):
		return self.__projectPath

	def getImagesPath(self):
		return self.__imagesPath

	def getIconCache(self):
		if self.__iconCache is None:
			self.__iconCache = CachedImageList(self.__imagesPath, ICON_SIZE[0], ICON_SIZE[1])
		return self.__iconCache

	def getBitmapCache(self):
		if self.__bitmapCache is None:
			self.__bitmapCache = BitmapCache(self.__imagesPath)
		return self.__bitmapCache

	def getBitmap(self, imageName, default=None):
		return self.getBitmapCache().get(imageName, default)

	def getEmptyBitmap(self):
		if self.__emptyBitmap is None:
			self.__emptyBitmap = wx.EmptyBitmap(0,0)
		return self.__emptyBitmap

