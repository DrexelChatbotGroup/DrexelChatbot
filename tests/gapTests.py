import unittest
from chatbot.gap import GenericAnswerPopulation

class TestGapMethods(unittest.TestCase):

    def test_populate(self):
        gap = GenericAnswerPopulation("genericAnswer", "db")
        answer = gap.populate()
        self.assertEqual(answer, 'not implemented yet')

if __name__ == '__main__':
    unittest.main()