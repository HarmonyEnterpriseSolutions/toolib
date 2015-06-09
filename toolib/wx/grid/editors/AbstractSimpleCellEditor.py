"""
Abstract Editor for control
"""

import wx.grid
from toolib._	import *
from toolib		import debug
from toolib.wx	import wxutils
from wx.grid import PyGridCellEditor

INSERT_STARTS_EDITING = True

class AbstractSimpleCellEditor(PyGridCellEditor):
	"""
	startEdit    -> stopEdit
	          or -> cancelEdit
	"""

	def __init__(self):
		PyGridCellEditor.__init__(self)
		self.__editing = False
		self.__reset = False

	##########################################################################
	# Abstract methods
	#

	def createControl(self, parent, id):
		"""
		Creates control
		"""
		raise NotImplementedError, "abstract"

	def cleanControl(self):
		"""
		here to cleanup control value
		"""
		pass

	def startEdit(self, grid, row, col):
		"""
		Prepare control to edit
		"""
		raise NotImplementedError, "abstract. Returns start control value"
	
	def stopEdit(self, grid, row, col):
		"""
		raises ValueError
		Returns True if the value has been changed.
		"""
		raise NotImplementedError, "abstract"
	
	def cancelEdit(self, grid, row, col):
		"""
		override to do something when editing canceled
		"""
		pass

	##########################################################################
	# Implementation
	#
	def Create(self, parent, id, evtHandler):
		"""
		Called to create the control, which must derive from wxControl.
		"""
		assert debug.trace("Create")
		self.SetControl(self.createControl(parent, id))
		self.GetControl().PushEventHandler(evtHandler)

	def SetSize(self, rect):
		"""
		Called to position/size the edit control within the cell rectangle.
		If you don't fill the cell (the rect) then be sure to override
		PaintBackground and do something meaningful there.
		"""
		assert debug.trace("SetSize(%s)" % (rect,))
		self.GetControl().SetDimensions(rect.x, rect.y, rect.width+2, rect.height+2, wx.SIZE_ALLOW_MINUS_ONE)

	if INSERT_STARTS_EDITING:
		def IsAcceptedKey(self, event):
			"""
			Return True to allow the given key to start editing
			make INSERT to start editing
			"""
			return event.GetKeyCode() == wx.WXK_INSERT and not event.HasModifiers() or PyGridCellEditor.IsAcceptedKey(self, event)

	def Clone(self):
		"""
		Create a new object which is the copy of this one
		"""
		# TODO: initargs here (like pickle)
		return self.__class__()

	def BeginEdit(self, row, col, grid):
		"""
		Fetch the value from the table and prepare the edit control
		to begin editing.  Set the focus to the edit control.
		"""
		assert debug.trace("BeginEdit(%s, %s)" % (row, col))
		if not self.__editing:
			# this is workaround against PushEventHandler related crash
			# see PopupControl.beginEventHandlerRedirect __doc__
			if hasattr(self.GetControl(), 'beginEventHandlerRedirect'):
				self.GetControl().beginEventHandlerRedirect()
			self.__editing = True
			self.__reset   = False
			self.startEdit(grid, row, col)
		else:
			debug.warning("superfluous startEdit skipped")

	def EndEdit(self, row, col, grid):
		"""
		Complete the editing of the current cell. Returns True if the value
		has changed.  If necessary, the control may be destroyed.
		"""
		assert debug.trace("EndEdit(%s, %s)" % (row, col))
		if self.__editing:	# wx bug(?) fix (two finishes)
			self.__editing = False
			try:
				try:
					if self.__reset:
						self.cancelEdit(grid, row, col)
						return False
					else:
						return self.stopEdit(grid, row, col)
				finally:
					# this is workaround against PushEventHandler related crash
					# see PopupControl.beginEventHandlerRedirect __doc__
					if hasattr(self.GetControl(), 'endEventHandlerRedirect'):
						self.GetControl().endEventHandlerRedirect()
					self.cleanControl()
			except ValueError, e:
				wxutils.messageBox(self.GetControl(), e[0], _("Error"), wx.ICON_HAND)
		else:
			debug.warning("superfluous stopEdit skipped")

	def Reset(self):
		"""
		Reset the value in the control back to its starting value.
		*Must Override*
		"""
		assert debug.trace("Reset")
		self.__reset = True

	def Destroy(self):
		"""
		Does not goes, this is a wxPython bug!
		"""
		debug.warning("Destroy called! Bug is fixed!")
		self.GetControl().PopEventHandler(True)
