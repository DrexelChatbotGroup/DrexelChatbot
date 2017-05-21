from chatbot.postag import NLTKPOSTag
from chatbot.genericquestion import GenericQuestion
from chatbot.errors import BadQuestionException
import logging
import re

class GenericQuestionConstruction():
    def __init__(self, question, db):
        self.question = question
        self.db = db
        self.tag_list = []

    def getgenericquestion(self):
        logging.debug("Running Generic Question Construction...")
        postag_class = NLTKPOSTag()
        #note: the library has been seen to have issue with non-English names (e.g.
        #'Yuan An'). Also, it considers 'Does' to be a proper noun
        self.tag_list = postag_class.getpostag(self.question)
        logging.debug("tag_list: " + str(self.tag_list))
        rep_list = self.findrepresentation()
        logging.debug("rep_list: " + str(rep_list))

        #if database does not have information about nouns in the question, stop 
        if len(rep_list) == 0:
            logging.warning("rep_list size 0, throwing exception")
            raise BadQuestionException()

        #replace nouns with their genericRepresentations
        paddedquestion = self.question
        for key, value in rep_list.items():
            paddedquestion = paddedquestion.replace(value, '(' + key + ')')
            #capitalise strings with Day representation
            if key == 'Day':
                rep_list[key] = value.title()

        #create returned object which contains a string and a dictionary 
        #whose keys are nouns in original question and values are generic 
        #representations of the keys
        returnedobject = GenericQuestion()
        returnedobject.paddedquestion = paddedquestion
        returnedobject.rep_list = rep_list
        return returnedobject

    def findrepresentation(self):
        #retrieve all nouns
        noun_list = []
        count = 0
        logging.debug("Getting noun list")
        while count < len(self.tag_list):
            word = self.tag_list[count][0]
            tag = self.tag_list[count][1]
            logging.debug("word: %s - tag: %s" % (word, tag))
            if tag[0].lower() == 'n':
                noun = word
		#consider adjacent proper nouns to be 1 noun
                if tag[:3].lower() == 'nnp':
                    while count + 1 < len(self.tag_list):
                        count = count + 1
                        word = self.tag_list[count][0]
                        tag = self.tag_list[count][1]
                        if tag[:3].lower() == 'nnp':
                            noun = noun + ' ' + word
                        else:
                            count = count - 1
                            break
                noun_list.append(noun)
                logging.debug("count: %s - noun: %s" % (str(count), noun))
            count = count + 1
        rep_list = {}

        #create a dictionary whose keys are generic representations 
        #of the nouns (if found) and values are the nouns
        logging.debug("Querying database for representations")
        for noun in noun_list:
            rep = ""
            #get a dictionary from database whose key is 
            #'property' and value is generic representation
            #of the noun
            query_string = """
            prefix cb: <http://drexelchatbot.com/rdf/>

                        SELECT ?property
            WHERE
            {
                ?s cb:name \"%s\" .
                ?s cb:property ?property .
            }
            """ % noun
            logging.debug("query_string: " + query_string)
            rep = self.db.query(query_string)
            logging.debug("noun: %s - rep: %s" % (noun, str(rep)))

            #store tuples
            if rep:
                rep_list[rep['property']] = noun

        #resolve special cases
        #replace substrings represent weekday with Day
        weekdays = re.findall(r"([Mm]on|[Tt]ues|[Ww]ed|[Tt]hurs|[Ff]ri|[Ss]atur|[Ss]un)day", self.question)
        if weekdays:
            for weekday in weekdays:
                rep_list['Day'] = weekday

        #replace substrings contain only 3 or 4 digits with Room
        for pair in self.tag_list:
            word = pair[0]
            match = re.search('^\d{3,4}[a-zA-Z]?$', word)
            if match:
                rep_list['Room'] = word

        return rep_list
