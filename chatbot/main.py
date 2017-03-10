from errors import ErrorHandler
from errors import ChatbotException 
import gqc
import gac
import gap
from database import stardog
import sys

def _main(question):
    try :
        db = stardog.StardogDB("chatbotDB")
        answer = "genericAnswers.txt"
        config = "trained_model.m5"

        gqc_object = gqc.GenericQuestionConstruction(question, db)
        genericquestion = gqc_object.getgenericquestion()
        print(genericquestion.paddedquestion)

        gac_object = gac.GenericAnswerConstruction(config, answer)
        genericanswer = gac_object.generateGenericAnswer(genericquestion.paddedquestion)
        print(genericanswer.getAnswer())

        gap_object = gap.GenericAnswerPopulation(genericanswer, db)
        answer = gap_object.populate(genericquestion.rep_list)
        
        print(answer)
    
    except ChatbotException as ex:
        ErrorHandler.handle(ex)

if __name__ == "__main__":
    _main(sys.argv[1])
