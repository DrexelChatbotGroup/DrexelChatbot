import unittest
from chatbot.gap import GenericAnswerPopulation
from chatbot.errors import BadQuestionException
from chatbot.errors import BadAnswerException

class TestGapMethods(unittest.TestCase):

    def test_populate1(self):
        genericAnswer = {
            'answer' : "(Professor)'s office is in (Location)",
            'dictionary1' : {'Professor' : 'Balduccinni'},
            'query' : "Select Location where Professor = (Professor)",
            'dictionary2' : {'Location' : 'UC102'}
        }
        gap = GenericAnswerPopulation(genericAnswer, "db")
        answer = gap.populate()
        self.assertEqual(answer, "Balduccinni's office is in UC102")

    def test_populate2(self):
        genericAnswer = {
            'question' : "Do you have (Professor)'s (Website)?",
            'answer' : "(Professor)'s website is at (Website)",
            'dictionary1' : {'Professor' : 'Marcello Balduccinni'},
            'query' : "Select Website where Professor = (Professor)",
            'dictionary2' : {'Website' : 'http://www.cs.drexel.edu/~mb3368'}
        }
        gap = GenericAnswerPopulation(genericAnswer, "db")
        answer = gap.populate()
        self.assertEqual(answer, "Marcello Balduccinni's website is at http://www.cs.drexel.edu/~mb3368")

    def test_populate3(self):
        genericAnswer = {
            'question' : "What is (Professor)'s area of (Research)?",
            'answer' : "(Professor)'s areas of research are (Research)",
            'dictionary1' : {'Professor' : 'Mongan'},
            'query' : "Select Research where Professor = (Professor)",
            'dictionary2' : {'Research' : 'service-oriented architectures, program comprehension, reverse engineering, software engineering, computer architecture, computer science education'}
        }
        gap = GenericAnswerPopulation(genericAnswer, "db")
        answer = gap.populate()
        self.assertEqual(answer, "Mongan's areas of research are service-oriented architectures, program comprehension, reverse engineering, software engineering, computer architecture, computer science education")


    def test_populate4(self):
        genericAnswer = {
            'answer' : "(Professor)'s office is in (Location)",
            'dictionary1' : {'Location' : 'UC102'},
            'query' : "Select Location where Professor = (Professor)",
            'dictionary2' : {'Location' : 'UC102'}
        }
        gap = GenericAnswerPopulation(genericAnswer, "db")
        self.assertRaises(BadQuestionException, gap.populate)

    def test_populate5(self):
        genericAnswer = {
            'answer' : "(Professor)'s office is in (Location)",
            'dictionary1' : {'Professor' : 'Balduccinni'},
            'query' : "Select Location where Professor = (Professor)",
            'dictionary2' : {}
        }
        gap = GenericAnswerPopulation(genericAnswer, "db")
        self.assertRaises(BadAnswerException, gap.populate)


if __name__ == '__main__':
    unittest.main()