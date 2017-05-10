import re
from errors import BadQuestionException
from errors import BadAnswerException
import sys
import logging

class GenericAnswerPopulation:
    def __init__(self, _genericAnswer, db):
        self.genericAnswer = _genericAnswer.getAnswer()
        self.query = _genericAnswer.getQuery()
        self.db = db;

    def populate(self, gqc_dictionary):
        logging.debug("Running Generic Answer Population...")
        self.__populateQuery(gqc_dictionary)
        ans_dictionary = self.__queryDatabase()
        combinedDictionary = self.__combineDictionary(gqc_dictionary, ans_dictionary)
        answer = self.__populateFromDictionary(combinedDictionary)
        return answer

    def __queryDatabase(self):
        ans_dictionary = self.db.query(self.query)
        logging.debug("queried answer dictionary: " + str(ans_dictionary))
        if(len(ans_dictionary) == 0):
            logging.warning("Error!!! The database query returned empty dictionary")
            logging.warning("The query was:\n" +  self.query);
            pass
        return ans_dictionary


    def __combineDictionary(self, dictionary1, dictionary2):
        combinedDictionary = dictionary1.copy()
        combinedDictionary.update(dictionary2)
        logging.debug("combined dictionary: " + str(combinedDictionary))
        return combinedDictionary


    def __populateFromDictionary(self, dictionary):
        rep_list = self.__getWordsInsideParenthesis(self.genericAnswer)
        logging.debug("rep_list: " + str(rep_list))
        genericAnswer = self.genericAnswer
        for rep in rep_list:
                if not(rep in dictionary):
                    logging.warning("Error!!! when populating final answer")
                    raise BadAnswerException(db, dictionary)
                genericAnswer = genericAnswer.replace("(" + rep + ")", dictionary[rep])

        return genericAnswer

    def __getWordsStartingWithDollar(self, sentence):
        return [ t for t in sentence.split() if t.startswith('$') ]

    def __getWordsInsideParenthesis(self, sentence):
        return re.findall(r'\((.*?)\)',sentence)

    def __populateQuery(self, dictionary):
        logging.debug("question dictionary: " + str(dictionary))
        var_list = self.__getWordsInsideParenthesis(self.query)
        logging.debug("var_list: " + str(var_list))
        for key in var_list:
            if not (key in dictionary):
                logging.warning("Error!!! when constructing query from generic query")
                raise BadQuestionException()
            self.query = self.query.replace("(" + key + ")", dictionary[key]);
        logging.debug("query populated: " + self.query)
