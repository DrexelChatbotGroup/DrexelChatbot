import re
from chatbot.errors import BadQuestionException
from chatbot.errors import BadAnswerException
import sys
import logging
import time

class GenericAnswerPopulation:
    def __init__(self, _genericAnswer, db):
        self.genericAnswer = _genericAnswer.getAnswer()
        self.query = _genericAnswer.getQuery()
        self.db = db;

    def populate(self, gqc_dictionary):
        logging.debug("Running Generic Answer Population...")
        self.__populateQuery(gqc_dictionary)
        ans_dictionary = self.__queryDatabase(gqc_dictionary)
        combinedDictionary = self.__combineDictionary(gqc_dictionary, ans_dictionary)
        answer = self.__populateFromDictionary(combinedDictionary)
        return answer

    def __queryDatabase(self, dictionary):
        if(self.query == "null"):
            logging.debug("query was null")
            raise BadAnswerException(self.db, dictionary)
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
                    raise BadAnswerException(self.db, dictionary)
                #if the answer is a picture, just return the picture
                if rep == "picture":
                    return '<img src="' + dictionary[rep] + 'height="250">'
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

        dayDictionary = {'Sunday':'s', 'Monday':'m', 'Tuesday':'t', 'Wednesday':'w', 'Thursday':'th', 'Friday':'f',
                         'Saturday':'sa', 'Sunday':'su'}

        #checking if no day was provided
        #if no day if provided current day should be used
        if("?startTime" in self.query and 'Day' not in dictionary):
            dictionary['Day'] = time.strftime("%a")
            self.genericAnswer = self.genericAnswer.replace("on (Day)", "today")

        #checking for days in the dictionary and replacing the query
        if('Day' in dictionary):
            day = dayDictionary[dictionary['Day']]
            startTimeReplacement = day+'StartTime'
            endTimeReplacement = day+'EndTime'
            self.query = self.query.replace("startTime", startTimeReplacement)
            self.query = self.query.replace("endTime", endTimeReplacement)
            self.genericAnswer = self.genericAnswer.replace("startTime", startTimeReplacement)
            self.genericAnswer = self.genericAnswer.replace("endTime", endTimeReplacement)

        for key in var_list:
            if not (key in dictionary):
                logging.warning("Error!!! when constructing query from generic query")
                raise BadAnswerException(self.db, dictionary)
            self.query = self.query.replace("(" + key + ")", dictionary[key]);
        logging.debug("query populated: " + self.query)
