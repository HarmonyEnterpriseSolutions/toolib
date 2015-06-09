import wx
import wx.lib.ogl as ogl


class ActivityShape(ogl.RectangleShape):

	def __init__(self, canvas, activity):
		self.canvas = canvas
		self.__activity = activity

		ogl.RectangleShape.__init__(self, self.__getWidth(), canvas.activityHeight)

		#self._textMarginX = 0
		self._textMarginY = 0

		self._updateX()
		self._updateY()
		self._updateText()

		canvas._listeners.bind('propertyChanged', self._onCanvasPropertyChanged)

		self.SetCornerRadius(-0.2)
		self.SetDraggable(False)

		self.SetPen(self.canvas.shapePenNormal)
		self.SetBrush(self.canvas.shapeBrushNormal)

		#self.SetShadowMode(ogl.SHADOW_RIGHT)

	def select(self):
		self.__activity.setSelected(True)

	def __getWidth(self):
		return self.canvas.getDx() * self.__activity.getDuration()

	def _updateWidth(self):
		#rint '*** _updateWidth', self, self.canvas.getDx()
		self.SetWidth(self.__getWidth())

	def _updateX(self):
		#rint '*** _updateX', self, self.canvas.getDx()

		self.SetX(self.canvas.borderLeft + (self.__activity.getStart() + self.__activity.getDuration() / 2.0) * self.canvas.getDx())
		
		# update all links x positions
		for link in self.__activity.getLinksFrom() + self.__activity.getLinksTo():
			try:
				self.canvas._getShape(link)._updateX()
			except KeyError:
				pass
		
	def _updateY(self):
		self.SetY(self.canvas.borderTop + self.__activity.getRow() * (self.canvas.activityHeight + self.canvas.activityGap)  + self.canvas.activityHeight / 2.)

		# update all likns y positions
		for link in self.__activity.getLinksFrom() + self.__activity.getLinksTo():
			try:
				self.canvas._getShape(link)._updateY()
			except KeyError:
				pass

	def _updateText(self):
		text = self.getText()
		if text:
			self.ClearText()
			for line in text.split('\n'):
				self.AddText(line)

	def getText(self):
		return self.__activity.getName()

	def _onPropertyChanged(self, event):
		assert self.__activity is event.source
		if   event.propertyName == 'duration':	self._updateWidth()
		elif event.propertyName == 'start': 	self._updateX()
		elif event.propertyName == 'row':   	self._updateY()
		elif event.propertyName == 'name':  	self._updateText()
		elif event.propertyName == 'selected':
			#dc = wx.ClientDC(self.canvas)
			#self.canvas.PrepareDC(dc)
			self.SetPen(self.canvas.shapePenSelected if event.value else self.canvas.shapePenNormal)
			self.SetBrush(self.canvas.shapeBrushSelected if event.value else self.canvas.shapeBrushNormal)
			#self.Draw(dc)
			self.canvas.Refresh(False)
		else:
			assert 0, "Unhandled property change, %s" % event.propertyName

	def _onCanvasPropertyChanged(self, event):
		if event.propertyName == 'magnifier':
			self._updateWidth()
			self._updateX()

			# ogl bug workaround: in ogl when text initially not fits it centers incorrectly on resize
			self._updateText()
		else:
			assert 0, "Unhandled canvas property change, %s" % event.propertyName

	def getMaxPoint(self):
		return (
			self.GetX() + self.GetWidth()  / 2,
			self.GetY() + self.GetHeight() / 2,
		)

	def __str__(self):
		for o, s in self.canvas._shapes.iteritems():
			if s is self:
				return "<ActivityShape %s>" % o
		return "<ActivityShape>"



if __name__ == '__main__':
	from test import test
	test()
