
class ErrorHandler():
	def handle(ex):
		if type(ex) is BadQuestionException:
			print("Sorry I did not understand your question. I am just a bot and I am not as smart as you. Maybe someday I will be smarter and rule your world.")
		elif type(ex) is BadAnswerException:
			print("Sorry I don't have an answer for that. I could give you a link to the website which might have the answer but my programmers will implement it next quarter.")
		else:
			print("I don't know what happened. I have error in my system and the programmers did not catch that error. They are not cool.")

class ChatbotException(BaseException):
	"""Base class for exceptions of the Drexel Chatbot"""
	pass

class BadQuestionException(ChatbotException):
	pass

class BadAnswerException(ChatbotException):
	pass
