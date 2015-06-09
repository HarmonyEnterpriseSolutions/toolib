# -*- coding: Cp1251 -*-
from toolib.util.strings import rsplit
from toolib.text.numberspeller.NumberSpeller import NumberSpeller, Unit

UNITS = {
	None		: Unit(Unit.MALE,),
	u"гривня"	: Unit(Unit.FEMALE, u"гривня",  u"гривні",  u"гривень"),
	u"копійка"	: Unit(Unit.FEMALE, u"копійка", u"копійки", u"копійок"),
	u"грн."		: Unit(Unit.FEMALE, u"грн."),
	u"коп."		: Unit(Unit.FEMALE, u"коп."),
}

def main():
	import wx

	class MainFrame(wx.Frame):
		def __init__(self, parent=None):
			wx.Frame.__init__(self, parent, -1, 'Начитувач сум версія 0.02 (c) Абрісола, 2005, 2010', style=wx.DEFAULT_FRAME_STYLE)# | wx.MAXIMIZE
			split = wx.SplitterWindow(self, -1)
			style = wx.TE_MULTILINE 
			self._source = wx.TextCtrl(split, -1, style=style)
			self._target = wx.TextCtrl(split, -1, style=style | wx.TE_READONLY)
			split.SplitHorizontally(self._target, self._source)

			self._source.Bind(wx.EVT_TEXT, self.OnTextChanged)
			self._speller = NumberSpeller('uk_UA')

		def spell(self, h, l):
			hd = ' '.join(rsplit(str(h), 3))
			hs, hu = self._speller.spellNumber(h, UNITS[u'грн.'])
			ls, lu = self._speller.spellNumber(l, UNITS[u'коп.'])
			ld = "%02d" %(l,)
			return "%s %s %s %s" % (hs.capitalize(), hu, ld, lu)

		def processLine(self, line):
			try:
				line = line.strip()
				if line:
					values = line.replace(',', '.').replace(' ', '').split('.')
					h = int(values[0])
					try:
						l = int(round(float('.' + values[1]) * 100))
						if l >= 100:
							h += l / 100
							l %= 100
					except IndexError:
						l = 0

					return self.spell(h, l)
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
