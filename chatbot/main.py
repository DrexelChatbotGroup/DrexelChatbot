from chatbot.errors import ErrorHandler
from chatbot.errors import ChatbotException 
import chatbot.gqc
import chatbot.gac
import chatbot.gap
from database.stardog import StardogDB

def main():
	try :
		#need to get question from website
		question = "test"
		db = StardogDB("chatbotDB")
		config = "genericAnswers.txt"
		answer = None

		gqc_object = gqc.GenericQuestionConstruction(question, db)
		genericquestion = gqc_object.getgenericquestion()

		gac_object = gac.GenericAnswerConstruction(config, answer)
		genericanswer = gac_object.generateGenericAnswer(genericquestion.paddedquestion)

		#expected genericAnswer is different from one being created
		gap_object = gap.GenericAnswerPopulation(genericAnswer, db)
		answer = gap_object.populate()

	except ChatbotException as ex:
		ErrorHandler.handle(ex)

if __name__ == "__main__":
	main()
