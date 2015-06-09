import wx
import sys
from toolib.util import lang

"""
wxControlWithItems::Append
wxControlWithItems::Clear
wxControlWithItems::Delete
wxControlWithItems::FindString
wxControlWithItems::GetClientData
wxControlWithItems::GetClientObject
wxControlWithItems::GetCount
wxControlWithItems::GetSelection
wxControlWithItems::GetString
wxControlWithItems::GetStringSelection
wxControlWithItems::Insert
wxControlWithItems::IsEmpty
wxControlWithItems::Number
wxControlWithItems::Select
wxControlWithItems::SetClientData
wxControlWithItems::SetClientObject
wxControlWithItems::SetSelection
wxControlWithItems::SetString
wxControlWithItems::SetStringSelection
"""

class ObjectListCtrl(wx.ListCtrl):
	

	def __init__(self, *args, **kwargs):
		args, kwargs = lang.normalize_args(args, kwargs, 
			('parent', 'id', 'pos', 'size', 'style', 'validator', 'name')
		)
		self.__strfunc = kwargs.pop('strfunc', str)
		self.__imageNameFunc = kwargs.pop('imageNameFunc', lambda object: getattr(object, 'getImageName', lambda: 'noimage.gif')())

		self.__objects = []
		self.__iconCache = None
		wx.ListCtrl.__init__(self, *args, **kwargs)

	# Implement ControlWithItems interface

	def setIconCache(self, iconCache):
		self.__iconCahce = iconCache
		self.SetImageList(iconCahce.getImageList())

	def getIconCache(self, iconCache):
		return self.__iconCache

	def clear(self):
		"""
		wxControlWithItems::Clear
		"""
		del self.__objects[:]
		self.ClearAll()

	def append(self, object):
		"""
		wxControlWithItems::Append
		"""
		self.__objects.append(object)
		self.InsertImageStringItem(sys.maxint, self.__strfunc(object), self.__imageIndexFunc(object))

	def insert(self, index, object):
		"""
		wxControlWithItems::Insert
		"""
		self.__objects.insert(index, object)
		sell.InsertImageStringItem(index, self.__strfunc(object), self.__imageIndexFunc(object))

	def __delitem__(self, i):
		"""
		wxControlWithItems::Delete
		"""
		del self.__objects[i]
		self.DeleteItem(i)

	def __len__(self):
		"""
		wxControlWithItems::GetCount
		"""
		return len(self.__objects)
	
	def iterSelectedObjects(self):
		index = self.GetFirstSelected()
		while index != -1:
			yield self.__objects[index]
			index = self.GetNextSelected(index)

	def getSelectedObjects(self):
		return list(self.iterSelectedObjects())

	def __getitem__(self, i):
		"""
		wxControlWithItems::GetString
		"""
		return self.__objects[i]

	def __iter__(self):
		return iter(self.__objects)

	def getIndex(self, object):
		return self.__objects.index(object)


if __name__ == '__main__':
	import toolib.startup
	toolib.startup.hookStd()

	class O(object):
		def __init__(self, s):
			self.s = s

		def __str__(self):
			return self.s

	class TestApp(wx.PySimpleApp):
		def OnInit(self):
			from dbgenie.Storage import Storage

			s = Storage.newInstance('lider.config.hot')

			print 

			frame = wx.Dialog(None)

			from toolib.wx.Resources import Resources
			iconCache = Resources(r'z:\projects\lider\res\images\liderdb.mdb').getIconCache()


			def getImageIndex(property):
				return iconCache.getImageIndex(property.getClass().getId() + ".gif")


			lc = ObjectListCtrl(
				frame,

				imageIndexFunc = getImageIndex,

				style=wx.LC_REPORT 
					| wx.BORDER_SUNKEN
					#| wx.BORDER_NONE
					| wx.LC_EDIT_LABELS
					| wx.LC_SORT_ASCENDING
					#| wx.LC_NO_HEADER
					#| wx.LC_VRULES
					#| wx.LC_HRULES
					#| wx.LC_SINGLE_SEL


			)

			lc.SetSize(frame.GetClientSize())
			lc.SetImageList(iconCache.getImageList(), wx.IMAGE_LIST_SMALL)

			lc.InsertColumn(0, "Field")

			for c in s.getClassFactory().getClasses():
				for p in c.getProperties():
					lc.append(p)

			frame.ShowModal()

			for i in lc.iterSelectedObjects():
				print i
			
			return False

	TestApp().MainLoop()
