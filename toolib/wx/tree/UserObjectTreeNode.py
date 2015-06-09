from TreeNode import TreeNode



class UserObjectTreeNode(TreeNode):
	def __init__(self, userObject=None, childCount=-1):
		TreeNode.__init__(self, childCount)
		self.__userObject = userObject

	def getUserObject(self):
		return self.__userObject

	def setUserObject(self, userObject):
		self.__userObject = userObject
		self.fireTextChanged()

	def getText(self):
		return str(self.__userObject)

	def getId(self):
		""" passes id from user object """
		return self.__userObject.getId()
