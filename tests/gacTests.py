import unittest
import chatbot.liveGac as gac
from chatbot.liveGac import GenericAnswer

class TestGacMethods(unittest.TestCase):
    answer = "/home/DrexelChatbot/chatbot/genericAnswers.csv"
    config = "/home/DrexelChatbot/chatbot/trained_model.m5"

    def test_getGenericAnswer(self):
        q = "What is (faculty)'s email?"
        gac_object = gac.GenericAnswerConstruction(self.config, self.answer)
        genericanswer = gac_object.generateGenericAnswer(q)
        self.assertEqual(genericanswer.getAnswer(), "(faculty)'s email address is (email).")

if __name__ == '__main__':
    unittest.main()
