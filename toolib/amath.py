#################################################################
# Program:   common
"""
	Math utils
"""
__author__  = "All"
__date__	= "$Date: 2003/11/18 13:01:58 $"
__version__ = "$Revision: 1.2 $"
# $Source: D:/HOME/cvs/toolib/amath.py,v $
#																#
#################################################################
import types

def matrixFlip(a):
	n = len(a)
	if n==0: return a;
	m = len(a[0])
	res = range(m)
	for i in xrange(m):
		row = range(n)
		res[i] = row
		for j in xrange(n):
			row[j] = a[j][i]
	return res

def matrixSlice(a, rowStart, rowStop, colStart, colStop):
	rowslice = list(a[rowStart:rowStop])
	for i in xrange(len(rowslice)):
		rowslice[i] = rowslice[i][colStart:colStop]
	return rowslice

def matrixList(a):
	if type(a) is not types.ListType:
		a = list(a)
	for i in xrange(len(a)):
		if type(a[i]) is not types.ListType:
			a[i] = list(a[i])
	return a

def matrixDump(m, out=None):
	if out is None:
		import sys
		out = sys.stdout
	width = len(m[0])
	out.write('		  |')
	for i in xrange(width):
		out.write(' %6s' % i)
	out.write('\n %s\n' % ('-' * (width+1) * 7))
	for i in xrange(len(m)):
		out.write('%6s |' % i)
		for elt in m[i]:
			out.write(' %6s' % (elt,))
		out.write('\n')

def pointsRect(pointList):
	"""
	returns rectangle: (minx, miny...), (maxx, maxy...),
	for set of points
	"""
	def min(minPoint, point):
		res = list(minPoint)
		for i in range(len(res)):
			if res[i] > point[i]: res[i] = point[i]
		return res
	def max(maxPoint, point):
		res = list(maxPoint)
		for i in range(len(res)):
			if res[i] < point[i]: res[i] = point[i]
		return res
	minPoint = reduce(min, pointList)
	maxPoint = reduce(max, pointList)
	return minPoint, maxPoint

################ END OF MODULE ################

if __name__ == '__main__':
	a = [
		(1,2),
		(3,4),
		(5,6),
		(1,7),
		(0,8),
	]
	(a,b),(c,d) = pointsRect(a)
	print a,b,c,d



