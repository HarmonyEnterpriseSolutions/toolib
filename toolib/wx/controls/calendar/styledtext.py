# -*- coding: cp1251 -*-

import wx

"""
accepts basestring or (list or tuple) or dict of possible values:

	font-size
	font-family
	font-style
	font-weight
	font-underlined

	color
	background

basestring is command to draw text
dict is command to change state (font, colors)
list is command to push state, process all items, and then pop state

"""

FONT_FAMILY = {
	'default'    : wx.DEFAULT,
	'fixed'      : wx.FIXED, 
	'decorative' : wx.DECORATIVE, 
	'roman'      : wx.ROMAN,
	'script'     : wx.SCRIPT,
	'swiss'      : wx.SWISS,
	'modern'     : wx.MODERN,
}

FONT_STYLE = {
	'normal'     : wx.NORMAL, 
	'slant'      : wx.SLANT, 
	'italic'     : wx.ITALIC,
}

FONT_WEIGHT = {
	'normal'     : wx.NORMAL, 
	'light'      : wx.LIGHT, 
	'bold'       : wx.BOLD,
}

#ALIGN_LEFT              : 0000 0000 0000 0000
#ALIGN_TOP               : 0000 0000 0000 0000
#ALIGN_CENTER_HORIZONTAL : 0000 0001 0000 0000
#ALIGN_RIGHT             : 0000 0010 0000 0000
#ALIGN_BOTTOM            : 0000 0100 0000 0000
#ALIGN_CENTER_VERTICAL   : 0000 1000 0000 0000
#ALIGN_MASK              : 0000 1111 0000 0000


DEFAULT_FONT = {
	'font-size'       : 8,
	'font-family'     : wx.DEFAULT,
	'font-style'      : wx.NORMAL,
	'font-weight'     : wx.BOLD,
	'font-underlined' : False,
}




def makeColorTuple(color):
	if isinstance(color, str):
		color = wx.NamedColor(color)
	return tuple(color)


class StyledTextRenderer(object):


	def __init__(self):
		self.__state = [{}]
		self.__pending = {}
		self.__cursor = wx.Point(0, 0)
		self.__bounds = wx.Rect(0,0,0,0)
		

	def attach(self, dc):
		
		self.__dc = dc
		self.__cursor.Set(0,0)
		self.resetBounds()

		font = dc.GetFont()
		state = self.__state[-1]
		if font.IsOk():
			state['font-size'      ] = font.PointSize 
			state['font-family'    ] = font.Family    
			state['font-style'     ] = font.Style     
			state['font-weight'    ] = font.Weight    
			state['font-underlined'] = font.Underlined
		else:
			state.update(DEFAULT_FONT)

		state['textColor' ] = tuple(dc.TextForeground)
		state['bgColor'   ] = tuple(dc.TextBackground)

		self.__pending.clear()

	def detach(self):
		self.__dc = None
		self.__state[-1].clear()


	def pushState(self):
		self.__state.append(self.__state[-1].copy())

	def popState(self):
		state = self.__state.pop()
		self.applyState(self.__state[-1], state)


	def updateState(self, update):

		update = update.copy()

		# internalize values
		for k in ('textColor', 'bgColor'):
			if k in update:
				update[k] = makeColorTuple(update[k])

		for k, conv in (
			('font-family', FONT_FAMILY),
			('font-style',  FONT_STYLE),
			('font-weight', FONT_WEIGHT),
		):
			if k in update:
				update[k] = conv.get(update[k], update[k])
		# internalized

		state = self.__state[-1]
		oldState = state.copy()
		state.update(update)

		self.applyState(state, oldState)
			

	def applyState(self, state, oldState):
		for k, v in state.iteritems():
			if oldState.get(k, NotImplemented) != v:
				self.__pending[k.split('-')[0]] = True

	def moveTo(self, x, y):
		self.__cursor.Set(x, y)

	def resetBounds(self):
		self.__bounds.Set(0,0,0,0)

	def renderRect(self, data, rect, align=None):
		"""
		Render aligned rect
		"""	

		y = rect.y

		if align & (wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_BOTTOM):
			
			# must measure height
			self.resetBounds()

			self.render(data, mute=True)

			if align & wx.ALIGN_CENTER_VERTICAL:
				y = max(y, rect.y + (rect.height - self.__bounds.height) / 2)
			elif align & wx.ALIGN_BOTTOM:
				y = max(y, rect.y + (rect.height - self.__bounds.height))

		self.moveTo(rect.x, y)

		self.render(data, rect.x, rect.width, align)


			
	def render(self, data, xmin = None, width = None, align = 0, mute=False):
		if isinstance(data, basestring):
			self.renderText(data, xmin, width, align, mute)
		elif isinstance(data, dict):
			self.updateState(data)
		elif isinstance(data, (list, tuple)):
			self.pushState()
			try:
				for i in data:
					self.render(i, xmin, width, align, mute)
			finally:
				self.popState()
		else:
			raise TypeError, type(data)


	def renderText(self, text, xmin=None, width=None, halign=0, mute=False):
		"""
		renders text, horizontally aligned in (xmin, width) bounds
		"""

		if xmin is None:
			xmin = self.__cursor.x
		
		assert width is not None or halign & (wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_RIGHT) == 0, "You must provide width to render horizontal aligned text"

		lines = text.split('\n')
		n = len(lines) - 1
		for i, line in enumerate(lines):
			newline = i<n
			if line or newline:
				self._renderLine(line, newline, xmin, width, halign, mute)

	
	def _renderLine(self, text, newline, xmin, width, halign, mute):
		
		# update font
		if self.__pending.pop('font', False):
			state = self.__state[-1]
			self.__dc.SetFont(wx.Font(
				state['font-size'],
				state['font-family'],
				state['font-style'],
				state['font-weight'],
				state['font-underlined'],
			))

		w, h = self.__dc.GetTextExtent(text or "M")
		if not text:
			w = 0

		if not mute:
			if self.__pending.pop('textColor', False):
				self.__dc.SetTextForeground(self.__state[-1]['textColor'])

			if self.__pending.pop('bgColor', False):
				self.__dc.SetTextBackground(self.__state[-1]['bgColor'])

			if halign & wx.ALIGN_CENTER_HORIZONTAL:
				self.__cursor.x = max(xmin, xmin + (width - w) / 2)
			elif halign & wx.ALIGN_RIGHT:
				self.__cursor.x = max(xmin, xmin + (width - w))

			self.__dc.DrawText(text, *self.__cursor)

		self.__bounds.Union((self.__cursor.x, self.__cursor.y, w, h))

		if newline:
			self.__cursor.x = xmin
			self.__cursor.y += h
		else:
			self.__cursor.x += w


	def getBounds(self):
		return self.__bounds


class StyledTextString(object):

	def __init__(self, data):
		self.__data = []
		self.render(data)

	def render(self, data):
		if isinstance(data, basestring):
			self.__data.append(data)
		elif isinstance(data, dict):
			pass
		elif isinstance(data, (list, tuple)):
			for i in data:
				self.render(i)
		else:
			raise TypeError, type(data)

	def __str__(self):
		return ''.join(self.__data)


class StaticStyledText(wx.Panel):

	def __init__(self, parent, text='', align=0):
		super(StaticStyledText, self).__init__(parent, -1, style=wx.FULL_REPAINT_ON_RESIZE)
		
		self.__align = align
		self.__text  = text
		self.__renderer = StyledTextRenderer()

		self.Bind(wx.EVT_PAINT,        self.__onPaint)
		self.Bind(wx.EVT_SIZE,         self.__onSize)

	def setText(self, text):
		if self.__text != text:
			self.__text = text
			self.Refresh()

	def getText(self):
		return self.__text

	def setAlign(self, align):
		if self.__align != align:
			self.__align = align
			self.Refresh()

	def getAlign(self):
		return self.__align

	def __onPaint(self, event):
		dc = wx.PaintDC(self)
		self.__renderer.attach(dc)
		self.__renderer.renderRect(self.__text, self.GetClientRect(), self.__align)
		self.__renderer.detach()

	def __onSize(self, evt):
		self.Refresh(False)
		evt.Skip()


def test():

	def oninit(self):
		self.Size = 800, 600
		#l = StaticStyledText(self, "hello world")
		#l = StaticStyledText(self, [{'font-size' : 15, 'textColor' : 'RED', 'font-weight' : 'normal'}, "Каждый ", [{'font-size' : 20, 'textColor' : 'ORANGE'}, "good "], "world\nand\nnow\nmultiline"])
		l = StaticStyledText(self, [
			{'textColor' : 'RED', 'font-size' : 40, 'font-weight' : 'normal'},	"Каждый\n",
			{'textColor' : 'ORANGE'},		"охотник\n",
			{'textColor' : 'YELLOW'},		"желает\n",
			{'textColor' : 'GREEN'}, 		"знать\n",
			{'textColor' : 'SKY BLUE'},	"где\n",
			{'textColor' : 'BLUE'},      	"сидят\n",
			{'textColor' : 'VIOLET'},    	"фазаны",
		], wx.ALIGN_CENTER)
			
	def ondestroy(self):
		pass

	def ontimer(self):
		pass

	from toolib.wx.TestApp import TestApp
	TestApp(oninit, ondestroy, ontimer = ontimer).MainLoop()

if __name__ == '__main__':
	test()
