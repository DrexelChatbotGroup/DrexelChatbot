
class ErrorHandler():
	def handle(ex):
		if type(ex) is BadQuestionException:
			print("V V V SAD! ")
		elif type(ex) is BadAnswerException:
			print("JUST V SAD! ")
		else:
			print("BAD")

class ChatbotException(BaseException):
	"""Base class for exceptions of the Drexel Chatbot"""
	pass

class BadQuestionException(ChatbotException):
	pass

class BadAnswerException(ChatbotException):
	pass
