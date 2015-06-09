#################################################################
# Program: Toolib
"""

"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2008/04/11 15:37:00 $"
__version__ = "$Revision: 1.9 $"
# $Source: D:/HOME/cvs/toolib/wx/imagecaches.py,v $
#
#################################################################

import os
import wx
from toolib.debug import *

__all__ = ["ImageLoader", "CachedImageList", "BitmapCache"]

class ImageLoader(object):
	def __init__(self, imagePath):
		self.imagePath = imagePath;

	def loadImage(self, imageName):
		"""
		Returns: wxImage image
		"""
		path = os.path.join(self.imagePath, str(imageName))
		if not os.path.exists(path) or not os.path.isfile(path):
			path = os.path.join(self.imagePath, "notfound.gif")
			if not os.path.exists(path) or not os.path.isfile(path):
				return None

		image = wx.Image(path)
		if image.Ok():
			return image
			

	def loadBitmap(self, imageName):
		"""
		Returns: wxBitmap bitmap
		"""
		#return wx.EmptyBitmap(0,0)
		image = self.loadImage(imageName)
		if image is not None:
			return wx.BitmapFromImage(image)


class CachedImageListStub(object):
		
	def getImageIndex(self, imageName):
		return -1
	
	def __nonzero__(self):
		return False

class CachedImageList(wx.ImageList, ImageLoader):
	"""
	wxImageList with lazy image loading
	has method getImageIndex
	"""

	def __init__(self, imagePath, width=16, height=16, mask=True):
		wx.ImageList.__init__(self, width, height, mask, 0)
		ImageLoader.__init__(self, imagePath)
		self.__imageIndexMap = {}

	def getImageIndex(self, imageName):
		"""
		Returns: int image index
		"""
		if imageName is None: return -1
		index = self.__imageIndexMap.get(imageName, None)
		if index is None:
			bitmap = self.loadBitmap(imageName)
			if bitmap is not None:
				index = self.Add(bitmap)
				self.__imageIndexMap[imageName] = index
			else:
				index = -1
		return index


class BitmapCache(ImageLoader):
	def __init__(self, imagePath):
		ImageLoader.__init__(self, imagePath)
		self.map = {}

	def get(self, imageName, default=None):
		"""
		Returns: int image index
		"""
		#return wx.EmptyBitmap(0,0)
		if imageName is None:
			return default
		bitmap = self.map.get(imageName, None)
		if bitmap is None:
			bitmap = self.loadBitmap(imageName)
			if bitmap is not None:
				self.map[imageName] = bitmap
			else:
				warning("Image resource not found: %s" % (imageName))
		return bitmap

	def __getitem__(self, key):
		val = self.get(key)
		if val is None:
			raise KeyError
		return val

# Static initialization
#wx.Image_AddHandler(wx.GIFHandler())
