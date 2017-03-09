from errors import ErrorHandler
from errors import ChatbotException 
import gqc
import gac
import gap
import sys

def _main(question):
    try :
        question = question
        db = None;
        config = None
        answer = None

        c = gqc.GenericQuestionConstruction(question, db)
        genericQuestion = c.getGenericQuestion()
        print(genericQuestion)

        c = gac.GenericAnswerConstruction(genericQuestion, config, answer)
        genericAnswer = c.generateGenericAnswer()
        print(genericAnswer)

        c = gap.GenericAnswerPopulation(genericAnswer, db)
        answer = c.populate()
        print(answer)

    except ChatbotException as ex:
        ErrorHandler.handle(ex)

if __name__ == "__main__":
    _main(sys.argv[1])
