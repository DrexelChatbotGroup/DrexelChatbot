"""
Implementation of the IEAgent interface for the College of Engineerings
meterials Science and Engineering, located here:
http://drexel.edu/materials/contact/faculty/
"""

__all__ = ['MaterialsIEAgent']
__version__ = '0.1'
__author__ = 'Tom Amon'

import requests
from bs4 import BeautifulSoup
import abc
from .ieagent import IEAgent, writeHTMLFile
import ttl

class MaterialsIEAgent(IEAgent):

    _link = "http://drexel.edu/materials/contact/faculty/"
    _flink = "http://drexel.edu"
    ttl_filename = "ttl/materials.ttl"

    def write_ttl(self):
        ttl_file = ttl.TtlFile(self.ttl_filename)

        webpage = requests.get(self._link)
        try:
            webpage.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        soup = BeautifulSoup(webpage.text, "html.parser")

        table = soup.select('tbody')[0]
        elems = table.select('tr')
        for i in range(0, len(elems)):
            rows = elems[i].select("td")
            picture = rows[0].find('img')['src']
            picture = self._flink + picture
            nameStr = rows[0].find('h2').getText()
            titleStr = rows[0].find('h3').getText()
            emailStr = rows[1].find('a').getText()
            phoneStr = rows[1].find('br').next_sibling
            phoneStr = phoneStr.split(":")[1]
            phoneStr = phoneStr.split('\n')[0]

            prof = ttl.TtlFileEntry()

            prof.name = nameStr
            prof.property = "faculty"
            prof.title = titleStr
            prof.email = emailStr
            prof.phone = phoneStr
            #prof.room = roomStr
            #prof.Interests = interestsStr

            prof.write_to(ttl_file)
    
        ttl_file.close()

        return ttl_file

