"""
Implementation of the IEAgent interface for the Goodwin College of Profession studies
located here: http://drexel.edu/goodwin/about/directory/

"""

__all__ = ['GoodwinIEAgent']
__version__ = '0.2'
__author__ = 'Tom Amon'

import requests
from bs4 import BeautifulSoup
import abc
from .ieagent import IEAgent, writeHTMLFile
import ttl


class GoodwinIEAgent(IEAgent):

    _flink = "http://drexel.edu"
    _link = "http://drexel.edu/goodwin/about/directory/"
    ttl_filename = "ttl/goodwin.ttl"

    def write_ttl(self):
        ttl_file = ttl.TtlFile(self.ttl_filename)

        webpage = requests.get(self._link)
        try:
            webpage.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        soup = BeautifulSoup(webpage.text, "html.parser")

        elems = soup.select('tr')
        for i in range(0, len(elems)):
            data = elems[i]
            img_src = data.select('img')[0]['src']
            data = data.getText().strip().split('\n')
            prof = ttl.TtlFileEntry()
            prof.picture = self._flink + img_src
            prof.property = "faculty"
            prof.name = data[0]
            prof.title = data[1]
            if not data[2].isspace():
                prof.phone = data[2]
            if not data[3].isspace():
                prof.email = data[3]

            prof.write_to(ttl_file)
    
        ttl_file.close()
        return ttl_file
