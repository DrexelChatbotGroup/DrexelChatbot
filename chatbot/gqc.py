from postag import NLTKPOSTag
import questionconstruction

class GenericQuestionConstruction():
	def __init__(self, question, db):
		self.question = question
		self.db = db
		self.tag_list = []

	def getgenericquestion(self):
		self.tag_list = getpostag(self.question)
		rep_list = findrepresentation()
		#replace nouns with their genericRepresentations
		paddedquestion = self.question
		for key, value in rep_list.items():
			paddedquestion.replace(key, value)
		#create returned object
		returnedobject = QuestionConstruction()
		returnedobject.paddedquestion = paddedquestion
		returnedobject.rep_list = rep_list
		return returnedobject

	def findrepresentation():
		#retrieve all nouns
		noun_list = []
                for tup in self.tag_list:
                        if tup[1][0].lower() is 'n':
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
