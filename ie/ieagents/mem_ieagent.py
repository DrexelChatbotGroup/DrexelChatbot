"""
Implementation of the IEAgent interface for the mechanical engineering and
mechanics website, located here: http://drexel.edu/mem/contact/faculty-directory/
"""

__all__ = ['MemIEAgent']
__version__ = '0.1'
__author__ = 'Tom Amon'

import requests
from bs4 import BeautifulSoup
import abc
from .ieagent import IEAgent
import ttl

class MemIEAgent(IEAgent):

    _link = "http://drexel.edu/mem/contact/faculty-directory/"
    ttl_filename = "ttl/mem.ttl"

    def write_ttl(self):
        ttl_file = ttl.TtlFile(self.ttl_filename)

        webpage = requests.get(self._link)
        try:
            webpage.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        soup = BeautifulSoup(webpage.text, "html.parser")

        elems = soup.select('tr')
        for i in range(2, len(elems)):
            nameStr = elems[i].find('strong').getText()
            titleStr = elems[i].find('br').next_sibling
            contact_info = elems[i].select('p')[2].getText().split('\n')
            emailStr = contact_info[0]
            phoneStr = contact_info[1]
            roomStr = contact_info[2]
            interestsStr = elems[i].select('p')[3].getText()

            prof = ttl.TtlFileEntry()

            prof.name = nameStr
            prof.property = "faculty"
            prof.title = titleStr
            prof.email = emailStr
            prof.phone = phoneStr
            prof.room = roomStr
            prof.Interests = interestsStr

            prof.write_to(ttl_file)
    
        ttl_file.close()

        return ttl_file
