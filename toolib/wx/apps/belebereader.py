# -*- coding: Cp1251 -*-
from toolib.util.strings import rsplit

def main():
	import wx

	class MainFrame(wx.Frame):
		def __init__(self, parent=None):
			wx.Frame.__init__(self, parent, -1, 'belebereader', style=wx.DEFAULT_FRAME_STYLE)# | wx.MAXIMIZE
			split = wx.SplitterWindow(self, -1)
			style = wx.TE_MULTILINE 
			self._source = wx.TextCtrl(split, -1, style=style)
			self._target = wx.TextCtrl(split, -1, style=style | wx.TE_READONLY)
			split.SplitHorizontally(self._target, self._source)

			self._source.Bind(wx.EVT_TEXT, self.OnTextChanged)

		def processLine(self, line):
			try:
				if line:
					return eval('"%s"'  % line.strip())
				else:
					return ""
			except:
				return '! Помилка: ' + line
			
		def OnTextChanged(self, event):
			text = '\n'.join(map(self.processLine, event.GetString().split('\n')))
			self._target.SetValue(text)

	class App(wx.PySimpleApp):
		def OnInit(self):
			frame = MainFrame()
			frame.Show()
			return True

	#import toolib.startup
	#toolib.startup.hookStd()
	App().MainLoop()

if __name__ == '__main__':
	import toolib.startup
	import locale
	#locale.setlocale(locale.LC_CTYPE, "Ukrainian_Ukraine.1251")
	locale.setlocale(locale.LC_CTYPE, "Russian_Russia.1251")
	toolib.startup.hookStd()
	toolib.startup.setDefaultEncoding()
	main()
