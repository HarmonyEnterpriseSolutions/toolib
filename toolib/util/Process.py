#################################################################
# Program:   Toolib
"""
Starts process with sreams to comunicate
Like java.lang.Process 

Note: waitFor() is interesting!
	  refer message


David Bolen db3l@fitlinxx.com 
27 Mar 2001 19:13:29 -0500 

Previous message: Getting all the *files* from a directory -- A better way?? 
Next message: Jython and JPython Questions...How similar to Python, Tkinter? 
Messages sorted by: [ date ] [ thread ] [ subject ] [ author ] 

--------------------------------------------------------------------------------

Nahuel Greco <ngreco@softhome.net> writes:

> Hi, im doing the following thing in Windows 98 / Activestate Python 2.0:
> 
> 	import win32pipe
> 
> 	cmd = "c:\\zebedee\\zebedee.exe -d 127.0.0.1"
> 	pipes = win32pipe.popen3(cmd,'t')
> 
> 	#Now.. if i do:
> 
> 	pipes[0].close()
> 	pipes[1].close()
> 	pipes[2].close()  # in this line, the program hangs.
> 
> 
> If i follow another closing order, the program stills hangs in the last
> close() call .. i think that when all the pipes are closed.. win32pipe
> try to close the child program.. and wait for that close.. but, the
> child program never exit.

Yes - the purpose of the popen# calls is to connect you to the child
process so you can interact with it.  Upon closing that final handle,
it'll wait for the process to exit so it can return any exit code.

If you don't actually want that interaction, you can use os.system()
to start off the process instead, but you won't be able to trap the
output, and you'll still have the long-lived problem you mention next.

Sometimes the order that you close the handles is important, in terms
of closing the right one so that the process decides it should exit
(say, when it's stdin goes away).

> If i do not close the pipes, when my python script exits, the child
> program is still running (i dont want that).

That's more a Windows thing than anything else.  There's no official
parent/child relationship like there is under Unix, so Windows will
let processes continue running even after the process that started
them exits, and even if they didn't want to disassociate themselves.
(This causes me no end of grief with respect to our systems management
tools and ensuring that no stray processes ever remain on failures).

It sounds like what you want to do is to ensure that you cause the
executable to exit before you actually exit.  That can be specific to
the executable you are using.

In looking at the product page you referenced (and the source), I
don't see any way via stdin to tell zebedee to exit - and with popen()
a message via stdin is really the only way you have available to you.
The main server receive loop - whether detached or not - actually
blocks on an accept() call, so it's not looking for any other source
of input.  It appears to just expect to be terminated when it's
supposed to exit.

You might try looking around for a process list/kill utility for 98,
and then using that to find out the pid for the started zebedee
process, and explicitly killing it when you want to terminate.

Alternatively, since it comes with source, my bet is that if you just
tweaked the ServerListener function in zebedee.c so that instead of
blocking in the accept(), it did a timeout select on the socket and on
a timeout, checked stdin for input as a reason for exiting, you could
easily shut it down from the Python script by just writing something
to its stdin.  (The Unix way to do this would be to include
fileno(stdin) in the select, but Windows can only select on sockets -
alternatively if you didn't mind being Windows specific you could use
native Win32 calls to wait on both the socket and stdin to the same
effect).

--
-- David
-- 
/-----------------------------------------------------------------------\
 \               David Bolen            \   E-mail: db3l@fitlinxx.com  /
  |             FitLinxx, Inc.            \  Phone: (203) 708-5192    |
 /  860 Canal Street, Stamford, CT  06902   \  Fax: (203) 316-5150     \
\-----------------------------------------------------------------------/

"""

__author__  = "Oleg Noga"
__date__	= "$Date: 2006/11/22 17:58:18 $"
__version__ = "$Revision: 1.2 $"
# $Source: D:/HOME/cvs/toolib/util/Process.py,v $
#################################################################

import os

class Process:

	def __init__(self, command, mode="t", separate_stderr=1):
		if separate_stderr:
			self.stdin, self.stdout, self.stderr = os.popen3(command, mode)
		else:
			self.stdin, self.stdout = os.popen4(command, mode)
			self.stderr = self.stdout
		#self.stdout = os.popen(command, "rw")

	def destroy(self):
		"""
		Kills the subprocess. Not implemented. How to get pid under win32?
		"""
		raise NotImplementedError, 'yet'

	def getErrorStream(self):
		"""Gets the error stream of the subprocess"""
		return self.stderr

	def getInputStream(self):
		"""Gets the input stream of the subprocess."""
		return self.stdin

	def getOutputStream(self):
		"""Gets the output stream of the subprocess."""
		return self.stdout

	def waitFor(self):
		"""
		causes the current thread to wait, if necessary, until 
		the process represented by this Process object has terminated.
		"""
		rco = self.stdout.close()
		rce = None
		if self.stderr != self.stdout:
			rce = self.stderr.close()
		rci = self.stdin.close()
		return rci or rco or rce or 0

if __name__ == "__main__":
	java = Process("1.sh")

	out = java.getOutputStream()

	#print "ERR----------------------"
	#
	#err = java.getErrorStream()
	#for l in err.readlines():
	#	print l,

	print "OUT----------------------"

	for l in out.readlines():
		print l,
	
	print java.waitFor()

