# -*- coding: Cp1251 -*-
###############################################################################
# Program:   Sula 0.8
'''
	Add absolute-locale fields to localized fields. So value in
	localized field is a result of localize function of value in
	absolute-locale field. Example value17 = _(abs_value17), ets
	'Контракт' = _('Contract')
'''
__author__  = "Lesha Strashko"
__date__	= "$Date: 2008/04/11 15:36:47 $"
__version__ = "$Revision: 1.3 $"
__credits__ = "No credits today"
# $Source: D:/HOME/cvs/toolib/scripts/i18n/add_abs_fields.py,v $
###############################################################################

configPath = 'sulib.config.db'
uId = 0


import dbengine
from toolib.utility.timer import Timer

def runScript():
	timer = Timer()
	timer.start()
	factory = dbengine.factory(configPath, uId)
	for classId in factory.getDescriptionManager().getClassIds():
		cLass = factory.getClassDescriptor(classId)
		for propD in cLass.iterProps():
			if propD.isLocalizable():
				absPropId = propD.getAbsPropertyId()
				if factory.getUtility().getDbSchema().hasColumn(cLass.getId(), absPropId):
					## column allready exists
					print 'column: %s allready exists in class: %s, skipping...' % (
						cLass.getId(),
						absPropId
					)
				else:
					## add column to table
					sql = factory.getUtility().getDbSchema().sqlAddColumn2Class(
						cLass.getId(),
						absPropId
					)
					factory.executeDML(sql)
					print 'field %s added to class: %s' % (
						cLass.getId(),
						absPropId
					)

if __name__ == '__main__':
	runScript()

