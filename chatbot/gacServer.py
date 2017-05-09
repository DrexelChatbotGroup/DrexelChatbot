import socketserver
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
            d[int(fields[0])] = GenericAnswer(fields[1], fields[2])
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

answer = "/home/DrexelChatbot/chatbot/genericAnswers.csv"
config = "/home/DrexelChatbot/chatbot/trained_model.m5"
gac_object = GenericAnswerConstruction(config, answer)


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data.decode("utf8"))
        # just send back the same data, but upper-cased
        genericanswer = gac_object.generateGenericAnswer(self.data.decode("utf8"))
        print(genericanswer.getAnswer())
        self.request.sendall(genericanswer.getAnswer().encode("utf8"))
        self.request.sendall(genericanswer.getQuery().encode("utf-8"))

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
