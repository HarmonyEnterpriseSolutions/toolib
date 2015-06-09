import traceback
import os
import wx
from wx.lib.embeddedimage import PyEmbeddedImage

try:
	import wx.lib.agw.customtreectrl as customtreectrl
except ImportError:
	import wx.lib.customtreectrl as customtreectrl

#####################################################################################################
# Fixing bug with styles conflict
#
"""

Window Styles
=============

This class supports the following window styles:

============================== =========== ==================================================
Window Styles                  Hex Value   Description
============================== =========== ==================================================
``TR_NO_BUTTONS``                      0x0 For convenience to document that no buttons are to be drawn.
``TR_SINGLE``                          0x0 For convenience to document that only one item may be selected at a time. Selecting another item causes the current selection, if any, to be deselected. This is the default.
``TR_HAS_BUTTONS``                     0x1 Use this style to show + and - buttons to the left of parent items.
``TR_NO_LINES``                        0x4 Use this style to hide vertical level connectors.
``TR_LINES_AT_ROOT``                   0x8 Use this style to show lines between root nodes. Only applicable if ``TR_HIDE_ROOT`` is set and ``TR_NO_LINES`` is not set.
``TR_DEFAULT_STYLE``                   0x9 The set of flags that are closest to the defaults for the native control for a particular toolkit.
``TR_TWIST_BUTTONS``                  0x10 Use old Mac-twist style buttons.
``TR_MULTIPLE``                       0x20 Use this style to allow a range of items to be selected. If a second range is selected, the current range, if any, is deselected.
``TR_EXTENDED``                       0x40 Use this style to allow disjoint items to be selected. (Only partially implemented; may not work in all cases).
``TR_HAS_VARIABLE_ROW_HEIGHT``        0x80 Use this style to cause row heights to be just big enough to fit the content. If not set, all rows use the largest row height. The default is that this flag is unset.
``TR_EDIT_LABELS``                   0x200 Use this style if you wish the user to be able to edit labels in the tree control.
``TR_ROW_LINES``                     0x400 Use this style to draw a contrasting border between displayed rows.
``TR_HIDE_ROOT``                     0x800 Use this style to suppress the display of the root node, effectively causing the first-level nodes to appear as a series of root nodes.
``wx.gizmos.TR_COLUMN_LINES``       0x1000
``wx.gizmos.TR_VIRTUAL``            0x4000 conflict !!!
``TR_FULL_ROW_HIGHLIGHT``           0x2000 Use this style to have the background colour and the selection highlight extend  over the entire horizontal row of the tree control window.
``TR_AUTO_CHECK_CHILD``             0x4000 Only meaningful foe checkbox-type items: when a parent item is checked/unchecked its children are checked/unchecked as well.
``TR_AUTO_TOGGLE_CHILD``            0x8000 Only meaningful foe checkbox-type items: when a parent item is checked/unchecked its children are toggled accordingly.
``TR_AUTO_CHECK_PARENT``           0x10000 Only meaningful foe checkbox-type items: when a child item is checked/unchecked its parent item is checked/unchecked as well.
``TR_ALIGN_WINDOWS``               0x20000 Flag used to align windows (in items with windows) at the same horizontal position.


============================== =========== ==================================================
"""
import wx.gizmos
if wx.gizmos.TR_VIRTUAL == customtreectrl.TR_AUTO_CHECK_CHILD:
	#rint "* fixing TR_AUTO_CHECK_CHILD vs TR_VIRTUAL conflict"
	customtreectrl.TR_AUTO_CHECK_CHILD  = 0x10000
	customtreectrl.TR_AUTO_TOGGLE_CHILD = 0x20000
	customtreectrl.TR_AUTO_CHECK_PARENT = 0x40000
	customtreectrl.TR_ALIGN_WINDOWS     = 0x80000

#####################################################################################################

try:
	from wx.lib.agw.customtreectrl import *
except ImportError:
	from wx.lib.customtreectrl import *

if hasattr(CustomTreeCtrl, 'GetControlBmp'):

	# 16 x 16 images

	Checked = PyEmbeddedImage(
		"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAMZJ"
		"REFUOI2lkz0KAjEQhd97s7fwBHYiCGLhFbSwsNGbWHkA8SZa2HgASxER9AKeQ4t1soFNdpEd"
		"CBkm+SbzkyFl6CLqRAMoXOnNNp9/4fdxyyI2XParoJOCVC4zg2Rhl4T+egcgk0IbLFVYzUET"
		"PDgMf2eWdtAGAwhRJB04PDlPk7DfIZl3YFaGNzqNa/Br+QTJfAT+oksOJrMplGHf5tfYXIOz"
		"KcSteizuWbihBlWfJWuFk0V02KvdBAPRLAAI3/MfYddx/gKqcR/ADJsz+gAAAABJRU5ErkJg"
		"gg==")

	NotChecked = PyEmbeddedImage(
		"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAI1J"
		"REFUOI2lk8ENgzAMRf//9hYdgWF65NpFOHHsqaOwAcswRzlQIFIJOMRSFCvKe7Ism5ShJlRF"
		"A/A1eTy7byk8DT09fRjf7ZZL+h2DmcPM4L7ckqF5fZZ/R+YrWNqxP0EEVtJ43YGzFUThE0EM"
		"zgqi8IkgBpMZQRQmma+gBD5sYgkMJLsAYBvPkmDtOs9/uQs8PMn4RwAAAABJRU5ErkJggg==")

	Flagged = PyEmbeddedImage(
		"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAflJ"
		"REFUOI2lk99Lk1EYx7/nObvahUK7cyNkrA1piOg0BokFvSAiDJftIrpof4E5uoqBCIlFUuyy"
		"27Ag3I1TunmjhGplThYZL7UwL14EV2yxzb1zzvF0oy+81fqBXzhX5/l+zvc55zlCkMRxRMdy"
		"A7C12oglkqxmciiUDDja7VACXtydGBc/14nfteAMxXlkwAOlz42ArwPZzTzU9S0spT9ie/Gm"
		"+CMgcuM+hwd9OOs/CSKClBJEElJKvPyg4/GzDTycjpoQyx04Q/GWZiKJcz1uXL7QA2cozr8A"
		"Yokkjwx4THNDNPC8vILoRhSLegq1Zg1EhPO9HoSHuhFLJNkCUNdyUPrc5smvd98gWV+AYavi"
		"tnYLqS8pEEkQEUaDXVDXctYEhbKBgK/DjDuvz6NQLKJqGNirNzD39g6ICEIIBP2dKJQNK8DR"
		"Zkd2M2/2fNExjp3tHXzNf0O59B2x3usQQoCIsKrpcLTZrQCl3wt1fctMMOwaxjXPJGjXhpkz"
		"s4icjhwmICynNSj93sN3JGku19gUL73IcqVS4mq1wrWawfX6Hu/v1/ngoMHNZpOfZj6xa2yK"
		"jzwWgCCJK9MP+Mmr9y3NV2cescXTahLDQ90YDXYh6O/EqqZjOa0hufLu75N4pMnEAquZzyiW"
		"DJxot0MJnMK9iUv/9hf+Rz8AshHWKLtawgYAAAAASUVORK5CYII=")

	NotFlagged = PyEmbeddedImage(
		"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAX5J"
		"REFUOI2lk7FLQlEUh3/v3Dc5OLiFDiK9QUpK5A0WVCCC4CBGLbVE/0C4NQgS1BxOzS1B2FLY"
		"ZIJBSGhRQvEIQQRrE0MtrUxOS0qvekl14HKHe7+Pc+/9XUkigf8U/YsGIBstROIJTuWLqDVa"
		"sJhN8KsKNlfmpc/7pO+OYA1FOaA64HPb4VGGUChVkb4oI3l6g7v9delHwdzqFocnFUyM2EAk"
		"IIQMIQRkWUb2+ha7mSvsrC33Jbo7sIaihrAQAtPjDiz4xmANRfmLIBJPcEB1GMJEAkSEGfcw"
		"ZqdciMQTrBOk8kX43PYf4d4c9DqRyhf1HdQaLXiUoYEwEcE7aket0dILLGYTCqXqQJiIkNMq"
		"sJhNeoFfVZC+KA+EiQjJrAa/qry/I4n+sIVjfHB8zvX6PTebdX58fOB2u8XPz0/c6bxwt/vK"
		"R2c3bAvHuMfoBBIJLK5t8+HJpSG8tLHDOsYoibNTLgS9TnhH7chpFSSzGvYyl4OT+DEXf/4L"
		"v6k3SsulH1+ZQhYAAAAASUVORK5CYII=")

	HalfChecked = PyEmbeddedImage(
		"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAP1J"
		"REFUOI1jZGRiZqAEMFGkm4GBgQXGkPav/U+q5qcbmxlZkAUOdIfD2UxMTFDMzMDMzMLAzMzM"
		"wMICoZmYmBm0EyZC1GEzmZBmJiaENgwDiNHMhBTwTPg0H/l+hCH1eirDlmdbUTTjdAG65jU/"
		"VzN8Y/nK0Hmtg2Hl7ZVIhuA0AOHsJY+XMLx9947h67dvDD9+/mboOdWN5EIcBiD7OVg4hOHF"
		"0xcMr16+Zvj08T1DkVEJMQYgAixQPpChQKWQgekLC0OreTtDomEiXDMjI0IbSjpAD+1ozRiG"
		"WO04FJsZGZkYGBkZcbsAPbTxacYaiKRoxvACLHmSAhgpzc4AZkA5MrlvgsQAAAAASUVORK5C"
		"YII=")
else:

	# 13 x 13
	
	HalfChecked = PyEmbeddedImage(
	    "iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAABHNCSVQICAgIfAhkiAAAAOZJ"
	    "REFUKJFjlAls+M9AImBhYGBgONAdDhdgYmKCYmYGZmYWBmZmZgYWFgjNxMTMoJ0wkYEJ2QRC"
	    "GpiYIMqZSNHAxMSM0ISu4cj3Iwyp11MZtjzbiqIBxSZ0DWt+rmb4xvKVofNaB8PK2yuRNKJo"
	    "QjhpyeMlDG/fvWP4+u0bw4+fvxl6TnUjuQRJE7IfgoVDGF48fcHw6uVrhk8f3zMUGZXg0oTw"
	    "dKB8IEOBSiED0xcWhlbzdoZEw0S4BkZGJkQ8oYdStGYMQ6x2HIoNjIxMDIyMjKg2oYcSLg0o"
	    "AUGsBgYGBgZGctIeAFbpN9iWnQaVAAAAAElFTkSuQmCC")

TreeItemIcon_HalfChecked = 4


class AlmostFalse(object):

	def __nonzero__(self):
		return False
	
	def __str__(self):
		return self.__class__.__name__

	__repr__ = __str__
	
	def __eq__(self, v):
		return v is False or v is 0


AlmostFalse = AlmostFalse()


BaseCustomTreeCtrl = CustomTreeCtrl
class CustomTreeCtrl(BaseCustomTreeCtrl):
	
	def __init__(self, *args, **kwargs):
		BaseCustomTreeCtrl.__init__(self, *args, **kwargs)

	def GetControlBmp(self, checkbox=True, checked=False, enabled=True, 
			halfChecked=False,	# this is my one
			**argw				# ignore other
		):
		"""
		bring back my nice checkboxes to me
		"""
		if checkbox:
			if checked:
				ei = Checked
			elif halfChecked:
				ei = HalfChecked
			else:
				ei = NotChecked
		else:
			if checked:
				ei = Flagged
			else:
				ei = NotFlagged
				
		bmp = ei.getBitmap()

		if not enabled:

			image = wx.ImageFromBitmap(bmp)
			image = GrayOut(image)
			bmp = wx.BitmapFromImage(image)

		return bmp

	def SetImageListCheck(self, *args, **kwargs):
		"""
		add half checked image to image lists
		"""
		BaseCustomTreeCtrl.SetImageListCheck(self, *args, **kwargs)
		self._imageListCheck .Add(self.GetControlBmp(checkbox=True, checked=False, halfChecked=True, enabled=True ))
		self._grayedCheckList.Add(self.GetControlBmp(checkbox=True, checked=False, halfChecked=True, enabled=False))

	def AutoCheckParent(self, item, checked):
		"""Traverses up the tree and checks/unchecks parent items.
		Meaningful only for check items."""

		if not item:
			raise Exception("\nERROR: Invalid Tree Item. ")

		parent = item.GetParent()
		if not parent or parent.GetType() != 1:
			return

		almost = False
		(child, cookie) = self.GetFirstChild(parent)
		while child:
			if child.GetType() == 1 and child.IsEnabled():
				if checked != child.IsChecked():
					almost = True
					break
			(child, cookie) = self.GetNextChild(parent, cookie)

		self.CheckItem2(parent, AlmostFalse if almost else checked, torefresh=True)
		self.AutoCheckParent(parent, checked)

	def SetFocus(self):
		# BUGFIX: eliminate SetFocus called from CustomTreeCtrl __init__
		file, line, fn, code = traceback.extract_stack()[-2]
		if (
			    not (os.path.sep.join(('wx','lib','customtreectrl'))       in file and fn == '__init__') 
			and not (os.path.sep.join(('wx','lib','agw','customtreectrl')) in file and fn == '__init__')
			and not (os.path.sep.join(('wx','lib','agw','hypertreelist'))  in file and fn == '__init__')
		):
			super(CustomTreeCtrl, self).SetFocus()


BaseGenericTreeItem = GenericTreeItem
class GenericTreeItem(BaseGenericTreeItem):

	def __init__(self, *args, **kwargs):
		BaseGenericTreeItem.__init__(self, *args, **kwargs)

	def GetCurrentCheckedImage(self):
		if self.IsChecked() is AlmostFalse:
			return TreeItemIcon_HalfChecked
		else:
			return BaseGenericTreeItem.GetCurrentCheckedImage(self)

# monkey patching, no other way to set GenericTreeItem
customtreectrl.CustomTreeCtrl = CustomTreeCtrl
customtreectrl.GenericTreeItem = GenericTreeItem

del customtreectrl
