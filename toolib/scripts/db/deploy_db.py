'''
	Deploy database by valid dbengine configuration file into DBMS.
	Customization:
		configPath		: <configPath>
		dbTarget		: {
							'host':<dbms_host>,
							'dbname':<db_name>,
							'user':<dbms_user_with_create_database_privileges>,
							'passwd':<users_password>
						  }
	Attention   : in config, DBMS user must have rights to create database.
	Warning		: if database exists - its droped!!!
'''

__author__  = "Lesha Strashko"
__date__	= "$Date: 2003/11/18 13:02:02 $"
__version__ = "$Revision: 1.3 $"
__credits__ = "No credits today"


configPath = 'sulib.config.db'
dbTarget = {
		'host': 'pavel2',
		'dbname': 'sula08_db_fedastest',
		'user': 'root',
		'passwd':'pipirka',
	}
uId = 0


import dbengine
from toolib.utility.timer		import Timer


def runScript(configPath, dbTarget):
	factory = dbengine.factory(configPath, uId)
	dbname = dbTarget.get('dbname', None)
	## make current db - None(else first sql-query will be failed, because of
	## MySQLdb.connect will try to connect to existing database)
	dbTarget['dbname'] = ""
	factory.setTarget(dbTarget)
	## print factory
	print "Deploying database %s" % dbname
	timer = Timer()
	timer.start()
	dbSchema = factory.getUtility().getDbSchema()

	if dbname is not None :
		if factory.getRawAccess().isDatabaseExists(dbname) :
			factory.getRawAccess().removeDatabase(dbname)
		factory.getRawAccess().createDatabase(dbname)
		factory.getRawAccess().setCurrentDatabase(dbname)
	cnt = 0
	for classId in factory.getDescriptionManager().getClassIds():
		classDescr = factory.getClassDescriptor(classId)
		print "+ table %s" % classDescr.getId(),
		query = dbSchema.sqlFromClassDescriptor(classDescr)
		factory.executeDML(query)
		#print query
		for keySql in dbSchema.sqlGenerateClassKeys(classDescr) :
			factory.executeDML(keySql)
		print "done."
		cnt += 1
	print 'Total tables: \t%s' % cnt
	print "Deploying database %s is done(time:%s)." % (dbname, timer.stop())


if __name__ == '__main__':
	runScript(configPath, dbTarget)
