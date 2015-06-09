from random import randint


def getRandomString(n, chars):
	randintArgs = 0, len(chars)-1
	return ''.join(
		(
			chars[randint(*randintArgs)]
			for i in xrange(n)
		)
	)

if __name__ == '__main__':
	chars= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
	
	print len(chars) ** 8
	print getRandomString(8, chars)
