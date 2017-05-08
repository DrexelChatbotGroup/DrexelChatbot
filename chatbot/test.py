from errors import *
import sys

try:
    db = ''
    dictionary = {'target':'test'}
    raise BadAnswerException(db, dictionary)
except ChatbotException as ex:
    ErrorHandler.handle(ex)
