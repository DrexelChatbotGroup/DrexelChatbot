import unittest
from database.stardog import StardogDB

class TestStardogDB(unittest.TestCase):
    def test_query_return_type(self):
        test = """
        prefix cb: <http://drexelchatbot.com/rdf/>
        SELECT ?property
        WHERE
        {
            ?s cb:name "Marcello Balduccini" .
            ?s cb:property ?property .
        }
        """
        sdb = StardogDB("chatbotDB")
        res = sdb.query(test)

        self.assertIsInstance(res, dict)

    def test_query_single_data(self):
        test = """
        prefix cb: <http://drexelchatbot.com/rdf/>
        SELECT ?property
        WHERE
        {
            ?s cb:name "Marcello Balduccini" .
            ?s cb:property ?property .
        }
        """
        sdb = StardogDB("chatbotDB")
        res = sdb.query(test)

        expected = {"property" : "faculty"}
        self.assertEqual(res, expected)

    def test_query_multiple_data(self):
        test = """
        prefix cb: <http://drexelchatbot.com/rdf/>
        SELECT ?phone ?email
        WHERE
        {
            ?s cb:name "Marcello Balduccini" .
            ?s cb:phone ?phone .
            ?s cb:email ?email .
        }
        """
        sdb = StardogDB("chatbotDB")
        res = sdb.query(test)
        expected = {"phone" : "215.571.3603", 
                    "email" : "marcello.balduccini@drexel.edu" }
        self.assertEqual(res, expected)

    def test_query_no_data(self):
        test = """
        prefix cb: <http://drexelchatbot.com/rdf/>
        SELECT ?phone ?email
        WHERE
        {
            ?s cb:name "NOT REAL LOSER" .
            ?s cb:phone ?phone .
            ?s cb:email ?email .
        }
        """
        sdb = StardogDB("chatbotDB")
        res = sdb.query(test)
        expected = {}
        self.assertEqual(res, expected)

if __name__ == '__main__':
    unittest.main()
