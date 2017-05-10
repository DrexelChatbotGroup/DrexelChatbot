max_question_length = 25
top_words = 5000
filt = '.?"\/!,<>@#$%^&*_-+=|}{][:;~`'
embedding_vector_length = 64
#Note: It is very important that the above values be set in the same way for
#      both this script and the gac class file.

import numpy
numpy.random.seed(0)

from zlib import adler32
from keras.preprocessing import sequence
from keras import models

class GenericAnswerConstruction:
    def __init__(self, configFile, answerFile):
        self.net = models.load_model(configFile)
        self.genericAnswers = self.loadAnswers(answerFile)

    def generateGenericAnswer(self, genericQuestion):
        encodedText = [self.my_hash(genericQuestion)]
        encodedText = sequence.pad_sequences(encodedText, maxlen=max_question_length)
        answerNumber = self.net.predict_classes(encodedText, verbose=0)[0]

        return self.genericAnswers[answerNumber]
            
    def my_hash(self, item):
        to_hash = item.replace("'", " ")
        for c in filt:
            to_hash = to_hash.replace(c, "")

        final = []
        words = to_hash.lower().split(" ")
        for word in words:
            final.append(adler32(word.encode()) % top_words)
        return final

    def loadAnswers(self, fname):
        f = open(fname)
        d = {}
        i = 0
        for line in f:
            fields = line.split(',')
            try:
            	d[int(fields[0])] = GenericAnswer(fields[1], fields[2])
            except ValueError:
                print("There was an encoding error on this line: " + str(line))
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
    import sys
    classifier = GenericAnswerConstruction("trained_model.m5", "genericAnswers.csv")
    for arg in sys.argv[1:]:
        print(arg + ":  " + classifier.generateGenericAnswer(arg).getAnswer())
    print("__________")
