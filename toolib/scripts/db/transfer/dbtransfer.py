###############################################################################
"""
	Project: Database transfer utility
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2004/02/18 11:59:28 $"
__version__ = "$Revision: 1.1 $"
# $Source: D:/HOME/cvs/toolib/scripts/db/transfer/dbtransfer.py,v $
###############################################################################

import os, sys, time
from DatabaseDescriptor import DatabaseError
from TransferDocument import DbTransfer
from TransferContext import TransferContext

PROFILE=0

def VERSION():
	from TransferDocument import __version__
	return __version__[len("$Revision:"):-1].strip() or "?"

def usage():
	print >> sys.stderr, "Usage: python %s <xml-config> [<indb> [<outdb> [<host> [<user> [<password>]]]]] > output.sql" % (sys.argv[0])

def main():
	reload(sys)
	sys.setdefaultencoding("Cp1251")
	print >> sys.stderr, "dbtransfer: database migration utility version %s (c) Abrisola, 2004" % (VERSION(),)
	
	config = None
	dbin = "${inputdb}"
	dbout = "${outputdb}"
	host = ""
	user = ""
	password = ""
	
	try:
		config	= sys.argv[1]
		dbin	= sys.argv[2]
		dbout	= sys.argv[3]
		host	= sys.argv[4]
		user	= sys.argv[5]
	except IndexError:
		usage()		
	try:
		password= sys.argv[6]
	except IndexError:
		pass
	
	print >> sys.stderr
	print >> sys.stderr, "  Config:", config
	print >> sys.stderr, "  In db :", dbin
	print >> sys.stderr, "  Out db:", dbout
	print >> sys.stderr, "  Host  :", host
	print >> sys.stderr, "  User  :", user

	if config == "None": config = None

	if config and not os.path.exists(config):
		print >> sys.stderr, "* Config file not foud. Terminating"
		return 1

	if not password:
		from getpass import getpass
		password = getpass("Enter database password: ")

	print >> sys.stderr
	transfer = DbTransfer()

	context = TransferContext(host, dbin, dbout, user, password)
	try:
		print >> sys.stderr, "  Comparing databases structure..."
		transfer.loadFromContext(context)
	except DatabaseError, e:
		print >> sys.stderr, "*", e[0], e[1]
		print >> sys.stderr, "  Default sql will not be generated!"

	if config:
		print >> sys.stderr, "  Updating from config..."
		transfer.updateFromXmlFile(config)
	else:
		print >> sys.stderr, "* No configuration. Configurated sql will not be generated!"
		
	print >> sys.stderr, "  Writing output sql..."

	print "# Database migration script: %s to %s on %s" % (dbin, dbout, host)
	print "# Generated on %s by dbtransfer version %s" % (time.asctime(), VERSION())
	print "# Source migration document:", config
	print

	transfer.writeTransferSql(context, sys.stdout)
	
	print >> sys.stderr, "  Done"
	
if __name__=="__main__":
	if PROFILE:
		import profile
		profile.run("sys.exit(main() or 0)")
	else:
		sys.exit(main() or 0)
