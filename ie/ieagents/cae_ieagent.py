"""
Implementation of the IEAgent interface for the College of Civil, Architectural, and Environmental Engineering faculty website, located here: http://drexel.edu/cae/contact/faculty/

Data is stored in an html table, with each person have a single row(tr).
The data, very conviently, is all in their own div. So just going through 
each div of the row should everything. The data is in the order:
Name
Title
Department
Interests
Email
Phone
Office

"""

__all__ = ['EceIEAgent']
__version__ = '0.1'
__author__ = 'Nanxi Zhang'

import requests
from bs4 import BeautifulSoup
import abc
from .ieagent import IEAgent
import ttl


class CaeIEAgent(IEAgent):

    _link = "http://drexel.edu/cae/contact/faculty/"
    ttl_filename = "ttl/cae.ttl"

    def write_ttl(self):
        ttl_file = ttl.TtlFile(self.ttl_filename)

        webpage = requests.get(self._link)
        try:
            webpage.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        soup = BeautifulSoup(webpage.text, "html.parser")

        elems = soup.select('tr')
        for i in range(2, len(elems)-6):
            #print (elems[i])
            nameStr = elems[i].find('strong').getText()
            print (nameStr)
            titleStr = elems[i].br.next_sibling.strip()
            #print (titleStr)
            emailStr = elems[i].select('p')[2].getText()
            phoneStr = elems[i].select('p')[3].getText()
            roomStr = elems[i].select('p')[4].getText()
            #print (emailStr)
            #print (phoneStr)
            #print (roomStr)
            interestsStr = elems[i].select('p')[5].getText().strip()
            #print (interestsStr)

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
