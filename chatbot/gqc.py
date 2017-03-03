from postag import NLTKPOSTag
from  genericquestion import GenericQuestion

class GenericQuestionConstruction():
	def __init__(self, question, db):
		self.question = question
		self.db = db
		self.tag_list = []

	def getgenericquestion(self):
		postag_class = NLTKPOSTag()
		self.tag_list = postag_class.getpostag(self.question)
		rep_list = self.findrepresentation()
		#replace nouns with their genericRepresentations
		paddedquestion = self.question
		for key, value in rep_list.items():
			paddedquestion = paddedquestion.replace(key, value)
		#create returned object
		returnedobject = GenericQuestion()
		returnedobject.paddedquestion = paddedquestion
		returnedobject.rep_list = rep_list
		return returnedobject

	def findrepresentation(self):
		#retrieve all nouns
		noun_list = []
		for tup in self.tag_list:
			if tup[1][0].lower() == 'n':
				noun_list.append(tup[0])
		rep_list = {}
		for noun in noun_list:
			rep = ""
			#get genericRepresentation
			
			#temporary code
			rep = "**Test**"

			#store tuples
			rep_list[noun] = rep
		return rep_list
