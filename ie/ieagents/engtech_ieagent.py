"""
Implementation of the IEAgent interface for the College of Engineering's
Engineering Technology, loacted here: http://drexel.edu/engtech/contact/faculty/
"""

__all__ = ['EngTechIEAgent']
__version__ = '0.1'
__author__ = 'Tom Amon'

import requests
from bs4 import BeautifulSoup
import abc
from .ieagent import IEAgent, writeHTMLFile
import ttl

class EngTechIEAgent(IEAgent):

    _flink = "http://drexel.edu"
    _link = "http://drexel.edu/engtech/contact/faculty/"
    ttl_filename = "ttl/engtech.ttl"

    def write_ttl(self):
        ttl_file = ttl.TtlFile(self.ttl_filename)

        webpage = requests.get(self._link)
        try:
            webpage.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        soup = BeautifulSoup(webpage.text, "html.parser")
        writeHTMLFile(soup, "test.html")

        table = soup.select('tbody')[0]
        elems = table.select('tr')
        for i in range(2, len(elems)):
            rows = elems[i].select("td")
            picture = rows[0].find('img')['src']
            picture = self._flink + picture
            nameStr = rows[0].find('h1').getText()
            titleStr = rows[0].find('h2').getText()
            emailStr = rows[1].find('a').getText()
            phoneStr = rows[1].find('br').next_sibling
            phoneStr = phoneStr.split(":")[1]
            phoneStr = phoneStr.split('\n')[0]
            interestsStr = rows[2].getText()

            prof = ttl.TtlFileEntry()

            prof.name = nameStr
            prof.property = "faculty"
            prof.picture = picture 
            prof.title = titleStr
            prof.email = emailStr
            prof.phone = phoneStr
            #prof.room = roomStr
            prof.Interests = interestsStr

            prof.write_to(ttl_file)
    
        ttl_file.close()

        return ttl_file
