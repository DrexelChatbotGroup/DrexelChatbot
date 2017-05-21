import unittest
from chatbot.gqc import GenericQuestionConstruction
from chatbot.postag import NLTKPOSTag

class TestGqcMethods(unittest.TestCase):

	def test_getpostag(self):
		postag = NLTKPOSTag()
		tag_list = postag.getpostag("sample question")
		self.assertEqual(tag_list[0][1], 'JJ')
		self.assertEqual(tag_list[0][0], 'sample')
		self.assertEqual(tag_list[1][1], 'NN')
		self.assertEqual(tag_list[1][0], 'question')

	def test_getgenericquestion(self):
		gap = GenericQuestionConstruction("sample question","db")
		returnedobject = gap.getgenericquestion()
		self.assertEqual(returnedobject.paddedquestion, 'sample **Test**')
		self.assertEqual(returnedobject.rep_list['question'], '**Test**')

if __name__ == '__main__':
	unittest.main()
