"""
Implementation of the IEAgent interface for the School of hospitatily and
management, located here: http://drexel.edu/cci/contact/Faculty/
"""

__all__ = ['HsmIEAgent']
__version__ = '0.2'
__author__ = 'Tom Amon'

import requests
from bs4 import BeautifulSoup
import abc
from .ieagent import IEAgent, writeHTMLFile
import ttl


class HsmIEAgent(IEAgent):

    _flink = "http://drexel.edu/"
    _link = "http://drexel.edu/hsm/about/faculty/"
    ttl_filename = "ttl/hsm.ttl"

    def write_ttl(self):
        ttl_file = ttl.TtlFile(self.ttl_filename)

        webpage = requests.get(self._link)
        try:
            webpage.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        soup = BeautifulSoup(webpage.text, "html.parser")

        tables = soup.select('article')
        for i in range(1, len(tables)):
            elems = tables[i].select('tr')
            for j in range(1, len(elems)):
                data = elems[j].select('td')
                
                prof = ttl.TtlFileEntry()
                prof.name = data[0].getText()
                prof.property = "faculty"
                prof.title = data[1].select('br')[0].previous_sibling
                prof.department = data[1].select('br')[0].next_sibling
                prof.email = data[2].select('br')[0].previous_sibling.getText()
                prof.phone = data[2].select('br')[0].next_sibling
                prof.write_to(ttl_file)
    
        ttl_file.close()
        return ttl_file
