import wx
import re

from TCursor    import TCursor
from TSelection import TSelection
from itertools  import chain
from toolib.wx.mixin.TWindowUtils import messageBox

try: _
except NameError: _ = lambda s: s

class FindReplaceDialog(wx.FindReplaceDialog):

	def Show(self, show):
		wx.FindReplaceDialog.Show(self, show)
		if show:
			self.setButtonText("Match &whole word only", _("Whole &cell"))
			self.setButtonText("Match &case", _("Search &selection"))
		
	def setButtonText(self, oldText, text):
		# todo: unix compattible
		import ctypes

		class POINT(ctypes.Structure):
			_fields_ = [("x", ctypes.c_int), ("y", ctypes.c_int)]

		class RECT(ctypes.Structure):
			_fields_ = [("topleft", POINT), ("bottomright", POINT)]

		hwnd = ctypes.windll.user32.FindWindowExA(self.GetHandle(), 0, 'Button', oldText)
		if hwnd:
			r = RECT()
			ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(r))
			h = r.bottomright.y - r.topleft.y
			ctypes.windll.user32.ScreenToClient(self.GetHandle(), ctypes.byref(r.topleft))
			ctypes.windll.user32.MoveWindow(hwnd, r.topleft.x, r.topleft.y, 150, h, True)
			ctypes.windll.user32.SetWindowTextW(hwnd, text)


class DownCellIterator(object):

	def __init__(self, grid, pos=None, skipFirst=False):
		self.grid = grid
		self.row, self.col = pos or self._firstCell()
		if not skipFirst:
			self._noskip()

	def __iter__(self):
		return self

	def _noskip(self):
		self.col -= 1

	def _firstCell(self):
		return (0,0)

	def next(self):
		self.col += 1
		if self.col >= self.grid.GetNumberCols():
			self.col = 0
			self.row += 1
		if self.row >= self.grid.GetNumberRows():
			raise StopIteration
		return self.row, self.col


class UpCellIterator(DownCellIterator):

	def _noskip(self):
		self.col += 1

	def _firstCell(self):
		return (self.grid.GetNumberRows()-1,self.grid.GetNumberCols()-1)

	def next(self):
		self.col -= 1
		if self.col < 0:
			self.col = self.grid.GetNumberCols()-1
			self.row -= 1
		if self.row < 0:
			raise StopIteration
		return self.row, self.col


class MFindReplace(TCursor, TSelection):
	"""
	Requires:
		getValueAsText
		setValueAsText

	Provides:
		getRowSelection		--> returns LineSelection
		getColSelection		--> returns LineSelection
		getCellSelection	--> returns CellSelection

	case insensitive not works when unicode matching
	"""
	
	SEARCH_SELECTION = wx.FR_MATCHCASE

	
	def __init__(self, getValueAsText, setValueAsText=None):

		self.__getValueAsText = getValueAsText
		self.__setValueAsText = setValueAsText

		self.Bind(wx.EVT_FIND,             self.__onFind)
		self.Bind(wx.EVT_FIND_NEXT,        self.__onFindNext)
		#self.Bind(wx.EVT_FIND_REPLACE,     self.__onReplace)
		#self.Bind(wx.EVT_FIND_REPLACE_ALL, self.__onReplaceAll)
		self.Bind(wx.EVT_FIND_CLOSE, self.__onDialogClose)

		self.__data = None
		self.__dialog = None
		self.__recoverTimer = None


	def __find(self, pos, skipFirst, event):

		down      = event.GetFlags() & wx.FR_DOWN
		wholeCell = event.GetFlags() & wx.FR_WHOLEWORD
		searchAll = not (event.GetFlags() & self.SEARCH_SELECTION)

		positions = self.__cellIterator(pos, skipFirst, down)

		if not searchAll:
			sel = self.getCellSelection().getCellSet()
		else:
			sel = None

		text = str(event.GetFindString())

		if wholeCell:
			match = re.compile(re.escape(text) + '$', re.LOCALE | re.IGNORECASE).match
		else:
			match = re.compile(
				'.*'.join(
					map(
						re.escape,
						filter(None, text.split(' '))
					)
				),
				re.LOCALE | re.IGNORECASE,
			).search

		wx.BeginBusyCursor()

		if searchAll:
			for p in positions:
				if match(str(self.__getValueAsText(*p))):
					wx.EndBusyCursor()
					self.GetGridWindow().SetFocus()
					self.setGridCursor(*p)
					return
		else:
			for p in positions:
				if p in sel and match(str(self.__getValueAsText(*p))):
					wx.EndBusyCursor()
					self.GetGridWindow().SetFocus()
					self.setGridCursor(*p)
					return

		wx.EndBusyCursor()
		messageBox(event.GetDialog(), _('Could not find the string:\n"%s"') % event.GetFindString(), _("Search"))

	def __onFind(self, event):
		self.__find(None, False, event)
				
	def __onFindNext(self, event):
		self.__find(self.getGridCursor(), True, event)

	def __onDialogClose(self, event):
		event.GetDialog().Destroy()
		self.__dialog = None

	def __cellIterator(self, pos, skipFirst, down):
		if down:
			return DownCellIterator(self, pos, skipFirst)
		else:
			return UpCellIterator(self, pos, skipFirst)

	#def __onReplace(self, event):
	#	pass
	
	#def __onReplaceAll(self, event):
	#	pass

	def find(self):
		if self.__dialog is None:
			
			if self.__data is None:
				self.__data = wx.FindReplaceData()
			
			flags = wx.FR_DOWN
			
			if len(self.getCellSelection()) > 1:
				flags |= self.SEARCH_SELECTION

			self.__data.SetFlags(flags)

			self.__dialog = FindReplaceDialog(self, self.__data, _("Search"))
			try:
				self.__dialog.Show(True)
			except wx.PyAssertionError, e:
				# workaround wx bug: can't have more than one find dialog currently. 
				# reprodused if previous find dialog destoy process not finished before new dialog created. only on slow remote console
				if "can't have more than one find dialog currently" in str(e):
					print "* workaround PyAssertionError: %s" % (e,)

					# dialog is buggy now, destroying
					self.__dialog.Destroy()
					self.__dialog = None

					# do find some time later, when application repaint complete
					if self.__recoverTimer is None:	
						self.__recoverTimer = wx.Timer(self, -1)
						self.Bind(wx.EVT_TIMER, lambda event: self.find())
					self.__recoverTimer.Start(500, True)
				else:
					raise

					
if __name__ == '__main__':
	from test.testFindReplace import test
	test()
