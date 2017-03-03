import abc
import nltk

class POSTag(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def getpostag(self, question):
		return

class NLTKPOSTag(POSTag):
	def getpostag(self, question):
		tokens = nltk.word_tokenize(question)
		tagged = nltk.pos_tag(tokens)
		return tagged
