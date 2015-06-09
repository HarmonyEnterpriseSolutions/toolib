import wx
import wx.lib.ogl as ogl
from toolib.wx.controls.ScrolledPanel import ScrolledPanel
from toolib.event.ListenerList import ListenerList

# shapes
from ActivityShape import ActivityShape
from LinkShape     import LinkShape
 
from GantDiagram   import GantDiagram





class GantView(ogl.ShapeCanvas):
	
	_dx = 10		# initial 1 activity unit pixel size

	_magnifierBase = 1.05	# magnification accuracy

	scaleHeight1 = 10
	scaleHeight2 = 20
	scaleHeight3 = 20

	activityHeight = 15
	activityGap    = activityHeight / 2

	borderTop      = scaleHeight3 + activityHeight
	borderLeft     = activityHeight
	borderBottom   = activityHeight
	borderRight    = activityHeight

	_dxMin = 3.
	
	
	def __init__(self, parent, model, **kwargs):

		self._dxMax = (wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X) - self.borderLeft - self.borderRight) / 20.	# to fit 20 minutes in fullscreen

		ogl.OGLInitialize()
		ogl._basic.NormalFont.SetPointSize(8)
		
		ogl.ShapeCanvas.__init__(self, parent, **kwargs)

		self.diagram = GantDiagram(model)
		self.SetDiagram(self.diagram)
		self.diagram.SetCanvas(self)

		self.shapePenNormal   = wx.Pen(wx.BLACK, 1)
		self.shapePenSelected = wx.Pen(wx.BLACK, 1)
		self.shapeBrushNormal   = wx.Brush('WHITE')
		self.shapeBrushSelected = wx.Brush('ORANGE')

		self._model = model
		self._model.listeners.bind('objectCreated',   self._onObjectCreated)
		self._model.listeners.bind('objectRemoved',   self._onObjectRemoved)
		self._model.listeners.bind('propertyChanged', self._onPropertyChanged)

		self.__magnifier = 0

		# shapes listen view to change scale
		self._listeners = ListenerList()

		self._shapes = {}

		# used for tips
		self.__lastMotionShape = None

		self.Bind(wx.EVT_MOTION,     self.__onMotion,     self)
		self.Bind(wx.EVT_MOUSEWHEEL, self.__onMouseWheel, self)
		self.Bind(wx.EVT_CHAR,       self.__onChar,       self)
		self.Bind(wx.EVT_MOUSE_EVENTS, self.__onMouseEvents, self)


	def getDx(self):
		return self._dx * self._magnifierBase ** self.__magnifier

	def _setMagnifier(self, magnifier):
		if self.__magnifier != magnifier:
			oldValue = self.__magnifier
			self.__magnifier = magnifier
			if self._dxMin < self.getDx() < self._dxMax:
				self._listeners.firePropertyChanged(self, 'magnifier', magnifier, oldValue)
				self.Refresh()
			else:
				self.__magnifier = oldValue

	@classmethod
	def createScrolledView(GantView, parent, model):
		scroll = ScrolledPanel(parent, style = wx.SUNKEN_BORDER)
		view = GantView(scroll, model, style=0)
		sizer = wx.BoxSizer(wx.VERTICAL)
		scroll.SetSizer(sizer)
		sizer.Add(view, 1, wx.GROW, 0)
		scroll.SetupScrolling()
		return scroll
	
	def _onObjectCreated(self, event):
		#rint ">>>", event
		object = event.source
		shape = self._shapes[object] = eval(object.__class__.__name__ + "Shape")(self, object)
		shape.SetCanvas(self)
		self.diagram.AddShape(shape)
		self._updateCanvasSize(shape)
		shape.Show(True)

		eh = EventHandler()
		eh.SetShape(shape)
		eh.SetPreviousHandler(shape.GetEventHandler())
		shape.SetEventHandler(eh)


	def _onObjectRemoved(self, event):
		#rint ">>>", event
		shape = self._shapes.pop(event.source)
		shape.Delete()

	def _onPropertyChanged(self, event):
		#rint "    >>>", event
		if event.source is self._model:
			if event.propertyName == 'scaleFactor':
				self.Refresh()
			else:
				assert 0, "Unhandled model property change: %s" % event.propertyName
		else:
			shape = self._shapes[event.source]
			shape._onPropertyChanged(event)
			self._updateCanvasSize(shape)

	def _getShape(self, object):
		return self._shapes[object]

	def _updateCanvasSize(self, shape):
		if hasattr(self.GetParent(), 'SetupScrolling'):
			width, height = shape.getMaxPoint()
			
			width  += self.borderRight
			height += self.borderBottom

			w, h = self.MinSize

			if w < width or h < height:
				self.MinSize = max(w, width), max(h, height)
				self.GetParent().SetupScrolling(scrollToTop=False)

	def __onMotion(self, event):
		if not event.Dragging():

			shape = self.FindShape(*event.GetPosition())[0]

			if shape != self.__lastMotionShape:

				text = shape.getText() if shape and hasattr(shape, 'getText') else ""
				
				tip = event.GetEventObject().ToolTip
				if text:
					if tip:
						tip.SetTip(text)
						tip.Enable(True)
					else:
						tip = event.GetEventObject().ToolTip = wx.ToolTip(text)
				elif tip:
						tip.SetTip("")
						tip.Enable(False)

				self.__lastMotionShape = shape

		event.Skip()

	def __onMouseWheel(self, event):
		if event.ControlDown() and not event.ShiftDown():
			self._setMagnifier(self.__magnifier + event.GetWheelRotation() / event.GetWheelDelta())
		else:
			event.Skip()
			self.GetParent().ProcessEvent(event)

	def __onMouseEvents(self, event):
		"""
		override focus on mouse event
		"""
		if event.ButtonDown():
			self.SetFocus()
		event.Skip()

	def __onChar(self, event):
		#rint "--------------------"
		dm = { ord('+') : 1, ord('-') : -1 }.get(event.GetKeyCode(), 0)
		if dm:
			self._setMagnifier(self.__magnifier + dm)
		else:
			event.Skip()


class EventHandler(ogl.ShapeEvtHandler):

	def OnLeftClick(self, *args):
		shape = self.GetShape()
		if hasattr(shape, 'select'):
			shape.select()


if __name__ == '__main__':
	from test import test
	test()
