import wx

"""
           EXCEL            openoffice

CORNER:    219 216 209      212 208 200
LABEL_SEL  182 189 210      172 174 181


(166, 202, 240)
        SYS_COLOUR_GRADIENTACTIVECAPTION
(255, 255, 225)
        SYS_COLOUR_INFOBK
( 58, 110, 165)
        SYS_COLOUR_BACKGROUND
        SYS_COLOUR_DESKTOP
( 10,  36, 106)
        SYS_COLOUR_ACTIVECAPTION
        SYS_COLOUR_HIGHLIGHT
        SYS_COLOUR_MENUHILIGHT
(255, 255, 255)
        SYS_COLOUR_3DHIGHLIGHT
        SYS_COLOUR_3DHILIGHT
        SYS_COLOUR_BTNHIGHLIGHT
        SYS_COLOUR_BTNHILIGHT
        SYS_COLOUR_CAPTIONTEXT
        SYS_COLOUR_HIGHLIGHTTEXT
        SYS_COLOUR_LISTBOX
        SYS_COLOUR_WINDOW
(128, 128, 128)
        SYS_COLOUR_3DSHADOW
        SYS_COLOUR_APPWORKSPACE
        SYS_COLOUR_BTNSHADOW
        SYS_COLOUR_GRAYTEXT
        SYS_COLOUR_INACTIVECAPTION
(  0,   0,   0)
        SYS_COLOUR_BTNTEXT
        SYS_COLOUR_INFOTEXT
        SYS_COLOUR_MAX
        SYS_COLOUR_MENUTEXT
        SYS_COLOUR_WINDOWFRAME
        SYS_COLOUR_WINDOWTEXT
(  0,   0, 128)
        SYS_COLOUR_HOTLIGHT
( 64,  64,  64)
        SYS_COLOUR_3DDKSHADOW
(192, 192, 192)
        SYS_COLOUR_GRADIENTINACTIVECAPTION
(212, 208, 200)
        SYS_COLOUR_3DFACE
        SYS_COLOUR_3DLIGHT
        SYS_COLOUR_ACTIVEBORDER
        SYS_COLOUR_BTNFACE
        SYS_COLOUR_INACTIVEBORDER
        SYS_COLOUR_INACTIVECAPTIONTEXT
        SYS_COLOUR_MENU
        SYS_COLOUR_MENUBAR
        SYS_COLOUR_SCROLLBAR

wxSYS_COLOUR_SCROLLBAR  The scrollbar grey area.  
wxSYS_COLOUR_BACKGROUND  The desktop colour.  
wxSYS_COLOUR_ACTIVECAPTION  Active window caption.  
wxSYS_COLOUR_INACTIVECAPTION  Inactive window caption.  
wxSYS_COLOUR_MENU  Menu background.  
wxSYS_COLOUR_WINDOW  Window background.  
wxSYS_COLOUR_WINDOWFRAME  Window frame.  
wxSYS_COLOUR_MENUTEXT  Menu text.  
wxSYS_COLOUR_WINDOWTEXT  Text in windows.  
wxSYS_COLOUR_CAPTIONTEXT  Text in caption, size box and scrollbar arrow box.  
wxSYS_COLOUR_ACTIVEBORDER  Active window border.  
wxSYS_COLOUR_INACTIVEBORDER  Inactive window border.  
wxSYS_COLOUR_APPWORKSPACE  Background colour MDI applications.  
wxSYS_COLOUR_HIGHLIGHT  Item(s) selected in a control.  
wxSYS_COLOUR_HIGHLIGHTTEXT  Text of item(s) selected in a control.  
wxSYS_COLOUR_BTNFACE  Face shading on push buttons.  
wxSYS_COLOUR_BTNSHADOW  Edge shading on push buttons.  
wxSYS_COLOUR_GRAYTEXT  Greyed (disabled) text.  
wxSYS_COLOUR_BTNTEXT  Text on push buttons.  
wxSYS_COLOUR_INACTIVECAPTIONTEXT  Colour of text in active captions.  
wxSYS_COLOUR_BTNHIGHLIGHT  Highlight colour for buttons (same as wxSYS_COLOUR_3DHILIGHT).  
wxSYS_COLOUR_3DDKSHADOW  Dark shadow for three-dimensional display elements.  
wxSYS_COLOUR_3DLIGHT  Light colour for three-dimensional display elements.  
wxSYS_COLOUR_INFOTEXT  Text colour for tooltip controls.  
wxSYS_COLOUR_INFOBK  Background colour for tooltip controls.  
wxSYS_COLOUR_DESKTOP  Same as wxSYS_COLOUR_BACKGROUND.  
wxSYS_COLOUR_3DFACE  Same as wxSYS_COLOUR_BTNFACE.  
wxSYS_COLOUR_3DSHADOW  Same as wxSYS_COLOUR_BTNSHADOW.  
wxSYS_COLOUR_3DHIGHLIGHT  Same as wxSYS_COLOUR_BTNHIGHLIGHT.  
wxSYS_COLOUR_3DHILIGHT  Same as wxSYS_COLOUR_BTNHIGHLIGHT.  
wxSYS_COLOUR_BTNHILIGHT  Same as wxSYS_COLOUR_BTNHIGHLIGHT.  
"""

app = wx.App()
app.MainLoop()

colors = [i for i in dir(wx) if i.startswith('SYS_COLOUR_')]
colors.sort()

rev = {}

for i in colors:
	c = getattr(wx, i)
	cc = wx.SystemSettings.GetColour(c)

	scolor = "(%3s, %3s, %3s)" % tuple(cc)

	rev.setdefault(scolor, []).append(i)

	#print "%40s  %3s   %s" % (i, c, scolor)

for color, names in rev.iteritems():
	print color
	names.sort()
	for i in names:
		print '\t', i

del app