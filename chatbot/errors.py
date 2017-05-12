
class ErrorHandler():
    @classmethod
    def handle(clsobj, ex):
        if type(ex) is BadQuestionException:
            print("Sorry I did not understand your question. I am just a bot and I am not as smart as you. Maybe someday I will be smarter and rule your world.")
        elif type(ex) is BadAnswerException:
            query = """prefix cb: <http://drexelchatbot.com/rdf/> select ?website where { ?s cb:name \"(target)\" . ?s cb:website ?website}"""
            for key in ex.dictionary.keys():
                new_query = query.replace("(target)", ex.dictionary[key])
                returned_dict = ex.db.query(new_query)
                if returned_dict is not None:
                    website = returned_dict['website']
                    print("Sorry I don't have an answer for that. But I found ", ex.dictionary[key], "'s website: ", '<a href="', website, '">', website, '</a>')
                else:
                    print("Sorry I don't have an answer for that. I also could not find the website for %s" % ex.dictionary[key])
        else:
            print("I don't know what happened. I have error in my system and the programmers did not catch that error. They are not cool.")

class ChatbotException(BaseException):
    """Base class for exceptions of the Drexel Chatbot"""
    pass

class BadQuestionException(ChatbotException):
    pass

class BadAnswerException(ChatbotException):
    def __init__(self, db, dictionary):
        self.dictionary = dictionary
        self.db = db
