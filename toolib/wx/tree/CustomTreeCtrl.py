"""
Fixes CustomTreeCtrl to be more like TreeCtrl
"""

import wx
from wx.lib.customtreectrl import CustomTreeCtrl



class CustomTreeCtrl(CustomTreeCtrl):
	

	def AppendItem(self, *args, **kwargs):
		# fix attribute selImage
		try:
			kwargs['selImage'] = kwargs.pop('selectedImage')
		except KeyError:
			pass
		return super(CustomTreeCtrl, self).AppendItem(*args, **kwargs)
