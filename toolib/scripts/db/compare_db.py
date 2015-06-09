 ###############################################################################
# Script:
'''
	Compares db from dbengine config with low database. Generates SQL needed
	to upgrade database to config(std out).
	Now detects:
		- absent classes
		- absent properties in classes
		- Primary Key consistency
		- isRequired attribute consistency
		- ...
	Parameters:
		configPath: <pythion_path_to_dbengine_config>,
		compare2database: <dbms_db_name>,
		sqlFilePath(optional): <difference_sql_output_file_os_path>

	!!!Serious adjustments needed.
'''
__author__  = "Lesha Strashko"
__date__	= "$Date: 2004/03/01 14:07:15 $"
__version__ = "$Revision: 1.3 $"
__credits__ = "No credits today"
# $Source: D:/HOME/cvs/toolib/scripts/db/compare_db.py,v $
###############################################################################

import dbengine
import sys
from toolib.utility.timer import Timer

compare2database = 'sula_db_07k'
configPath = 'sulib.config.db'
sqlFilePath = 'diffSQL.sql'


def runScript(configPath, compare2database, sqlFilePath = None):
	timer = Timer()
	print '+ Comparing DB:'
	timer.start()
	factory = dbengine.factory(configPath)

	## reset dbtarget
	target = factory.getTarget()
	target['dbname'] = compare2database
	factory.setTarget(target)
	print factory
	## create file for output
	outSqlList = []
	for classId in factory.getDescriptionManager().getClassIds():
		cLass = factory.getClassDescriptor(classId)
		compareClassDescriptor(cLass, outSqlList)
		#print rs
	print ' ++++++++++ SQL ++++++++++++++'
	for sqlStr in outSqlList:
		print sqlStr
	if sqlFilePath is not None:
		file = open(sqlFilePath, 'w')
		file.write('\n'.join(outSqlList))
		file.close()
	print '+ Finished. Time:%s' % (timer.stop())

fmap = {'field':0, 'type':1, 'null':2, 'key':3, 'default':4, 'extra':5}


def compareClassDescriptor(cLass, outSqlList):
	'''
	Compare config info about classDescriptor to table schema
	in database.
	'''
	print '+ processing class %s' % cLass.getId()
	if cLass.getId() not in cLass.getFactory().getRawAccess().getTableIds():
		print ' raw: class %s not found in db' % cLass.getId()
		outSqlList.append(
			cLass.getFactory().getUtility().sqlFromClassDescriptor(cLass)
		)
		return
	for propD in cLass.iterProps():
		comparePropertyDescriptor(propD, outSqlList)

def comparePropertyDescriptor(propD, outSqlList):
	'''
	Compare config info about propertyDescriptor to field schema
	in database.
	'''
	if propD.isPersistent():
		#find self in rs
		rs = propD.getFactory().executeDQL('SHOW COLUMNS FROM %s LIKE "%s"' % (
			propD.getClassId(),
			propD.getId()
			)
		)
		if rs.isEmpty():
			print ' raw: field %s: not found.' % (propD.getId())
			outSqlList.append(propD.getFactory().getUtility().sqlAddColumn2Class(
				propD.getClassId(),
				propD.getId()
				)
			)
			return
		#check isRequired
		isRequired = 1
		if rs.getItem(0, fmap['null']) == 'YES':
			isRequired = 0
		if propD.isRequired() != isRequired:
			print ' raw: field %s: isRequired config(%s) != db(%s)' % (
				propD.getId(),
				propD.isRequired(),
				isRequired
			)
		#check primary key
		if propD.isPrimaryKey():
			if rs.getItem(0, fmap['key']) != 'PRI':
				print ' raw: field %s seems to be primary key, but not' % (propD.getId())


def main():
	runScript(configPath, compare2database, sqlFilePath)

if __name__ == '__main__':
	main()


