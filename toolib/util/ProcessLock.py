import os

SLEEP = 100

class LockAsquireTimeout(Exception):
	pass

if os.name == 'nt':

	import win32api
	import win32event
	import winerror

	class ProcessLock(object):

		def __init__(self, name, acquire=True, sleep=100):
			self.__name = name
			self.__mutex = None
			self.__sleep = sleep
			if acquire:
				self.acquire()

		def acquire(self, timeout=-1):
			if self.__mutex is None:
				while True:
					self.release()
					self.__mutex = win32event.CreateMutex(None, False, "toolib.util.ProcessLock_" + self.__name)
					e = win32api.GetLastError()
					#rint e
					if e == 0:
						break
					elif e == winerror.ERROR_ALREADY_EXISTS:
						self.release()
						if timeout == -1:
							win32api.Sleep(self.__sleep)
						elif timeout == 0:
							t = min(timeout, self.__sleep)
							timeout -= t
							win32api.Sleep(t)
						else:
							self.release()
							raise LockAsquireTimeout()
					else:
						self.release()
						raise OSError("CreateMutext error: %s" % self.__lastError)

		def __nonzero__(self):
			return self.__mutex is not None
						
		def release(self):
			if self.__mutex:
				win32api.CloseHandle(self.__mutex)
				self.__mutex = None

else:

	import tempfile
	import time

	class ProcessLock(object):

		def __init__(self, name, acquire=True, sleep=1000):
			self.__sleep = sleep 
			self.__path = os.path.join(tempfile.gettempdir(), "toolib.util.ProcessLock_%s.lock" % name)
			self.__mutex = None
			self.__asquired = False
			if acquire:
				self.acquire()

		def acquire(self, timeout=-1):
			if not self.__asquired:
				while True:
					if os.path.exists(self.__path):
						#rint "exists"
						pid = open(self.__path, 'rt').read().strip()
						#rint "pid", pid

						running = False
						for line in os.popen("ps xa"):
							if line.split(None, 1)[0] == pid:
								running = True
								break
                        
						#rint "running", running
						if running:
							if timeout == -1:
								time.sleep(self.__sleep / 1000.)
							elif timeout == 0:
								t = min(timeout, self.__sleep)
								timeout -= t
								time.sleep(t / 1000.)
							else:
								raise LockAsquireTimeout()
						else:
							break
					else:
						break
							
				open(self.__path, 'wt').write(str(os.getpid()))
				self.__asquired = True

		def __nonzero__(self):
			return self.__asquired
						
		def release(self):
			if self.__asquired:
				if os.path.exists(self.__path):
					os.remove(self.__path)				
				self.__asquired = False



if __name__ == '__main__':
	import time

	print "locking..."
	l = ProcessLock('bebe', True)
	print "locked"
	time.sleep(10)
	print "unlocked"
	l.release()
	time.sleep(10)
	print "exit"
