"""
Wrapper class and functions for interacting with a stardog database.
"""

__all__ = ["StardogDB"]
__version__ = '0.1'
__author__ = 'Tom Amon and Nanxi Zhang'

import subprocess

_STARDOG_INSTALL_PATH = "/home/stardog/bin/"


class StardogDB:

    def __init__(self, database_name):
        self._database_name = database_name

    def remove_all(self):
        #./stardog data add db filename.ttl
        path = _STARDOG_INSTALL_PATH + "stardog"
        command = [path, "data", "remove", "-a", self._database_name]
        subprocess.call(command)

    def add(self, ttl_files):
        #./stardog data add db filename.ttl
        path = _STARDOG_INSTALL_PATH + "stardog"
        command = [path, "data", "add", self._database_name]
        subprocess.call(command + ttl_files)

    def query(self, str_query):
        #./stardog query chatbotDB query
        path = _STARDOG_INSTALL_PATH + "stardog"
        out = subprocess.check_output([path, "query", self._database_name, "-f",
        "CSV", str_query])
        out = out.decode("utf-8")
        res = out.splitlines()
        res_dict = {}
        if len(res) == 2:
            keys = res[0].split(',')
            values = res[1].split(',')
            i = 0
            for k, v in zip(keys, values):
                res_dict[k] = v
        return res_dict


if __name__ == "__main__":
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
    #print(sdb.query(test))

    test2 = """
    prefix cb: <http://drexelchatbot.com/rdf/>
    SELECT ?phone ?email
    WHERE
    {
        ?s cb:name "Marcello Balduccini" .
        ?s cb:phone ?phone .
        ?s cb:email ?email .
    }
    """
    #print(sdb.query(test2))

    test3 = """
    prefix cb: <http://drexelchatbot.com/rdf/>
    SELECT ?phone ?email
    WHERE
    {
        ?s cb:name "NOT REAL LOSER" .
        ?s cb:phone ?phone .
        ?s cb:email ?email .
    }
    """
    #print(sdb.query(test3))

    test3 = """
    prefix cb: <http://drexelchatbot.com/rdf/>
    SELECT ?p ?o
    WHERE
    {
        ?s cb:name "Mongan" .
	?s ?p ?o .
    }
    """
    print(sdb.query(test3))
