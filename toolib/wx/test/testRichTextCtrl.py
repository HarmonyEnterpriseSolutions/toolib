import wx
from toolib.wx.TestApp import TestApp
import wx.richtext as rt
from cStringIO import StringIO
import re
from toolib.text.html.BeautifulSoup import BeautifulSoup, NavigableString, Tag


REC_XML = re.compile('''(?s)\<\!\-\-\<xml\>(.*)\<\/xml\>\-\-\>''')



class RichText(wx.Panel):

	def __init__(self, parent):
		super(RichText, self).__init__(parent)

		self.toolbar = wx.ToolBar(self)
		self.richtext = rt.RichTextCtrl(self, style=wx.VSCROLL|wx.HSCROLL|wx.BORDER_SUNKEN|wx.WANTS_CHARS)

		def doBind(item, handler, updateUI=None):
			self.Bind(wx.EVT_MENU, handler, item)
			if updateUI is not None:
				self.Bind(wx.EVT_UPDATE_UI, updateUI, item)

		doBind(self.toolbar.AddTool(wx.ID_CUT,    images.cut  .GetBitmap(), shortHelpString="Cut"   ), self.richtext.ProcessEvent, self.richtext.ProcessEvent)
		doBind(self.toolbar.AddTool(wx.ID_COPY,   images.copy .GetBitmap(), shortHelpString="Copy"  ), self.richtext.ProcessEvent, self.richtext.ProcessEvent)
		doBind(self.toolbar.AddTool(wx.ID_PASTE,  images.paste.GetBitmap(), shortHelpString="Paste" ), self.richtext.ProcessEvent, self.richtext.ProcessEvent)
		
		self.toolbar.AddSeparator()
		
		doBind(self.toolbar.AddTool(wx.ID_UNDO,   images.undo.GetBitmap(), shortHelpString="Undo"), self.richtext.ProcessEvent, self.richtext.ProcessEvent)
		doBind(self.toolbar.AddTool(wx.ID_REDO,   images.redo.GetBitmap(), shortHelpString="Redo"), self.richtext.ProcessEvent, self.richtext.ProcessEvent)
		
		self.toolbar.AddSeparator()
		
		id_bold, id_italic, id_underlined = [wx.NewId() for i in range(3)]
		
		doBind(self.toolbar.AddCheckTool(id_bold,       images.bold     .GetBitmap(), shortHelp="Bold"     ), self._onBold,      self._onUpdateBold)
		doBind(self.toolbar.AddCheckTool(id_italic,     images.italic   .GetBitmap(), shortHelp="Italic"   ), self._onItalic,    self._onUpdateItalic)
		doBind(self.toolbar.AddCheckTool(id_underlined, images.underline.GetBitmap(), shortHelp="Underline"), self._onUnderline, self._onUpdateUnderline)

		self.toolbar.AddSeparator()

		doBind(self.toolbar.AddTool(-1, images.colour.GetBitmap(), shortHelpString="Font Colour"), self._onColour)

		self.toolbar.Realize()

		self.richtext.AcceleratorTable = wx.AcceleratorTable([
			wx.AcceleratorEntry(wx.ACCEL_SHIFT, wx.WXK_DELETE, wx.ID_CUT),
			wx.AcceleratorEntry(wx.ACCEL_CTRL , wx.WXK_INSERT, wx.ID_COPY),
			wx.AcceleratorEntry(wx.ACCEL_SHIFT, wx.WXK_INSERT, wx.ID_PASTE),
			wx.AcceleratorEntry(wx.ACCEL_CTRL,  ord('A'),      wx.ID_SELECTALL),

			wx.AcceleratorEntry(wx.ACCEL_CTRL,  ord('Z'), wx.ID_UNDO),
			wx.AcceleratorEntry(wx.ACCEL_CTRL,  ord('Y'), wx.ID_REDO),

			wx.AcceleratorEntry(wx.ACCEL_CTRL,  ord('B'), id_bold),
			wx.AcceleratorEntry(wx.ACCEL_CTRL,  ord('I'), id_italic),
			wx.AcceleratorEntry(wx.ACCEL_CTRL,  ord('U'), id_underlined),
		])

		box = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(box)

		box.Add(self.toolbar, 0, wx.EXPAND)
		box.Add(self.richtext, 1, wx.EXPAND)

	
	def _onBold(self, evt):
		self.richtext.ApplyBoldToSelection()
        
	def _onItalic(self, evt): 
		self.richtext.ApplyItalicToSelection()
        
	def _onUnderline(self, evt):
		self.richtext.ApplyUnderlineToSelection()
        
	def _onUpdateBold(self, evt):
		evt.Check(self.richtext.IsSelectionBold())
    
	def _onUpdateItalic(self, evt): 
		evt.Check(self.richtext.IsSelectionItalics())
    
	def _onUpdateUnderline(self, evt): 
		evt.Check(self.richtext.IsSelectionUnderlined())
    
	def _onColour(self, evt):
		colourData = wx.ColourData()
		attr = rt.TextAttrEx()
		attr.SetFlags(rt.TEXT_ATTR_TEXT_COLOUR)
		if self.richtext.GetStyle(self.richtext.GetInsertionPoint(), attr):
			colourData.SetColour(attr.GetTextColour())

		dlg = wx.ColourDialog(self, colourData)
		if dlg.ShowModal() == wx.ID_OK:
			colourData = dlg.GetColourData()
			colour = colourData.GetColour()
			if colour:
				if not self.richtext.HasSelection():
					self.richtext.BeginTextColour(colour)
				else:
					r = self.richtext.GetSelectionRange()
					attr.SetFlags(rt.TEXT_ATTR_TEXT_COLOUR)
					attr.SetTextColour(colour)
					self.richtext.SetStyle(r, attr)
		dlg.Destroy()

	def get_html(self):

		handler = rt.RichTextHTMLHandler()
		handler.SetFlags(rt.RICHTEXT_HANDLER_SAVE_IMAGES_TO_MEMORY)
		handler.SetFontSizeMapping([7,9,11,12,14,22,100])

		try:
			stream = StringIO()
			if handler.SaveStream(self.richtext.GetBuffer(), stream):

				return "<!--<xml>%s</xml>-->\n%s" % (self.get_xml() or '', stream.getvalue())
		finally:
			handler.DeleteTemporaryImages()

	def set_html(self, html):
		m = REC_XML.match(html)
		if m:
			xml = m.groups()[0]
		else:
			xml = Document.from_html(html).__xml__()

		self.set_xml(xml)

	def get_xml(self):

		handler = rt.RichTextXMLHandler()

		stream = StringIO()
		if handler.SaveStream(self.richtext.GetBuffer(), stream):

			return stream.getvalue()

	def set_xml(self, xml):
		rt.RichTextXMLHandler().LoadStream(self.richtext.GetBuffer(), StringIO(xml))
		self.richtext.Refresh()


def strip_html(html):
	return html.split('</xml>-->')[-1].strip()


class Document(list):

	XML = '''\
<?xml version="1.0" encoding="UTF-8"?>
<richtext version="1.0.0.0" xmlns="http://www.wxwidgets.org">
<paragraphlayout>
%s
</paragraphlayout>
</richtext>'''

	@classmethod
	def from_html(klass, html):

		self = klass()

		soup = BeautifulSoup(html)
		for i in soup.recursiveChildGenerator():
			if isinstance(i, NavigableString):
				self.add_text(Text(i))
			elif isinstance(i, Tag) and i.name == 'br':
				self.end_paragraph()

		return self

	def __init__(self):
		self.paragraph_ended = True
	
	def add_text(self, text):
		if self.paragraph_ended:
			self.append(Paragraph())
			self.paragraph_ended = False

		try:
			self[-1][-1].last = False
		except IndexError:
			pass
		
		self[-1].append(text)

	def end_paragraph(self):
		if self.paragraph_ended:
			self.append(Paragraph())
		else:
			self.paragraph_ended = True
	
	def __xml__(self):
		return self.XML % '\n'.join([p.__xml__() for p in self])


class Paragraph(list):

	def __xml__(self):
		return '    <paragraph>\n%s\n    </paragraph>' % '\n'.join([text.__xml__() for text in self])


class Text(object):

	ATTR_BY_TAG = {
		'u' : 'fontunderlined="1"',
		'b' : 'fontweight="92"',
		'i' : 'fontstyle="93"',
	}
	
	def __init__(self, text_element):
		self.text = unicode(text_element).strip()
		self.attributes = set()
		self.last = True
		parent = text_element.parent
		while parent:
			if isinstance(parent, Tag) and parent.name in self.ATTR_BY_TAG:
				self.attributes.add(self.ATTR_BY_TAG[parent.name])
			parent = parent.parent
	
	def __xml__(self):
		attrs = ' '.join(self.attributes)
		return ("      <text%s>%s</text>" % (' ' + attrs if attrs else '', self.text if self.last else self.text + ' ')).encode('UTF-8')





def main():
	
	def oninit(self):

		self.rt = RichText(self)
		self.xml     = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.SUNKEN_BORDER)
		self.html    = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.SUNKEN_BORDER)

		box = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(box)

		box.Add(self.rt, 1, wx.EXPAND)
		box.Add(self.xml,     1, wx.EXPAND)
		box.Add(self.html,    1, wx.EXPAND)

		def on_richtext_changed(event):
			self.html.SetValue(self.rt.get_html() or '')
			self.xml.SetValue(self.rt.get_xml() or '')
		
		self.rt.Bind(wx.EVT_TEXT, on_richtext_changed)

		#self.xml.Bind(wx.EVT_TEXT, lambda event: self.rt.set_xml(self.xml.GetValue()))

		#self.rt.set_html(open("test_wwm_html.html", 'rt').read().decode('cp1251'))




	def ondestroy(self):
		pass

	TestApp(oninit, ondestroy).MainLoop()


from wx.lib.embeddedimage import PyEmbeddedImage
class images:

	cut = PyEmbeddedImage(
		"iVBORw0KGgoAAAANSUhEUgAAABAAAAAPCAYAAADtc08vAAAABHNCSVQICAgIfAhkiAAAAbBJ"
		"REFUKJGdk0FLG1EQx3/vpRdv7sG49CKYxvSmVDwkpd78ALbSShQkbU81guAH8BN4EE0KGlCQ"
		"5iAIoiaIwWAP3bi0WXZLW1q2WfGmJ8mhV19Pu+xqWsSBx/Bm/vObmQcPIWP4Jz83r96vb6pw"
		"LJxzXfdWThKyuJR8/2rjOI4Kxz8ZDQUwkHosuGERwOLKsohLydpaKSIqfyjfrOsM8C2VSlKr"
		"1RRAtVJRAK8mJ+8GWFxZFldui93dPTzvTFWqhwCMPnt6a3yAB52CWjLBSCLBwcH+P0f/7wpX"
		"bouLywvys+/uB9CSCfRendVCkezMm/tN8PnwiKHBQX59axKXHWUACCFjAHyp15VX2gIgbdg0"
		"MkO8LG+I7WxO+XeARwt5ngwPBw8q/eLe1wtI75y25QTCsG9bDtI7p+fFW6xmU0UAXmkLU9eY"
		"OK0LNf0cIOji+4ezOSZO68LUNX4vrUbfIG3YXPf3AdD9o4Wpa5E9TV3jT8MC4Lq/j7RhRwGm"
		"rtG2HPx9u6bGI4CuqXHShs12NqfalhNtIGSMn8cnaiczpnYyY6paKHb8jdVCMdA0Tz4Gmr9P"
		"zKg0oZ3GfwAAAABJRU5ErkJggg==")

	copy = PyEmbeddedImage(
		"iVBORw0KGgoAAAANSUhEUgAAABAAAAAPCAYAAADtc08vAAAABHNCSVQICAgIfAhkiAAAATlJ"
		"REFUKJGFk71OwzAURo/tpE2AdihiAAmQWNiKWICpDIhnQEi8A0+ASsXAzDsgIcTEA3QANsZu"
		"XTMQBiqkUkFF04aB2sRJSO90bV+f+33+EUIqzq7bMam471UA6JzuiPRaMqROltc2KS9tMFhY"
		"JVArAJw31qlfPWfguYCqp6j5Lou+S81XpmAWRGgLe1t13r8i+sMxYdAtasrFyYGx5eik4v11"
		"DYHW8T6dl0/6w4i3wYjXjxFh0KV51ADasYYYQNUzKXlQDQYsiNnluzLJA6CsBKQgrdtHa2x2"
		"zJdkeoq5koLvsYEc7m5bdqxqRwk8V5C4GFwlDCRKKdR2Egq01IkpUhJgCsmKtkdKJiHTOSFA"
		"xoWQ7NFbgF8F+ZAU4PLuKbMopYBJXAhxwH5ZgPW5ZkH+tdC8eShyZ+IHUNNZHhrzal0AAAAA"
		"SUVORK5CYII=")

	paste = PyEmbeddedImage(
		"iVBORw0KGgoAAAANSUhEUgAAABAAAAAPCAYAAADtc08vAAAABHNCSVQICAgIfAhkiAAAAXNJ"
		"REFUKJGFkzsvREEYhp/vzDnWWHuxdnsJjd+wRKPYgkIUKqHVKtYlQoi4FX6BiGQTolEpFBIU"
		"/gUJtbXWdSMuo1jGHueceJvJN5nvmff9JiPiKH6UL5YMITrfGJWwfQARR5EvlsxY8pqr6gvL"
		"60u+A3NT8wCcOd2hICdfLJmT/k+AQPPPXke6hcP241CHbmOxtboW5TRS0jO9a06HM5j7MgAf"
		"lRsAzE2N15cLBm77A02NURxLSmUBUJlcvc5pYi1dAGxODDI7WgDgaHHEF8UBkERbJAQgrV2y"
		"rZ510AixM5BEG+bxDkllMfdlVCZn46T071MXFvZ9cVwAiScxzw+hEIAm5ZDSsD05RLX2Tvnp"
		"jZXS0S8AnUAgFALQ7AlQh/yVHSI6gcSTNo5vJiI0e/LtRJHWrh8gno6EAHhKLCTepHwzqaNi"
		"McRVmNpTIA5U6J3ZC3r3AZz6IroV3j8wYCFn4532cN/OZeA/uAC98weRN/ynL78NdulpYuMM"
		"AAAAAElFTkSuQmCC")

	
	undo = PyEmbeddedImage(
		"iVBORw0KGgoAAAANSUhEUgAAABAAAAAPCAYAAADtc08vAAAABHNCSVQICAgIfAhkiAAAAhVJ"
		"REFUKJGNkstrE1EYxX8zmcSZZDJp2rSNfSg22CANYhYijWjAjcviwkVxW2hBVyZ/gZu6aOtK"
		"aLC7dicqwcdGiIrUoCIhpUVDsPZhq4GENqE2aUu5LuqkLxv94Fvce885995zPkmSLRxVffce"
		"ikQ6W123N7i41XOR65fPSeaeFH3wTAz390h7ib2D4+J9ZhGXajskWqxscq27C5MjP0nOEInF"
		"hQkIDgyJpeUCvjoVjyrjtCoAOK0KHlXGV6eSSGUZefxaACgu1cbH6W/0Do6LL/M5WjQNpyqz"
		"tb3NbKnClaCPwMlmpudzJFJZ/G4Hhm2b+OQMAApAp8fOykoRv9uBrlpYq+yQU6NRKbXn+ZFY"
		"XCzNLeN22Jj9UdoV0FU7umoHYK2yTmblF6nR6D5fAFobXRR/5tBVO07r+o6A06pgGM59QMOx"
		"9ddU4pMzhDu8ICtAHgAZwDhmrXZbYz3hDi/BgSFxUMBjkzA0jbXNMucDp3YEJJsVQ9cwdI1S"
		"uczCaoFsLl+N0ySHI/fF1eAZDF3j00KhGqOyWCgy8TZNa0sDXSeauNTuqw6KaWD37Zi4caGT"
		"ekPnXeYrp9uaePPnTKo1iSb5ZjjA8WY333N5JpKfeXm3f9dgSbYc2aHomHj6Ki2mMnPiUWJK"
		"hKJj4iBGrnV7yO/lrL+dfHGD4RcfSI70H4q25hdME0vlDZ7f6TtE/i8P/lW/AfYJsF99ZciZ"
		"AAAAAElFTkSuQmCC")

	redo = PyEmbeddedImage(
		"iVBORw0KGgoAAAANSUhEUgAAABAAAAAPCAYAAADtc08vAAAABHNCSVQICAgIfAhkiAAAAg5J"
		"REFUKJGdkr9rU1EcxT/3vbz2vfS924qRpmopVmIsFCWDiFkCAXHs5CDoJqSrJIP+BS5tXCw0"
		"EHDo4FBUguDgULVQImJJLe0Qu2hqWyKNMT9q0p/XofRHmtrBA9/l3HPPPffcK4Sms4fxyRn1"
		"NDXFYqG0z4Wv+kg+uC34B8SeQTSRUq/S87SbLU2iUn2D6/5unj+612AUTaSUEJpO/OV7Nfb2"
		"Mx5TA2B9W6OyuYVjuGjVdxq4zGhMHD5QCE0nFB1RHl1h6DrZ4hrhgI/+nk7mvueZyCzQK00M"
		"XadS32G5VuNyTydLywUqm1u4AMprNXxdkmp9m3DAx3BkoPHOg0PKf6qNrg4Dx9TYKJa45HEz"
		"vVJGA3AMF7bpxjZ1zp1pb+ogMxoT2eIaAN4Oh+7THdimG2A3AYCUDtK2SE3NH9u2bLOwTTdS"
		"OvucY6zuGlzrv0C1XuOsI/G0NL9YYHBIhXq9SMtqWtMAhiMDYjpXQNoWtwJ9hKIjak9w5/GY"
		"AljIr5L7XaBcqyFtC2lbiBbj4B/cfzKupLZN0H+RX+Uqzz5+JR2PNMQZn5xR2cU887mfLC0X"
		"+FH5c2AAcPNhQt290cf5Tg8r+SIjH+aaTJogNL1hgrGkejExq2az39Trd19UMJZURzWHRztq"
		"mI5HxPCbT6yW1rni7ybo954YwHUcmY5HRNxOKmm1nrgZaOzgf/AXUUy2DjrCDG0AAAAASUVO"
		"RK5CYII=")


	bold = PyEmbeddedImage(
		"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAEtJ"
		"REFUOI3NUkEKACAMyq3//7jWNQwWY0HzKNOJCIi2DCSlfmHQmbA5zBNAFG4CPoAodo4fFOyA"
		"wZGvHTDqdwCecnQHh0EU/ztIGyy1dBRJuH/9MwAAAABJRU5ErkJggg==")

	italic = PyEmbeddedImage(
		"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAGdJ"
		"REFUOI3Vk1EOgDAIQwt4/2P0lopfS6YOgsEfl+xntK8kMBE1dI623F8Atqzox+73N1GTcgez"
		"mOTDPEThJekAHIBHmhQwzCTfAyrpKaCSHgKq6SGgmi5qkHmVV3Nfzf5S+/9faANOrocplI0e"
		"xSoAAAAASUVORK5CYII=")

	underline = PyEmbeddedImage(
		"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAFdJ"
		"REFUOI1jZGRiZqAEMFGkmxoGsKAL/P/39z8yn5GJmRGbGE4XIEvC2NjEcBpAKhg1gIABS5cs"
		"/o9MYwOMuJIyetwzMGBGIV4DiAUEUyI2gJKwBjw3AgDOdhYrghF5ggAAAABJRU5ErkJggg==")


	colour = PyEmbeddedImage(
		"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAPZJ"
		"REFUOI1jZGRiZqAEsOCS+Mcu9h+bONPPV4wofEKa37Lz4zWYEd0LuGzG5RKsLiAFDEIDllTz"
		"MWxtyGJ4yiWKofgfCyTSkGMCJRDd/hr/Z2BgYGCZ5cAg8v0jg++C9wy6zx8ysP37zfCYXYFh"
		"g1gww+VfUSiGwg2AaRZ/JcPw6v0fhv/qLxg4vv1jCOv5zPBvZgrDSukghp8/ZRkY/rFiGgDT"
		"jBV84mX4572WgekzL8O/v5hBxoRXMwMDw/+3QgwM/3CHNeFY+MvMwMDyE6vtRBnAKPqWgUH2"
		"OQUu4P/IwGh8HrcFBAORgYFhF/NZRhetP1jVAACsCFJPHjA77wAAAABJRU5ErkJggg==")



if __name__ == '__main__':
	main()
