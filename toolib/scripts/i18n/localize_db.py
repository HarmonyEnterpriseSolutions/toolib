###############################################################################
# Script:
'''
'''
__author__  = "Lesha Strashko"
__date__	= "$Date: 2004/11/12 15:11:27 $"
__version__ = "$Revision: 1.3 $"
__credits__ = "No credits today"
# $Source: D:/HOME/cvs/toolib/scripts/i18n/localize_db.py,v $
###############################################################################

uId = 0



import dbengine
import sys
from toolib.utility.timer import Timer


def runScript(configPath):
	timer = Timer()
	print '+ Localizing DB:'
	timer.start()
	factory = dbengine.factory(configPath, uId)

	oks = 0
	errors = 0
	warnings = 0
	
	for classId in factory.getDescriptionManager().getClassIds():
		cd = factory.getClassDescriptor(classId)
		if cd.isLocalizable():
			print
			print 'processing class %s' % cd.getId()
			set = cd.iterObjects()
			for obj in set:
				for pd in cd.iterProps():
					if pd.isLocalizable():
						print "%20s:%-7s" % (pd.getId(), obj.getId()),
						value = obj[pd.getAbsPropertyId()].getValue()
						if value:
							uvalue = factory._(value)
							obj[pd.getId()].setValue(uvalue)
							oks += 1
							print ' value set ok:      "%s"->"%s"' % (value, uvalue)
						else:
							uvalue = obj[pd.getId()].getValue()
							if uvalue:
								print ' ! Value unchanged: %s->"%s"' % (repr(value), uvalue)
								errors += 1
							else:
								print ' * unused value,    %s->%s' % (repr(value), repr(uvalue))
								warnings += 1
			set.save()
			#print '...done'

	print '---------------------------------------------------'
	print '+ Finished in %s' % (timer.stop(),)
	print '  \tSuccesses:', oks
	print '  \tErrors   :', errors
	print '  \tWarnings :', warnings
	print '  \tTotal    :', oks + errors + warnings

def main():
	usage = '''
Locale DB script, usage:
exctract_dbtext configPath
	configPath		- dbengine config path
p2003 Abrisola
	'''
	if len(sys.argv) == 2:
		runScript(sys.argv[1])
	else:
		print usage
		return

if __name__ == '__main__':
	main()


