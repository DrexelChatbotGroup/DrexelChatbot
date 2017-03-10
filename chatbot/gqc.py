from postag import NLTKPOSTag
from genericquestion import GenericQuestion
from errors import BadQuestionException

class GenericQuestionConstruction():
	def __init__(self, question, db):
		self.question = question
		self.db = db
		self.tag_list = []

	def getgenericquestion(self):
		postag_class = NLTKPOSTag()
		self.tag_list = postag_class.getpostag(self.question)
		rep_list = self.findrepresentation()

		if len(rep_list) == 0:
			raise BadQuestionException()
		#replace nouns with their genericRepresentations
		paddedquestion = self.question
		for key, value in rep_list.items():
			paddedquestion = paddedquestion.replace(value, key)
		#create returned object which contains a string and a dictionary 
		#whose keys are nouns in original question and values are generic 
		#representations of the keys
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
			#get a dictionary from from database whose keys are 
			#'property' and values are generic representation
			query_string = """
			prefix cb: <http://drexelchatbot.com/rdf/>

			SELECT ?property
			WHERE
			{
				?s cb:name \"%s\" " .
				?s cb:property ?property .
			}
			""" % noun

			rep = self.db.query(query_string)

			#for testing purpose
			#rep = "**test**"

			#store tuples
			if not rep:
				rep_list[rep['property']] = noun
		return rep_list
