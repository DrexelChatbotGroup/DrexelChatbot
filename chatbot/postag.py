import abc

class POSTag(object, metaclass = abc.ABCMeta):
	@abc.abstractmethod
	def getpostag(self, question):
		raise NotImplementedError('getPOSTag() method not implemented')

class NLTKPOSTag(POSTag):
	import nltk
	def getpostag(self, question):
		tokens = word_tokenize(question)
		tagged = pos_tag(tokens)
		return tagged
