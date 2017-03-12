"""
Implementation of the IEAgent interface for the College of Engineering, Electrical and
Computer Engineering faculty website, located here: http://drexel.edu/ece/contact/faculty-directory/

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


class EceIEAgent(IEAgent):

    _link = "http://drexel.edu/ece/contact/faculty-directory/"
    ttl_filename = "ttl/ece.ttl"

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
            #print (elems[i])
            nameStr = elems[i].find('strong').getText()
            #print (nameStr)
            titleStr = elems[i].find('em').getText()
            #print (titleStr)
            contactStr = elems[i].select('p')[1].getText()
            contactList = contactStr.splitlines()
            if contactList[1]:
                emailStr = contactList[1].strip()
            if len(contactList) > 2 and contactList[2]:
                phoneStr = contactList[2].strip()
            if len(contactList) > 3 and contactList[3]:
                roomStr = contactList[3].strip()
            #print (emailStr)
            #print (phoneStr)
            #print (roomStr)
            interestsStr = elems[i].select('p')[3].getText()
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
