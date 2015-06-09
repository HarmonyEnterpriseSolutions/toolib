import os

good = []
bad = []

for i in xrange(32, 256):
	s = chr(i)
	
	try:
		f = open("a"+s+"a", "wt")
		f.close()
		os.remove("a"+s+"a")
		#rint "- Ok"
		good.append(s)
	except Exception, e:
		print "%s [%s]" % (i, s),
		print e.__class__, e
		bad.append(s)
	
	try:
		f = open(s, "wt")
		f.close()
		os.remove(s)
		#rint "- Ok"
		good.append(s)
	except Exception, e:
		print "%s [%s]" % (i, s),
		print e.__class__, e
		bad.append(s)
	
	
#print "".join(good)
#print `"".join(bad)`
