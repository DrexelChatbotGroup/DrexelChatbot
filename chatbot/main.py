from chatbot.errors import ErrorHandler
from chatbot.errors import ChatbotException 
import chatbot.gqc as gqc
import chatbot.liveGac as gac
import chatbot.gap as gap
from database import stardog
import sys
import logging
import time

def _main(question):
    try :
        db = stardog.StardogDB("chatbotDB")
        answer = "/home/DrexelChatbot/chatbot/genericAnswers.csv"
        config = "/home/DrexelChatbot/chatbot/trained_model.m5"
        logfile = "/home/DrexelChatbot/chatbot/chatbot.log"
        
        logging.basicConfig(filename=logfile, level=logging.INFO)
        logging.info('New call at: ' + time.strftime("%c"))
        logging.info('Recieved input question: ' + question)

        gqc_object = gqc.GenericQuestionConstruction(question, db)
        genericquestion = gqc_object.getgenericquestion()
        logging.info('Generic question: ' + genericquestion.paddedquestion)

        gac_object = gac.GenericAnswerConstruction(config, answer)
        genericanswer = gac_object.generateGenericAnswer(genericquestion.paddedquestion)
        logging.info('Generic answer: ' + genericanswer.getAnswer())
        logging.info('Generic query: ' + genericanswer.getQuery())

        gap_object = gap.GenericAnswerPopulation(genericanswer, db)
        answer = gap_object.populate(genericquestion.rep_list)
        logging.info('Final answer: ' + answer)
        
        print(answer)
    
    except ChatbotException as ex:
        logging.debug("Encountered excption of type " + str(type(ex)))
        ErrorHandler.handle(ex)

    except Exception as ex:
        print('Our system encountered some error. Hope our future bosses will not see this.')
        logging.error(ex)
    
    logging.info("End: " + time.strftime("%c") + "\n\n")

if __name__ == "__main__":
    _main(sys.argv[1])
