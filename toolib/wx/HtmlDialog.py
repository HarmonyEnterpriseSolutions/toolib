#################################################################
# Program: Toolib
"""

"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2004/10/19 14:54:08 $"
__version__ = "$Revision: 1.3 $"
# $Source: D:/HOME/cvs/toolib/wx/HtmlDialog.py,v $
#
#################################################################
import wx
import wx.html
import webbrowser

# This shows how to catch the OnLinkClicked non-event.  (It's a virtual
# method in the C++ code...)
class HtmlWindow(wx.html.HtmlWindow):
	def __init__(self, parent, id=-1):
		wx.html.HtmlWindow.__init__(self, parent, id)

	def OnLinkClicked(self, linkinfo):
		webbrowser.open(linkinfo.GetHref())

class HtmlDialog(wx.Dialog):

	def __init__(self, parent=None, id=-1, title="Html Dialog", pos=wx.DefaultPosition, size=(400, 400), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER):
		wx.Dialog.__init__(self, parent, id, title, pos, size, style)

		self.htmlWnd = HtmlWindow(self)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.htmlWnd, 1, wx.EXPAND | wx.ALIGN_BOTTOM | wx.ALL, 0)

##		self.__southPanel = wx.Panel(self, -1)
##		sizer.Add(self.__southPanel, 0, wx.ALL | wx.GROW)

		sizer.Add(
			wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL),
			0, wx.GROW, 0)

		ok = wx.Button(self, -1, "Ok")
		sizer.Add(ok, 0, wx.ALIGN_CENTER | wx.ALL, 10)

		self.SetSizer(sizer)

		wx.EVT_BUTTON(ok, ok.GetId(), self.OnOk)

		#self.Layout()
		#self.Fit()

##  def getSouthPanel(self):
##		return self.__southPanel

	def OnOk(self, event):
		self.Hide()
		##self.Destroy()

	def loadUrl(self, url):
		self.htmlWnd.LoadPage(url)

	def setHtml(self, html):
		self.htmlWnd.SetPage(html)

	def getHtmlWindow(self):
		return self.htmlWnd

if __name__ == '__main__':
	class TestApp(wx.PySimpleApp):
		def OnInit(self):
			dlg = HtmlDialog()
			dlg.loadUrl("http://www.yahoo.com");
			dlg.ShowModal()
			dlg.Destroy()
			return True

	TestApp().MainLoop()

