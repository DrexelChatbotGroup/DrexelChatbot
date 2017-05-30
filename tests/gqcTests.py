import unittest
from chatbot.gqc import GenericQuestionConstruction
from chatbot.errors import BadQuestionException
from chatbot.postag import NLTKPOSTag
from database.stardog import StardogDB

class TestGqcMethods(unittest.TestCase):

    def test_getpostag(self):
        postag = NLTKPOSTag()
        tag_list = postag.getpostag("sample question")
        self.assertEqual(tag_list[0][1], 'JJ')
        self.assertEqual(tag_list[0][0], 'sample')
        self.assertEqual(tag_list[1][1], 'NN')
        self.assertEqual(tag_list[1][0], 'question')

    def test_getgenericquestion(self):
        db = StardogDB("chatbotDB")
        gap = GenericQuestionConstruction("What is Mongan's email?",db)
        returnedobject = gap.getgenericquestion()
        self.assertEqual(returnedobject.paddedquestion, "what is (faculty)'s email?")
        self.assertEqual(returnedobject.rep_list['faculty'], 'Mongan')

    def test_getgenericquestion_with_day(self):
        db = StardogDB("chatbotDB")
        gap = GenericQuestionConstruction("What is Monday?",db)
        returnedobject = gap.getgenericquestion()
        self.assertEqual(returnedobject.paddedquestion, "what is (Day)?")
        self.assertEqual(returnedobject.rep_list['Day'], 'Monday')
    
    def test_bad_question(self):
        db = StardogDB("chatbotDB")
        gap = GenericQuestionConstruction("What is it?",db)
        self.assertRaises(BadQuestionException, gap.getgenericquestion)

if __name__ == '__main__':
    unittest.main()
