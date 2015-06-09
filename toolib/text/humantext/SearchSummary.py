import re
import operator


class Counter(object):

	def __init__(self):
		self.count = 0

	def inc(self):
		self.count += 1

	def get(self):
		return self.count


class SearchSummary(object):
	"""
	provide lowercase regexp


	[-------------x---------------]
	[--------x----------x----------]
	[----x--------x-------x-------]

	"""

	def __init__(self, pattern, match_template, length):
		self._pattern = re.compile(pattern)
		self._match_template = match_template
		self._length = length


	def format(self, text):

		count = Counter()
		matches = []

		def f(m):
			count.inc()
			matches.append(m)
			return ''

		self._pattern.sub(f, text.lower())

		if matches:
			distances = [matches[i+1].start() - matches[i].end() for i in xrange(len(matches)-1)]

			try:
				offset, number, extra_length = find_max_chain(distances, self._length)
				#rint offset, number, extra_length, '!!!!!!!!!!!!'
				matches = matches[offset:offset+number+1]
			except ValueError:	# no chain found
				matches = [matches[0]]
				extra_length = self._length


			pos = 0
			html = []

			for m in matches:
				html.append(text[pos:m.start()])
				html.append(self._match_template % text[m.start():m.end()])
				pos = m.end()

			html.append(text[matches[-1].end():])

			# |-----------------------------------------|                    |------| #
			
			
			a = len(html[0])
			b = len(html[-1])

			if a + b > 0:

				#rint a, b, extra_length

				html[0]  = ltrim_on_word(html[0],  max(0,   a-1-extra_length*a/(a+b)))
				html[-1] = rtrim_on_word(html[-1], min(b-1, extra_length*b/(a+b)))

			return u''.join(html), count.get()

		else:
			return u'', 0


def find_max_chain(distances, max_distance):
	"""
	returns (offset, size) of chain of distances having maximum
	"""
	#rint "--------------------------"
	#rint distances, max_distance
	#rint "--------------------------"

	for c in xrange(len(distances)-1, -1, -1):

		count = c+1 
		
		# leave distances for begining and for ending
		max_inner_distance = int(float(max_distance) / (count + 2) * count)

		chains = [reduce(operator.add, distances[i:i+c], distances[i+c]) for i in xrange(len(distances)-c)]

		m = min(chains)

		#rint c, chains, m

		if m <= max_inner_distance:
			return chains.index(m), count, max_distance

	raise ValueError, 'no chain found'


REC_LETTER = re.compile(r'(?iu)\w')
	
def ltrim_on_word(s, pos):

	if s:
		if REC_LETTER.match(s[pos]):

			#rint 1
			while True:
				pos -= 1
				#rint s[pos]
				if pos < 0 or not REC_LETTER.match(s[pos]):
					break

			if pos > 0:
				return u'... ' + s[pos+1:]
			else:
				return s
	
		else:
		
			#rint 2
			while True:
				pos += 1
				#rint s[pos]
				if pos >= len(s) or REC_LETTER.match(s[pos]):
					break

			return u'... ' + s[pos:]
	else:
		return s

def rtrim_on_word(s, pos):

	if s:
		if REC_LETTER.match(s[pos]):

			#rint 1
			while True:
				pos += 1
				#rint s[pos]
				if pos >= len(s) or not REC_LETTER.match(s[pos]):
					break

			if pos > 0:
				return s[:pos] + u' ...'
			else:
				return s
	
		else:
		
			#rint 2
			while pos >= 0:
				pos -= 1
				#rint s[pos]
				if pos < 0 or REC_LETTER.match(s[pos]):
					break

			return s[:pos+1] + u' ...'
	else:
		return s

if __name__ == '__main__':
	d = [5,4,3,2,1,2,3,4,5,6]
	#rint d

	#rint find_max_chain(d, 0)



	print '"' + ltrim_on_word(u"hello                     world            ", len(u"hello                     world        ")-1) + '"'

