import re

class GenericAnswerPopulation:
    def __init__(self, _genericAnswer, db):
        self.genericAnswer = _genericAnswer["answer"]
        self.dictionary1 = _genericAnswer["dictionary1"]
        self.query = _genericAnswer["query"]
        self.dictionary2 = _genericAnswer["dictionary2"]
        self.db = db;

    def populate(self):
        query = self.__populateQuery(self.query, self.dictionary1)
        dictionary2 = self.__queryDatabase(query)
        combinedDictionary = self.__combineDictionary(self.dictionary1, dictionary2)
        answer = self.__populateFromDictionary(self.genericAnswer, combinedDictionary)
        return answer

    def __queryDatabase(self, query):
        #some database magic here
        #db.query(query)
        #return result as dictionary
        return self.dictionary2


    def __combineDictionary(self, dictionary1, dictionary2):
        combinedDictionary = self.dictionary1.copy()
        combinedDictionary.update(dictionary2)
        return combinedDictionary


    def __populateFromDictionary(self, genericAnswer, dictionary):
        ans = self.__getWordsInsideParenthesis(genericAnswer)
        length = len(ans);
        for i in range(0,length):
            key = ans[i]
            genericAnswer = genericAnswer.replace("(" + ans[i] + ")", dictionary[key])
        print("[final answer populated] " +  genericAnswer)
        return genericAnswer

    def __getWordsStartingWithDollar(self, sentence):
        return [ t for t in sentence.split() if t.startswith('$') ]

    def __getWordsInsideParenthesis(self, sentence):
        return re.findall(r'\((.*?)\)',sentence)

    def __populateQuery(self, query, dictionary):
        ans = self.__getWordsInsideParenthesis(query)
        length = len(ans);
        for i in range(0,length):
            key = ans[i]
            query = query.replace("(" + ans[i] + ")", dictionary[key]);
        print("[query populated] " + query)
        return query
