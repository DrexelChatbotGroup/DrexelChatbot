"""
Implementation of the IEAgent interface for the College of Engineering Management 
faculty website, located here: http://drexel.edu/engmgmt/egmt/contact/faculty/
"""

__all__ = ['EgmtIEAgent']
__version__ = '0.2'
__author__ = 'Nanxi Zhang and Tom Amon'

import requests
from bs4 import BeautifulSoup
import abc
from .ieagent import IEAgent, writeHTMLFile
import ttl

    
class EgmtIEAgent(IEAgent):

    _link = "http://drexel.edu/engmgmt/egmt/contact/faculty/"
    _flink = "http://www.drexel.edu"
    ttl_filename = "ttl/egmt.ttl"

    def write_ttl(self):
        ttl_file = ttl.TtlFile(self.ttl_filename)

        webpage = requests.get(self._link)
        try:
            webpage.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        soup = BeautifulSoup(webpage.text, "html.parser")
        
        elems = soup.select('tr')
        for i in range(3, len(elems)):
            e = elems[i]
            nameStr = elems[i].find('h1').getText()
            titleStr = elems[i].find('p').getText()
            a_href = elems[i].select('a')[1]['href']
            websiteStr = self._flink + a_href
            emailStr = elems[i].select('a')[2].getText()
            if elems[i].select('img'):
                img_src = elems[i].select('img')[0]['src']
                pictureStr = self._flink + img_src
            phoneStr = elems[i].select('td')[2].find('br').next_sibling
            if not phoneStr.isspace():
                phoneStr = phoneStr.split(":")[1]
            prof = ttl.TtlFileEntry()
            prof.name = nameStr
            prof.property = 'faculty'
            prof.website = websiteStr
            prof.title = titleStr
            prof.email = emailStr
            prof.phone = phoneStr
            prof.website = websiteStr
                
            prof.write_to(ttl_file)
        
        ttl_file.close()
        return ttl_file
