import wx


class XIterItems(object):

	def iterRootItems(self):
		item = self.GetRootItem()
		while item:
			yield item
			item = self.GetNextSibling(item)


	def iterItemsRecursive(self, parentItem=None, stopFn=lambda item: False, includeSelf=True):

		skipParents = False

		if parentItem is None:
			parentItems = self.iterRootItems()
			skipParents = self.GetWindowStyle() & wx.TR_HIDE_ROOT
		else:
			parentItems = (parentItem,)
		
		for parentItem in parentItems:
			
			if not skipParents and includeSelf:
				yield parentItem

			if skipParents or not includeSelf or not stopFn(parentItem):

				item, cookie = self.GetFirstChild(parentItem)
				while item:
					yield item
					if not stopFn(item):
						for i in self.iterItemsRecursive(item, stopFn, includeSelf=False):
							yield i
					item = self.GetNextSibling(item)


		