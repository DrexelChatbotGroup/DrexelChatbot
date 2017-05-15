"""
UNFINISHED
Implementation of the IEAgent interface for the College of Engineering Management faculty website, located here:
http://drexel.edu/engmgmt/egmt/contact/faculty/

Data is stored in an html table, but there are so many divs that trying to
naviagate the table is a nightmare. However, there is a div with class name
"user-profile-stub clearfix" that contains each indiviual person, so that can
be used to keep place in the file. 
The order of information:
name
education
title
department
room
phone
email
areas of expertise

"""

__all__ = ['EgmtIEAgent']
__version__ = '0.1'
__author__ = 'Nanxi Zhang'

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
            #print (elems[i])
            nameStr = elems[i].find('h1').getText()
            print (nameStr)
            titleStr = elems[i].find('p').getText()
            print (titleStr)
            emailStr = elems[i].select('a')[2].getText()
            print (emailStr)
            if elems[i].select('img'):
                img_src = elems[i].select('img')[0]['src']
                pictureStr = self._flink + img_src
                print (pictureStr)
            #phoneStr = elems[i].select('p')[3].getText()
            #roomStr = elems[i].select('p')[4].getText()
            #print (phoneStr)
            #print (roomStr)
            #interestsStr = elems[i].select('p')[5].getText().strip()
        #print (interestsStr)
            #prof = ttl.TtlFileEntry()
                
            #prof.write_to(ttl_file)
        
        ttl_file.close()
        return ttl_file
