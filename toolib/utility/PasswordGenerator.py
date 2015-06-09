import random

lowercase = 'abcdefghijklmnopqrstuvwxyz'
uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letters = lowercase + uppercase
digits = '0123456789'
lettersAndDigits = letters + digits

class PasswordGenerator:

	def alphabet(self):
		return lettersAndDigits

	def genPassword(self, length):
		ab = self.alphabet()
		n = len(ab)-1
		p = range(length)
		for i in xrange(length):
			p[i] = ab[random.randint(0, n)]
		return ''.join(p)


if __name__ == '__main__':
	p = PasswordGenerator()
	for i in range(25):
		print p.genPassword(8)
