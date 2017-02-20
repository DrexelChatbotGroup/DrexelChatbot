import POSTagInterface
import nltk

class NLTKPOSTag(POSTag):
	def getPOSTag(self, question):
		tokens = word_tokenize(question)
		tagged = pos_tag(tokens)
		return tagged
