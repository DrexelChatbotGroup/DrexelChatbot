import unittest
from chatbot.gap import GenericAnswerPopulation
from chatbot.errors import BadQuestionException
from chatbot.errors import BadAnswerException
from chatbot.liveGac import GenericAnswer
from database.stardog import StardogDB

class TestGapMethods(unittest.TestCase):

    def test_populate_simple(self):
        chatbotDB = StardogDB("chatbotDB")
        answer = "(faculty)'s office is in (room)"
        query = '''
        prefix cb: <http://drexelchatbot.com/rdf/> 
        select ?room
        where {
        ?s cb:room ?room . 
        ?s cb:name "(faculty)" 
        }
        '''
        dic = {'faculty' : 'Balduccini'}
        genericAnswer = GenericAnswer(answer, query)
        gap = GenericAnswerPopulation(genericAnswer, chatbotDB)
        answer = gap.populate(dic)
        self.assertEqual(answer, "Balduccini's office is in Rush 233C")

    def test_populate_complex(self):
        chatbotDB = StardogDB("chatbotDB")
        answer = "(faculty)'s website is (website) and room is (room)"
        query = '''
        prefix cb: <http://drexelchatbot.com/rdf/> 
        select ?website ?room
        where {
        ?s cb:name "(faculty)" . 
        ?s cb:website ?website .
        ?s cb:room ?room 
        }
        '''
        dic = {'faculty' : 'Balduccini'}
        genericAnswer = GenericAnswer(answer, query)
        gap = GenericAnswerPopulation(genericAnswer, chatbotDB)
        answer = gap.populate(dic)
        solution = "Balduccini's website is http://www.cs.drexel.edu/~mb3368 and room is Rush 233C"
        self.assertEqual(answer, solution)


    def test_populate_bad_answer_wrong_query(self):
        chatbotDB = StardogDB("chatbotDB")
        answer = "(faculty)'s office is in (room)"
        query = '''
        prefix cb: <http://drexelchatbot.com/rdf/> 
        select ?room
        where {
        ?s cb:room ?room . 
        ?s cb:name "(faculty)" 
        }
        '''
        dic = {'building' : 'uCross'}
        genericAnswer = GenericAnswer(answer, query)
        gap = GenericAnswerPopulation(genericAnswer, chatbotDB)
        self.assertRaises(BadAnswerException, gap.populate, dic)

    def test_populate_bad_answer_null_query(self):
        chatbotDB = StardogDB("chatbotDB")
        answer = "(faculty)'s office is in (room)"
        query = '''null'''
        dic = {'building' : 'uCross'}
        genericAnswer = GenericAnswer(answer, query)
        gap = GenericAnswerPopulation(genericAnswer, chatbotDB)
        self.assertRaises(BadAnswerException, gap.populate, dic)

    def test_populate_bad_answer_wrong_answer(self):
        chatbotDB = StardogDB("chatbotDB")
        answer = "(building)'s office is in (room)"
        query = '''
        prefix cb: <http://drexelchatbot.com/rdf/> 
        select ?room
        where {
        ?s cb:room ?room . 
        ?s cb:name "(faculty)" 
        }
        '''
        dic = {'faculty' : 'Balduccini'}
        genericAnswer = GenericAnswer(answer, query)
        gap = GenericAnswerPopulation(genericAnswer, chatbotDB)
        self.assertRaises(BadAnswerException, gap.populate, dic)

    def test_populate_week(self):
        chatbotDB = StardogDB("chatbotDB")
        answer = "(building) opens (startTime) on (Day)"
        query = '''
        prefix cb: <http://drexelchatbot.com/rdf/> 
        select ?startTime
        where {
        ?s cb:startTime ?startTime . 
        ?s cb:name "(building)" 
        }
        '''
        dic = {'building' : 'Rush', 'Day': 'Monday'}
        genericAnswer = GenericAnswer(answer, query)
        gap = GenericAnswerPopulation(genericAnswer, chatbotDB)
        answer = gap.populate(dic)
        self.assertEqual(answer, "Rush opens 7:30 a.m. on Monday")

if __name__ == '__main__':
    unittest.main()
