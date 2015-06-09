#################################################################
# Program:   toolib
"""
	Pumps stream to another
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2005/08/03 12:24:18 $"
__version__ = "$Revision: 1.1 $"
# $Source: D:/HOME/cvs/toolib/util/Pump.py,v $
#																#
#################################################################
#import sys

__all__ = ["Pump", "stream2stream", "stream2file", "file2stream"]

class Pump:
	def __init__(self, buf_size=1024*8):
		self._buf_size = buf_size

	def stream2stream(self, ins, outs):
		while 1:
			buf = ins.read(self._buf_size)
			if not buf:
				break
			outs.write(buf)

	def stream2file(self, ins, filename, filemode="t"):
		f = file(filename, "w"+filemode)
		try:
			self.stream2stream(ins, f)
		finally:
			f.close()

	def file2stream(self, filename, outs, filemode="t"):
		f = file(filename, "r"+filemode)
		try:
			self.stream2stream(f, outs)
		finally:
			f.close()

	#def stream2stdout(self, ins):
	#	self.sreamToStream(ins, sys.stdout)
		
	#def stream2stderr(self, ins):
	#	self.sreamToStream(ins, sys.stderr)

	#def stdin2stream(self, outs):
	#	self.sreamToStream(sys.stdin, outs)


# create default instance and expose functions
instance = Pump()

stream2stream = instance.stream2stream
stream2file = instance.stream2file
file2stream = instance.file2stream
