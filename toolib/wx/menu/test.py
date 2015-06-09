import wx

from toolib.wx.TestApp	import TestApp
from MenuResources		import MenuResources
from Menu				import Menu
from MenuBar			import MenuBar

from toolib.wx.Resources import Resources 


def test():

	g = None

	def oninit(self):
		config = {
			'items' : [
				{
					'text'	: 'File',
					'items' : [
						{						# dict is equal to 'aaa'
							'id'	: 'aaa',
						},
						'bbb',
						{
							'id'	:		'newSubmenu',
							'text'	: 		'New fucking submenu',
							'items'	: [
								'xxx',
								'yyy',
								'zzz',
							],
						},
						'oldSubmenu',
					],
				},
			],
		}

		actionConf = {
			'aaa' : {
				'text'		: 'A',
			},
			'bbb' : {
				'text'		: 'B',
			},
			'newSubmenu' : {
				'text'		: 'Submenu',
			},
			'oldSubmenu' : {
				'text'		: 'Old submenu',
				'submenu'	: {
					'items' : [
						'ddd',
						'eee',
						'fff',
					],
				}
			}

		}

		resources = MenuResources(Resources(r"Z:\projects\lider\res\images"), actionConf)
		self.SetMenuBar(MenuBar(resources, config))
		wx.TextCtrl(self, -1)

	def ondestroy(self):
		pass

	TestApp(oninit, ondestroy).MainLoop()

if __name__ == '__main__':
	test()