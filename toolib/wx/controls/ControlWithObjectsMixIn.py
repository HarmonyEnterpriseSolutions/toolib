#################################################################
# Package: toolib.wx.controls
"""
Mixin to make object control from any control 
implementing ControlWithItems interface

Methods mapping:
	Clear			clear
	Append			append
	Insert			insert				Note: arguments order reversed
	Delete			__delitem__
	GetCount		__len__
	GetString		__getitem__
	GetSelection	getSelectedObject
	SetSelection	setSelectedObject

Method added:
	getIndex		returns object index
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2006/08/03 18:40:40 $"
__version__ = "$Revision: 1.4 $"
# $Source: D:/HOME/cvs/toolib/wx/controls/ControlWithObjectsMixIn.py,v $
#
#################################################################

class ControlWithObjectsMixIn(object):

	def __init__(self, objects=None, strfunc=None):
		self.__strfunc = strfunc or str
		self.__objects = list(objects or ())

	def clear(self):
		"""
		wxControlWithItems::Clear
		"""
		del self.__objects[:]
		self.Clear()

	def append(self, object):
		"""
		wxControlWithItems::Append
		"""
		self.__objects.append(object)
		sell.Append(self.__strfunc(object))

	def insert(self, index, object):
		"""
		wxControlWithItems::Insert
		"""
		self.__objects.insert(index, object)
		self.Insert(self.__strfunc(object), index)

	def __delitem__(self, i):
		"""
		wxControlWithItems::Delete
		"""
		del self.__objects[i]
		self.Delete(i)

	def __len__(self):
		"""
		wxControlWithItems::GetCount
		"""
		return len(self.__objects)
	
	def getSelectedObject(self):
		return self.__objects[self.GetSelection()]

	def setSelectedObject(self, object):
		self.SetSelection(self.getIndex(object))

	def __getitem__(self, i):
		"""
		wxControlWithItems::GetString
		"""
		return self.__objects[i]

	def __iter__(self):
		return iter(self.__objects)

	def getIndex(self, object):
		return self.__objects.index(object)

	def _mapObjects(self, objects):
		return map(self.__strfunc, objects or ())

	def _mapObject(self, object):
		return self.__strfunc(object)

	def _setObjects(self, objects):
		del self.__objects[:]
		self.__objects.extend(objects)
