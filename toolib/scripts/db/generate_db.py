'''
	Generates SQL-script(enough to create database) by dbengine config.
	Customization:
		configPath		: <configPath>,
		withDBCreate	: <is_SQL_CREATE_DATABASE_%DBNAME%_inserted>,
		sqlFilePath		: <output_sql_script_default_%dbname%.sql>
'''

__author__  = "Lesha Strashko"
__date__	= "$Date: 2003/11/18 13:02:02 $"
__version__ = "$Revision: 1.2 $"
__credits__ = "No credits today"


configPath = 'sulib.config.db'
sqlFilePath = None
withDBCreate = 1
uId = 0


import dbengine
from toolib.utility.timer		import Timer


def runScript(configPath, withDBCreate = 1, sqlFilePath = None):
	factory = dbengine.factory('sulib.config.db', 0)

	dbname = factory.getTarget()['dbname']
	if withDBCreate:
		sqlStr = "CREATE DATABASE %s;\n" % dbname
	else:
		sqlStr = ''
	sqlStr = "%s%s" % (
		sqlStr,
		factory.getUtility().generateDatabaseSql()
	)
	if sqlFilePath is None:
		sqlFilePath = "%s.sql" % factory.getTarget()['dbname']
	f = file(sqlFilePath, 'w')
	f.write('')
	f.write(sqlStr)
	f.close()

if __name__ == "__main__":
	runScript(configPath, withDBCreate, sqlFilePath)


