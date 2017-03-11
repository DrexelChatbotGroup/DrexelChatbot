import re
from errors import BadQuestionException
from errors import BadAnswerException

class GenericAnswerPopulation:
    def __init__(self, _genericAnswer, db):
        self.genericAnswer = _genericAnswer.getAnswer()
        self.query = _genericAnswer.getQuery()
        self.db = db;

    def populate(self, gqc_dictionary):
        self.__populateQuery(gqc_dictionary)
        ans_dictionary = self.__queryDatabase()
        combinedDictionary = self.__combineDictionary(gqc_dictionary, ans_dictionary)
        answer = self.__populateFromDictionary(combinedDictionary)
        return answer

    def __queryDatabase(self):
        ans_dictionary = self.db.query(self.query)
        return ans_dictionary


    def __combineDictionary(self, dictionary1, dictionary2):
        combinedDictionary = dictionary1.copy()
        combinedDictionary.update(dictionary2)
        return combinedDictionary


    def __populateFromDictionary(self, dictionary):
        rep_list = self.__getWordsInsideParenthesis(self.genericAnswer)
        genericAnswer = self.genericAnswer
        for rep in rep_list:
                if not(rep in dictionary):
                    print("[Error!!! when populating final answer]")
                    raise BadAnswerException()
                genericAnswer = genericAnswer.replace("(" + rep + ")", dictionary[rep])

        print("[final answer populated] " +  genericAnswer)
        return genericAnswer

    def __getWordsStartingWithDollar(self, sentence):
        return [ t for t in sentence.split() if t.startswith('$') ]

    def __getWordsInsideParenthesis(self, sentence):
        return re.findall(r'\((.*?)\)',sentence)

    def __populateQuery(self, dictionary):
        var_list = self.__getWordsInsideParenthesis(self.query)
        for key in var_list:
            if not (key in dictionary):
                print("[Error!!! when constructing query from generic query]")
                raise BadQuestionException()
            self.query = self.query.replace("(" + key + ")", dictionary[key]);
        print("[query populated] " + self.query)
