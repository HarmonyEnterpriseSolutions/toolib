import wx
from wx.lib.scrolledpanel import ScrolledPanel as Base

class ScrolledPanel(Base):

	"""
	Scrolls vertical scrollbar
	if EVT_MOUSEWHEEL not passed to ScrolledPanel i call ProcessEvent directly from child window event handler
	"""

	def __init__(self, *args, **kwargs):
		super(Base, self).__init__(*args, **kwargs)
		self.Bind(wx.EVT_MOUSEWHEEL, self.__onMouseWheel)

	def __onMouseWheel(self, event):
		if not event.ControlDown() and not event.ShiftDown():
			self.Scroll(-1, max(0, self.GetViewStart()[1] - event.GetWheelRotation() / event.GetWheelDelta()))
		else:
			event.Skip()
