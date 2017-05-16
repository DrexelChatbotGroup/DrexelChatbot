"""
Wrapper class and functions for interacting with a stardog database.
"""

__all__ = ["StardogDB"]
__version__ = '0.1'
__author__ = 'Tom Amon and Nanxi Zhang'

import subprocess
from SPARQLWrapper import SPARQLWrapper, JSON

_STARDOG_INSTALL_PATH = "/home/stardog/bin/"
_STARDOG_ENDPOINT = "http://localhost:5820/chatbotDB/query/"


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
        command = [path, "data", "add", self._database_name] + ttl_files
        subprocess.call(command)

    def query(self, str_query):
        sparql = SPARQLWrapper(_STARDOG_ENDPOINT)
        sparql.setQuery(str_query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        bindings = results["results"]["bindings"]
        res = {}
        if bindings:
            for key in bindings[0]:
                res[key] = bindings[0][key]["value"]
        return res
