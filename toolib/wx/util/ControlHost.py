# -*- coding: Cp1251 -*-
###############################################################################
#
'''
'''
__author__  = "Oleg Noga"
__date__	= "$Date: 2005/12/07 19:53:53 $"
__version__ = "$Revision: 1.2 $"
# $Source: D:/HOME/cvs/toolib/wx/util/ControlHost.py,v $
###############################################################################
import wx
from toolib.util.OrderDict import OrderDict

class ControlHost(object):
	"""
	registers labels, controls, validators
	validates, produces error messages, 
	gathers data

	"""

	_POS_CONTROL   = 0
	_POS_VALIDATOR = 1
	_POS_LABEL     = 2
	
	def __init__(self):
		self.__controls = OrderDict()
		
	def getControlIds(self):
		return self.__controls.keys()

	def registerControl(self, id, control, validator=None, label=None):
		self.__controls[id] = (control, validator, label)

	def validate(self):
		errors = []
		for id, (control, validator, label) in self.__controls.iteritems():
			if validator is not None and control.IsEnabled():
				value = self._getControlValue(id)
				try:
					validator.validate(value, label)
				except ValueError, e: 
					errors.append(e[0])
		return errors

	def getControl(self, id):
		return self.__controls[id][self._POS_CONTROL]
		
	def _getControlValue(self, id):
		c = self.getControl(id)
		if hasattr(c, 'getDate'):
			return c.getDate()
		else:
			return c.GetValue()

	def getValidator(self, id):
		return self.__controls[id][self._POS_VALIDATOR]

	def setValidator(self, id, validator):
		control, oldValidator, label = self.__controls[id]
		self.registerControl(id, control, validator, label)

	def getLabel(self, id):
		return self.__controls[id][self._POS_LABEL]
		
	def setLabel(self, id, label):
		control, validator, oldLabel = self.__controls[id]
		self.registerControl(id, control, validator, label)

	def getData(self):
		d = {}
		for id in self.__controls.iterkeys():
			d[id] = self._getControlValue(id)
		return d
