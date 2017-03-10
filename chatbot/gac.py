max_question_length = 100
top_words = 5000
filt = '.?"\/!,<>@#$%^&*_-+=|}{][:;~`'
embedding_vector_length = 64
#Note: It is very important that the above values be set in the same way for
#      both this script and the gac class file.

from keras.preprocessing import text
from keras.preprocessing import sequence
from keras import models

class GenericAnswerConstruction:
        def __init__(self, configFile, answerFile):
                self.net = models.load_model(configFile)
                self.genericAnswers = loadAnswers(answerFile)

        def generateGenericAnswer(self, genericQuestion):
                encodedText = [text.one_hot(genericQuestion.replace("'", " "), top_words, filters=filt)]
                encodedText = sequence.pad_sequences(encodedText, maxlen=max_question_length)

                answerNumber = getMax(self.net.predict(encodedText)[1])

                return self.genericAnswers[answerNumber]
                
        def getMax(L):
                m = L[0]
                ret = 0
                for i in range(len(L)):
                        if L[i] > m:
                                m = L[i]
                                ret = i
                return ret

        def loadAnswers(fname):
                f = open(fname)
                d = {}
                i = 0
                for line in f:
                        fields = line.split(',')
                        d[i] = GenericAnswer(fields[0], fields[1])
                        i += 1
                f.close()
                return d
        
class GenericAnswer:
        def __init__(self, newAnswer, newQuery):
                self.answer = newAnswer
                self.query = newQuery

        def getAnswer(self):
                return self.answer

        def getQuery(self):
                return self.query

if __name__ == "__main__":
        classifier = GenericAnswerConstruction("trained_model.m5", "genericAnswers.txt")
        print(str(classifier.generateGenericAnswer("Where is (Person)'s office?")))
