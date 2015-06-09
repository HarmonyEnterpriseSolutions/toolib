###############################################################################
# Script:
'''
	Extracts localizable strings from db(dbengine supportable) and make file
	...
	_('strI')
	_('strI+1')
	...
	wich is incited later to pygettext for extraction and following
	localization.
'''

__author__  = "Lesha Strashko"
__date__	= "$Date: 2003/11/18 13:02:02 $"
__version__ = "$Revision: 1.2 $"
__credits__ = "No credits today"
# $Source: D:/HOME/cvs/toolib/scripts/i18n/extract_dbtext.py,v $
###############################################################################

import dbengine
import sys
from toolib.utility.timer import Timer


def runScript(configPath, tmpOutfileName = 'stringsFromDB.locale'):
	timer = Timer()
	print '+ Extracting localizable strings from DB:'
	print '\tconfig:%s' % configPath
	print '\toutFile:%s' % tmpOutfileName
	timer.start()
	factory = dbengine.factory(configPath)
	## create file for output
	outFile = file(tmpOutfileName, 'w')
	sCounter = 0
	try:
		## suck strings from db
		for classId in factory.getDescriptionManager().getClassIds():
			cLass = factory.getClassDescriptor(classId)
			if cLass.isLocalizable():
				print 'processing class %s' % cLass.getId()
				outFile.write("## ++++++++++++++ Processing class %s:\n" % cLass.getId())
				objSet = cLass.iterObjects()
				for obj in objSet:
					outFile.write("# object:%s\n" % obj.getUniqueId())
					for propD in cLass.iterProps():
						if propD.isLocalizable():
							#print "\tprocessing property %s:" % propD.getId()
							value = obj[propD.getAbsPropertyId()].getValue()
							if (value is not None) and value != "":
								outFile.write('_("%s")\t# %s\n' % (value, propD.getId()))
								sCounter += 1
							else:
								str =  '#+ Warning: Object(%s), property(%s) is not set.' % (
									obj.getUniqueId(),
									propD.getAbsPropertyId()
								)
								outFile.write(str)
	finally:
		outFile.close()
	print '+ Finished strings:%s time:%s' % (sCounter, timer.stop())

def main():
	usage = '''
DB extract script, usage:
exctract_dbtext configPath [outFilePath]
	configPath		- dbengine config path
	outFile			- location file for all extracted strings
p2003 Abrisola
	'''
	if len(sys.argv) < 2:
		print usage
		return
	elif len(sys.argv) == 2:
		runScript(sys.argv[1])
	else:
		runScript(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
	main()


