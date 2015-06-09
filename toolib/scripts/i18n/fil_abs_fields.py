###############################################################################
# Program:   Sula 0.8
'''
	Fill absolute locale fields from relative field values. Script needed in such case:
		you allready have a table filled with data. To localize it you need to
		put all data into absolute locale fields. So this script do such a thing
		automatically.

'''
__author__  = "Lesha Strashko"
__date__	= "$Date: 2003/11/18 13:02:02 $"
__version__ = "$Revision: 1.2 $"
__credits__ = "No credits today"
# $Source: D:/HOME/cvs/toolib/scripts/i18n/fil_abs_fields.py,v $
###############################################################################


configPath  = 'sulib.config.db'
uId			= 0



import dbengine
from toolib.utility.timer import Timer

def runScript():
	timer = Timer()
	timer.start()
	factory = dbengine.factory(configPath, uId)

	for classId in factory.getDescriptionManager().getClassIds():
		cLass = factory.getClassDescriptor(classId)
		if cLass.isLocalizable():
			## localizable class
			print 'processing class %s' % cLass.getId()
			objSet = cLass.iterObjects()
			for obj in objSet:
				for propD in cLass.iterProps():
					if propD.isLocalizable():
						## set value of absolute property from value of relative property
						obj[propD.getAbsPropertyId()].setValue(
							obj[propD.getId()].getValue()
						)
			objSet.save()

if __name__ == '__main__':
	runScript()

