#!/usr/bin/python2
#-*- coding: utf-8 -*-
""""""

import sys
import string
import re
import json
import operator
import argparse
from collections import defaultdict


class Words:
	"""This class handles the loading of stopword lists and the removal of stopwords, punctuation, or making sure the words in a string are found in a dictionary."""

	stopwords = set()
	dictionary = set()
	punctuation = r''
	def __init__(self, stopwordsfile = '', dictionaryfile = '', punctuationfile = ''):
		if stopwordsfile.strip() != '':
			try:
				self.stopwords = set([w.strip().lower() for w in open(filename, 'r')])
			except IOError as e:
				self.stopwords = set()
		if len(self.stopwords) <= 0:
			self.stopwords = set(['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear', 'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may', 'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor', 'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since', 'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet', 'you', 'your'])

		if dictionaryfile.strip() != '':
			try:
				self.dictionary = set([w.strip().lower() for w in open(dictionaryfile, 'r')])
			except IOError as  e:
				self.dictionary = set()
		if len(self.dictionary) <= 0:
			self.dictionary = set([])

		if punctuationfile.strip() != '':
			try:
				regex_punctuation_string = "|".join([w.strip() for w in open(punctuationfile, 'r').readlines()])
				self.punctuation = re.compile(regex_punctuation_string)
			except IOError as e:
				self.punctuation = r''
		if len(self.punctuation) <= 0:
			regex_punctuation_string = "!|\"|#|\$|%|&|'|\(|\)|\*|\+|,|-|\.|/|\\\|:|;|\<|\=|\>|\?|@|\[|\||\]|\^|_|`|{|\||}|~|¡|¿|—|–|…|�|”|“|‘|’|´|¯|•|→"
			self.punctuation = re.compile(regex_punctuation_string)
	
	def removeStopwords(self, words):
		"""removes stopwords from a string"""
		wordList = [w.strip() for w in words.split(' ')]
		rtnWords = []
		for word in wordList:
			if word.lower() not in self.stopwords:
				rtnWords.append(word)
		return " ".join(rtnWords)

	def removeStopwordsLine(self, wordLines):
		rtnLines = []
		for line in wordLines:
			rtnLines.append(self.removeStopwords(line))
		return rtnLines

	def removePunctuation(self, words):
		"""removes puntuation from a string"""
		return self.punctuation.sub(' ', words)

	def removePunctuationLine(self, wordLines):
		rtnLines = []
		for line in wordLines:
			rtnLines.append(self.removePunctuation(line))
		return rtnLines

	def removeNonDictionaryWords(self, words):
		wordList = [w.strip() for w in words.split(' ')]
		rtnWords = []
		for word in wordList:
			if word.lower() in self.dictionary:
				rtnWords.append(word)
		return " ".join(rtnWords)

	def removeNonDictionaryWordsLine(self, wordLines):
		rtnLines = []
		for line in wordLines:
			rtnLines.append(self.removeNonDictionaryWords(line))
		return rtnLines

	def removeNumbers(self, words):
		"""removes numbers from a string"""
		return re.sub(r'\d', '', words)

	def removeNumbersLine(self, wordLines):
		rtnLines = []
		for line in wordLines:
			rtnLines.append(self.removeNumbers(line))
		return rtnLines
		
##############################################################################################
# Following is a porter stemmer implementation that was freely available on the internet.
# I included this in this file to simplify the text_cleaner tool.
##############################################################################################
##################################### START ##################################################
"""Porter Stemming Algorithm
This is the Porter stemming algorithm, ported to Python from the
version coded up in ANSI C by the author. It may be be regarded
as canonical, in that it follows the algorithm presented in

Porter, 1980, An algorithm for suffix stripping, Program, Vol. 14,
no. 3, pp 130-137,

only differing from it at the points maked --DEPARTURE-- below.

See also http://www.tartarus.org/~martin/PorterStemmer

The algorithm as described in the paper could be exactly replicated
by adjusting the points of DEPARTURE, but this is barely necessary,
because (a) the points of DEPARTURE are definitely improvements, and
(b) no encoding of the Porter stemmer I have seen is anything like
as exact as this version, even with the points of DEPARTURE!

Vivake Gupta (v@nano.com)

Release 1: January 2001

Further adjustments by Santiago Bruno (bananabruno@gmail.com)
to allow word input not restricted to one word per line, leading
to:

release 2: July 2008
"""
class PorterStemmer:

	def __init__(self):
		"""The main part of the stemming algorithm starts here.
		b is a buffer holding a word to be stemmed. The letters are in b[k0],
		b[k0+1] ... ending at b[k]. In fact k0 = 0 in this demo program. k is
		readjusted downwards as the stemming progresses. Zero termination is
		not in fact used in the algorithm.

		Note that only lower case sequences are stemmed. Forcing to lower case
		should be done before stem(...) is called.
		"""

		self.b = ""  # buffer for word to be stemmed
		self.k = 0
		self.k0 = 0
		self.j = 0	 # j is a general offset into the string

	def cons(self, i):
		"""cons(i) is TRUE <=> b[i] is a consonant."""
		if self.b[i] == 'a' or self.b[i] == 'e' or self.b[i] == 'i' or self.b[i] == 'o' or self.b[i] == 'u':
			return 0
		if self.b[i] == 'y':
			if i == self.k0:
				return 1
			else:
				return (not self.cons(i - 1))
		return 1

	def m(self):
		"""m() measures the number of consonant sequences between k0 and j.
		if c is a consonant sequence and v a vowel sequence, and <..>
		indicates arbitrary presence,

		   <c><v>		gives 0
		   <c>vc<v>		gives 1
		   <c>vcvc<v>	gives 2
		   <c>vcvcvc<v> gives 3
		   ....
		"""
		n = 0
		i = self.k0
		while 1:
			if i > self.j:
				return n
			if not self.cons(i):
				break
			i = i + 1
		i = i + 1
		while 1:
			while 1:
				if i > self.j:
					return n
				if self.cons(i):
					break
				i = i + 1
			i = i + 1
			n = n + 1
			while 1:
				if i > self.j:
					return n
				if not self.cons(i):
					break
				i = i + 1
			i = i + 1

	def vowelinstem(self):
		"""vowelinstem() is TRUE <=> k0,...j contains a vowel"""
		for i in range(self.k0, self.j + 1):
			if not self.cons(i):
				return 1
		return 0

	def doublec(self, j):
		"""doublec(j) is TRUE <=> j,(j-1) contain a double consonant."""
		if j < (self.k0 + 1):
			return 0
		if (self.b[j] != self.b[j-1]):
			return 0
		return self.cons(j)

	def cvc(self, i):
		"""cvc(i) is TRUE <=> i-2,i-1,i has the form consonant - vowel - consonant
		and also if the second c is not w,x or y. this is used when trying to
		restore an e at the end of a short	e.g.

		   cav(e), lov(e), hop(e), crim(e), but
		   snow, box, tray.
		"""
		if i < (self.k0 + 2) or not self.cons(i) or self.cons(i-1) or not self.cons(i-2):
			return 0
		ch = self.b[i]
		if ch == 'w' or ch == 'x' or ch == 'y':
			return 0
		return 1

	def ends(self, s):
		"""ends(s) is TRUE <=> k0,...k ends with the string s."""
		length = len(s)
		if s[length - 1] != self.b[self.k]: # tiny speed-up
			return 0
		if length > (self.k - self.k0 + 1):
			return 0
		if self.b[self.k-length+1:self.k+1] != s:
			return 0
		self.j = self.k - length
		return 1

	def setto(self, s):
		"""setto(s) sets (j+1),...k to the characters in the string s, readjusting k."""
		length = len(s)
		self.b = self.b[:self.j+1] + s + self.b[self.j+length+1:]
		self.k = self.j + length

	def r(self, s):
		"""r(s) is used further down."""
		if self.m() > 0:
			self.setto(s)

	def step1ab(self):
		"""step1ab() gets rid of plurals and -ed or -ing. e.g.

		   caresses  ->  caress
		   ponies	 ->  poni
		   ties		 ->  ti
		   caress	 ->  caress
		   cats		 ->  cat

		   feed		 ->  feed
		   agreed	 ->  agree
		   disabled  ->  disable

		   matting	 ->  mat
		   mating	 ->  mate
		   meeting	 ->  meet
		   milling	 ->  mill
		   messing	 ->  mess

		   meetings  ->  meet
		"""
		if self.b[self.k] == 's':
			if self.ends("sses"):
				self.k = self.k - 2
			elif self.ends("ies"):
				self.setto("i")
			elif self.b[self.k - 1] != 's':
				self.k = self.k - 1
		if self.ends("eed"):
			if self.m() > 0:
				self.k = self.k - 1
		elif (self.ends("ed") or self.ends("ing")) and self.vowelinstem():
			self.k = self.j
			if self.ends("at"):   self.setto("ate")
			elif self.ends("bl"): self.setto("ble")
			elif self.ends("iz"): self.setto("ize")
			elif self.doublec(self.k):
				self.k = self.k - 1
				ch = self.b[self.k]
				if ch == 'l' or ch == 's' or ch == 'z':
					self.k = self.k + 1
			elif (self.m() == 1 and self.cvc(self.k)):
				self.setto("e")

	def step1c(self):
		"""step1c() turns terminal y to i when there is another vowel in the stem."""
		if (self.ends("y") and self.vowelinstem()):
			self.b = self.b[:self.k] + 'i' + self.b[self.k+1:]

	def step2(self):
		"""step2() maps double suffices to single ones.
		so -ization ( = -ize plus -ation) maps to -ize etc. note that the
		string before the suffix must give m() > 0.
		"""
		if self.b[self.k - 1] == 'a':
			if self.ends("ational"):   self.r("ate")
			elif self.ends("tional"):  self.r("tion")
		elif self.b[self.k - 1] == 'c':
			if self.ends("enci"):	   self.r("ence")
			elif self.ends("anci"):    self.r("ance")
		elif self.b[self.k - 1] == 'e':
			if self.ends("izer"):	   self.r("ize")
		elif self.b[self.k - 1] == 'l':
			if self.ends("bli"):	   self.r("ble") # --DEPARTURE--
			# To match the published algorithm, replace this phrase with
			#	if self.ends("abli"):	   self.r("able")
			elif self.ends("alli"):    self.r("al")
			elif self.ends("entli"):   self.r("ent")
			elif self.ends("eli"):	   self.r("e")
			elif self.ends("ousli"):   self.r("ous")
		elif self.b[self.k - 1] == 'o':
			if self.ends("ization"):   self.r("ize")
			elif self.ends("ation"):   self.r("ate")
			elif self.ends("ator"):    self.r("ate")
		elif self.b[self.k - 1] == 's':
			if self.ends("alism"):	   self.r("al")
			elif self.ends("iveness"): self.r("ive")
			elif self.ends("fulness"): self.r("ful")
			elif self.ends("ousness"): self.r("ous")
		elif self.b[self.k - 1] == 't':
			if self.ends("aliti"):	   self.r("al")
			elif self.ends("iviti"):   self.r("ive")
			elif self.ends("biliti"):  self.r("ble")
		elif self.b[self.k - 1] == 'g': # --DEPARTURE--
			if self.ends("logi"):	   self.r("log")
		# To match the published algorithm, delete this phrase

	def step3(self):
		"""step3() dels with -ic-, -full, -ness etc. similar strategy to step2."""
		if self.b[self.k] == 'e':
			if self.ends("icate"):	   self.r("ic")
			elif self.ends("ative"):   self.r("")
			elif self.ends("alize"):   self.r("al")
		elif self.b[self.k] == 'i':
			if self.ends("iciti"):	   self.r("ic")
		elif self.b[self.k] == 'l':
			if self.ends("ical"):	   self.r("ic")
			elif self.ends("ful"):	   self.r("")
		elif self.b[self.k] == 's':
			if self.ends("ness"):	   self.r("")

	def step4(self):
		"""step4() takes off -ant, -ence etc., in context <c>vcvc<v>."""
		if self.b[self.k - 1] == 'a':
			if self.ends("al"): pass
			else: return
		elif self.b[self.k - 1] == 'c':
			if self.ends("ance"): pass
			elif self.ends("ence"): pass
			else: return
		elif self.b[self.k - 1] == 'e':
			if self.ends("er"): pass
			else: return
		elif self.b[self.k - 1] == 'i':
			if self.ends("ic"): pass
			else: return
		elif self.b[self.k - 1] == 'l':
			if self.ends("able"): pass
			elif self.ends("ible"): pass
			else: return
		elif self.b[self.k - 1] == 'n':
			if self.ends("ant"): pass
			elif self.ends("ement"): pass
			elif self.ends("ment"): pass
			elif self.ends("ent"): pass
			else: return
		elif self.b[self.k - 1] == 'o':
			if self.ends("ion") and (self.b[self.j] == 's' or self.b[self.j] == 't'): pass
			elif self.ends("ou"): pass
			# takes care of -ous
			else: return
		elif self.b[self.k - 1] == 's':
			if self.ends("ism"): pass
			else: return
		elif self.b[self.k - 1] == 't':
			if self.ends("ate"): pass
			elif self.ends("iti"): pass
			else: return
		elif self.b[self.k - 1] == 'u':
			if self.ends("ous"): pass
			else: return
		elif self.b[self.k - 1] == 'v':
			if self.ends("ive"): pass
			else: return
		elif self.b[self.k - 1] == 'z':
			if self.ends("ize"): pass
			else: return
		else:
			return
		if self.m() > 1:
			self.k = self.j

	def step5(self):
		"""step5() removes a final -e if m() > 1, and changes -ll to -l if
		m() > 1.
		"""
		self.j = self.k
		if self.b[self.k] == 'e':
			a = self.m()
			if a > 1 or (a == 1 and not self.cvc(self.k-1)):
				self.k = self.k - 1
		if self.b[self.k] == 'l' and self.doublec(self.k) and self.m() > 1:
			self.k = self.k -1

	def stemWords(self, words):
		rtnLines = []
		wordLine = [w.strip() for w in words.split(" ")]
		for word in wordLine:
			rtnLines.append(self.stemWord(word))
		return " ".join(rtnLines)

	def stemWord(self, word):
		return self.stem(word, 0, len(word)-1)

	def stem(self, p, i, j):
		"""In stem(p,i,j), p is a char pointer, and the string to be stemmed
		is from p[i] to p[j] inclusive. Typically i is zero and j is the
		offset to the last character of a string, (p[j+1] == '\0'). The
		stemmer adjusts the characters p[i] ... p[j] and returns the new
		end-point of the string, k. Stemming never increases word length, so
		i <= k <= j. To turn the stemmer into a module, declare 'stem' as
		extern, and delete the remainder of this file.
		"""
		# copy the parameters into statics
		self.b = p
		self.k = j
		self.k0 = i
		if self.k <= self.k0 + 1:
			return self.b # --DEPARTURE--

		# With this line, strings of length 1 or 2 don't go through the
		# stemming process, although no mention is made of this in the
		# published algorithm. Remove the line to match the published
		# algorithm.

		self.step1ab()
		self.step1c()
		self.step2()
		self.step3()
		self.step4()
		self.step5()
		return self.b[self.k0:self.k+1]
######################################### END ################################################
##############################################################################################

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog='./text_cleaner.py', description="Cleans* text files. \n*cleaning means lowercasing, removing punctuation and stopwords, stemming, counting, sorting, and removing words with a low occurrence.")
	parser.add_argument('-o', '--output-format', dest='output_format', help='specifies output format. Default is a space between words. Options are: space, tab, newline.', metavar='[space|tab|newline]', default='space')
	parser.add_argument('-L', '--line-mode', action='store_true', default=False, dest='line_mode', help='Output the words in line mode. Lines are preserved. Using this option nullifies the output format options specified.')
	parser.add_argument('-x', '--remove', dest='remove', default=[], nargs='+', help='removes one, many, or all of the following (whichever are specified): stopwords, punctuation, words, numbers. If "words" is specified for removal, then the --word-count or -w argument must also be given.', metavar='[stopwords,punctuation,words,numbers,blanklines]')
	parser.add_argument('--stopword-file', dest='stopword_file', default='', help="use the specified file for stopwords. If this option in used the '--remove=stopword' option is assumed.", metavar="FILE")
	parser.add_argument('--dict-file', dest='dict_file', default='', help="use the specified file for dictionary words. If this options is specified only words found in the dictionary will be used.", metavar="FILE")
	parser.add_argument('--punct-file', dest='punct_file', default='', help="use the specified file for punctuation. If this options is specified only words found in the dictionary will be used.", metavar="FILE")
	parser.add_argument('-l', '--lowercase', action='store_true', default=False, dest='lowercase', help='lowercase words.')
	parser.add_argument('-s', '--stem-words', action='store_true', default=False, dest='stem', help='stem the words (using a porter stemmer).')
	parser.add_argument("-i", "--input-file", dest="input_file", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file", metavar="FILE")

	args = parser.parse_args()

	contentList = (line.strip().lower() if args.lowercase else line.strip() for line in args.input_file)

	output = []

	delimiters = {'space':" ", 'tab':"\t", 'newline':"\n"}
	outputDelimiter = delimiters[args.output_format]

	cleaner = Words(args.stopword_file, args.dict_file, args.punct_file)
	stemmer = PorterStemmer()

	if args.line_mode:
		for line in contentList:
			if line.strip() == '' and 'blanklines' in args.remove: continue
			if 'numbers' in args.remove:
				line = cleaner.removeNumbers(line)

			if 'punctuation' in args.remove:
				line = cleaner.removePunctuation(line)

			if 'stopwords' in args.remove:
				line = cleaner.removeStopwords(line)

			if 'words' in args.remove:
				line = cleaner.removeNonDictionaryWords(line)

			if args.stem:
				line = stemmer.stemWords(line)

			output.append(line)

		sys.stdout.write("\n".join(output) + "\n")

	else: # word mode
		output = " ".join(contentList)
		if 'numbers' in args.remove:
			output = cleaner.removeNumbers(output)

		if 'punctuation' in args.remove:
			output = cleaner.removePunctuation(output)

		if 'stopwords' in args.remove:
			output = cleaner.removeStopwords(output)

		if 'words' in args.remove:
			output = cleaner.removeNonDictionaryWords(output)

		if args.stem:
			output = stemmer.stemWords(output)

		rtnOutput = []
		for word in output.split(" "):
			if word.strip() != '':
				rtnOutput.append(word.strip())

		output = " ".join(rtnOutput)
		sys.stdout.write(outputDelimiter.join(output.split(" ")))

