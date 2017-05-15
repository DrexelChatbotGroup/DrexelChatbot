"""
UNFINISHED
Implementation of the IEAgent interface for the College of Chemical and Biological Engineering faculty website, located here: http://drexel.edu/cae/contact/faculty/

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

__all__ = ['CbeIEAgent']
__version__ = '0.1'
__author__ = 'Nanxi Zhang'

import requests
from bs4 import BeautifulSoup
import abc
from .ieagent import IEAgent
import ttl


class CbeIEAgent(IEAgent):

    _link = "http://drexel.edu/cbe/contact/faculty/"
    _flink = "http://drexel.edu/"
    ttl_filename = "ttl/cbe.ttl"

    def write_ttl(self):
        ttl_file = ttl.TtlFile(self.ttl_filename)

        webpage = requests.get(self._link)
        try:
            webpage.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        soup = BeautifulSoup(webpage.text, "html.parser")

        elems = soup.select('tr')
        for i in range(2, len(elems)-14):
            
            prof = ttl.TtlFileEntry()
            
            #print (elems[i])
            nameStr = elems[i].find('strong').getText().strip()
            #print (nameStr)
            titleStr = elems[i].br.next_sibling.strip()
            #print (titleStr)
            contactStr = elems[i].select('td')[1].getText()
            contactList = contactStr.splitlines()
            #print (contactList)
            if contactList[1]:
                emailStr = contactList[1].strip()
                prof.email = emailStr
                #print (emailStr)
            if len(contactList) > 2 and contactList[2]:
                phoneStr = contactList[2].strip()
                prof.phone = phoneStr
                #print (phoneStr)
            if len(contactList) > 3 and contactList[3]:
                roomStr = contactList[3].strip()
                prof.room = roomStr
                #print (roomStr)
            interestsStr = elems[i].select('td')[2].getText().strip()
            #print (interestsStr)
            img_src = elems[i].select('img')[0]['src'].strip()
            pictureStr = self._flink + img_src
            #print (pictureStr)

            prof.name = nameStr
            prof.property = "faculty"
            prof.title = titleStr
            prof.interests = interestsStr
            prof.picture = pictureStr

            prof.write_to(ttl_file)

        ttl_file.close()

        return ttl_file
