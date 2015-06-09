import wx
from CellAttributes import CellAttributes

def monochrome(color):
	i = (color.Red() + color.Green() + color.Blue()) / 3
	return wx.Colour(i,i,i,color.Alpha())

CELL_ATTRIBUTES_DICT = {
	'default' : CellAttributes(
		textColor   = 'BLACK',
		bgColor     = 'WHITE',
		borderColor = 'GRAY',
		textAlign   = wx.ALIGN_CENTER | wx.ALL,
		font        = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL),
		minHeight   = 20,
	),
	'header' : CellAttributes(
		textColor       = 'BLUE',
		bgColor         = wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNFACE),
		borderHighlight = wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT),
		borderShadow    = wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNSHADOW),
		yWeight         = 0.5,
		minHeight       = 20,
		maxHeight       = 30,
	),
	'week' : CellAttributes(
		bgColor     = wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNFACE),
		borderHighlight = wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT),
		borderShadow    = wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNSHADOW),
		minWidth        = 20,
		maxWidth        = 70,
	),
	'otherMonth' : CellAttributes(
		textColor   = wx.SystemSettings_GetColour(wx.SYS_COLOUR_GRAYTEXT),
	),
	'currentDay' : CellAttributes(
		borderColor = 'BLACK',
		borderWidth = 3,
	),
	'selectedDay' : CellAttributes(
		bgColor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT),
		textColor = 'WHITE',
	),
	'currentDayUnfocused' : CellAttributes(
		borderColor = 'GRAY',
		borderWidth = 3,
	),
	'selectedDayUnfocused' : CellAttributes(
		bgColor = monochrome(wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT)),
		textColor = 'WHITE',
	),
	'holiday' : CellAttributes(
		textColor = 'RED',
	),
	'today' : CellAttributes(
		borderColor = 'RED',
		borderWidth = 3,
	),
	'label' : CellAttributes(
		textColor   = 'BLUE',
		bgColor     = 'WHITE',
		#bgColor         = wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNFACE),
		#borderHighlight = wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNSHADOW),
		#borderShadow    = wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT),
		textAlign   = wx.ALIGN_CENTER | wx.ALL,
		textIndent  = 1,
		font        = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL),

	),
}

del monochrome