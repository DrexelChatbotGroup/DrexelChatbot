import NLTKPOSTag
import QuestionConstruction

class GenericQuestionConstruction():
	def __init__(self, question, db):
		self.question = question
		self.db = db
		self.tagList = []

	def getGenericQuestion(self):
		self.tagList = getPOSTag(self.question)
		nounList = []
		for tup in self.tagList:
			if tup[1][0].lower() is 'n':
				nounList.append(tup)
		repList = findRepresentation()
		paddedQuestion = self.question
		for key, value in repList.items():
			paddedQuestion.replace(key, value)
		returnedObject = QuestionConstruction()
		returnedObject.paddedQuestion = paddedQuestion
		returnedObject.repList = repList
		return returnedObject

	def findRepresentation():

