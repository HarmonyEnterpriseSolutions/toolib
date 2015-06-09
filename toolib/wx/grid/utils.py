import wx

boolInternalValues = ["", "1"]

if wx.__version__.startswith("2.7.2.0"):
	boolInternalValues.reverse()

def boolToInternal(value):
	return boolInternalValues[int(bool(value))]


boolFromInternal = {}
for i, v in enumerate(boolInternalValues):
	boolFromInternal[v] = bool(i)

del i
del v

boolFromInternal = boolFromInternal.get
