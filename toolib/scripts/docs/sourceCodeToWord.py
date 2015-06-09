# -*- coding: Cp1251 -*-
import os
import win32com.client
const = win32com.client.constants
import re

tests = (
	re.compile(r"""def\s+test\s*\("""), 
	re.compile(r"""if __name__ == ["']__main__["']:""".replace(' ', r'\s*')),
)

def sourceCodeToWord(rootPath, skipPackages=(), skipFiles=()):

	skipFiles = [os.path.join(rootPath, f) for f in skipFiles]

	word = win32com.client.DispatchEx("Word.Application")
	word.Visible = True

	word.Documents.Add(DocumentType=const.wdNewBlankDocument)

	Styles = word.ActiveDocument.Styles
	Selection = word.Selection
	Font = Selection.Font

	def printText(text):
		Selection.TypeText(Text=text+"\n")

	def printHeader(n, text):
		Selection.Style = Styles("Заголовок %s" % n)
		Selection.TypeText(Text=text+"\n")
		Selection.Style = Styles("Обычный")

	def printSourceFile(path):

		f = open(path, 'rt')
		source = f.read()
		f.close()

		for rec in tests:
			m = rec.search(source)
			if m:
				print m
				source = source[:m.start()]
				break

		source = source.replace('\t', '    ')

		if source.strip():

			Selection.Font.Bold = const.wdToggle
			printText('\nФайл: %s\n' % os.path.split(path)[-1])
			Selection.Font.Bold = const.wdToggle

			stored = Font.Name, Font.Size
			Font.Name, Font.Size = "Courier New", 8

			Selection.TypeText(Text=source)
			Selection.TypeText(Text='\n')

			Font.Name, Font.Size = stored

	def printPackage(dir, name=None, depth=0):

		if name is None:
			name = os.path.split(dir)[-1]

		printHeader(depth+2, 'Пакет: %s' % name)

		for file in os.listdir(dir):
			path = os.path.join(dir, file)
			if os.path.isdir(path):
				if os.path.exists(os.path.join(path, '__init__.py')):
					# this is subpackage
					package = '.'.join((name, file))
					if package not in skipPackages:
						printPackage(path, package, depth+1)
			
			elif file.endswith('.py') and not path in skipFiles:
				printSourceFile(path)


	printHeader(1, 'Вихідні коди')
	printPackage(rootPath)


if __name__ == '__main__':
	sourceCodeToWord(
		'z:\\projects\\lider\\src\\lider',
		(
			'lider.test',
			'lider.config.demo',
			'lider.config.mysql',
			'lider.config.inline',
			'lider.config.train',
		),
		(
			'MainFrame_inline.py'
			'MainFrame_mysql.py'
			'MainFrame_train.py'
		),
	)
