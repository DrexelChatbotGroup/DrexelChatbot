import socket
import sys


class GenericAnswer:
    def __init__(self, newAnswer, newQuery):
        self.answer = newAnswer
        self.query = newQuery

    def getAnswer(self):
        return self.answer

    def getQuery(self):
        return self.query

class GenericAnswerConstruction:
    def __init__(self, configFile, answerFile):
        pass

    def generateGenericAnswer(self, genericQuestion):
        HOST, PORT = "localhost", 9999

        # Create a socket (SOCK_STREAM means a TCP socket)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(bytes(genericQuestion + "\n", "utf-8"))

            # Receive data from the server and shut down
            answer = str(sock.recv(1024), "utf-8")
            query = str(sock.recv(1024), "utf-8")

        #print("Sent:     {}".format(genericQuestion))
        #print("Received answer: {}".format(answer))
        #print("Received query: {}".format(query))

        return GenericAnswer(answer, query)