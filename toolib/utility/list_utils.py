###############################################################################
# Program:   Sula 0.7
"""
	List utility module.
"""
__author__  = "Lesha Strashko"
__date__	= "$Date: 2008/03/20 19:03:25 $"
__version__ = "$Revision: 1.3 $"
__credits__ = "No credits today"
# $Source: D:/HOME/cvs/toolib/utility/list_utils.py,v $
###############################################################################

class ListUtility :
	def __init__(self) :
		pass

	def matrixToListOfDict(self, list, mapList) :
		'''
		Converts matrix : list[0..n] of list[0..m] to
		list of dict : list[0..n] of dict(m-keys, key names - in mapList)
		'''
		retList = []
		for i in range(len(list)) :
			rowDict = {}
			for j in range(len(mapList)) :
				rowDict[mapList[j]] = list[i][j]
			retList.append(rowDict)
		return retList

	def listOfDictToMatrix(self, list, mapList) :
		'''
		Converts list of dict : list[0..n] of dict(m-keys, key names - in mapList)
		to list[0..n] of list[0..M] according to map.
		'''
		retList = []
		for i in range(len(list)) :
			row = []
			for j in range(len(mapList)) :
				row.append(list[i][mapList[j]])
			retList.append(row)
		return retList

if __name__ == '__main__' :
	def test():
		conv = ListUtility()
		a = [[1,3,4,5 ],[3,5,5,6]]
		m = ['val', 'dict', 'fuck', 'off']
		liod = conv.matrixToListOfDict(a, m)
		print liod
		print conv.listOfDictToMatrix(liod, m)

	test()
