from chatbot.errors import ErrorHandler
from chatbot.errors import ChatbotException 
import chatbot.gqc
import chatbot.gac
import chatbot.gap
from database.stardog import StardogDB

def _main(question):
    try :
        db = StardogDB("chatbotDB")
        answer = "genericAnswers.txt"
        config = "trained_model.m5"

        gqc_object = gqc.GenericQuestionConstruction(question, db)
        genericquestion = gqc_object.getgenericquestion()

        gac_object = gac.GenericAnswerConstruction(config, answer)
        genericanswer = gac_object.generateGenericAnswer(genericquestion.paddedquestion)

        gap_object = gap.GenericAnswerPopulation(genericanswer, db)
        answer = gap_object.populate(genericquestion.rep_list)
        
        print(answer)
    
    except ChatbotException as ex:
        ErrorHandler.handle(ex)

if __name__ == "__main__":
    _main(sys.argv[1])
