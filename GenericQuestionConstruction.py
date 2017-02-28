import NLTKPOSTag
import QuestionConstruction

class GenericQuestionConstruction():
	def __init__(self, question, db):
		self.question = question
		self.db = db
		self.tagList = []

	def getGenericQuestion(self):
		self.tagList = getPOSTag(self.question)
		repList = findRepresentation()
		#replace nouns with their genericRepresentations
		paddedQuestion = self.question
		for key, value in repList.items():
			paddedQuestion.replace(key, value)
		#create returned object
		returnedObject = QuestionConstruction()
		returnedObject.paddedQuestion = paddedQuestion
		returnedObject.repList = repList
		return returnedObject

	def findRepresentation():
		#retrieve all nouns
		nounList = []
                for tup in self.tagList:
                        if tup[1][0].lower() is 'n':
                                nounList.append(tup[0])
		repList = {}
		for noun in nounList:
			rep = ""
			#get genericRepresentation
			
			#store tuples
			repList[noun] = rep
		return repList
