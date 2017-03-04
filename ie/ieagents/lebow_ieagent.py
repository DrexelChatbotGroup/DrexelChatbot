"""
Implementation of the IEAgent interface for the College of computing and
infomatics faculty website, located here:
http://www.lebow.drexel.edu/faculty-and-research/faculty-directory

Data is stored in an html table, but there are so many divs that trying to
naviagate the table is a nightmare. However, there is a div with class name
"user-profile-stub clearfix" that contains each indiviual person, so that can
be used to keep place in the file. 
The order of information:
name
education
title

"""

__all__ = ['LebowIEAgent']
__version__ = '0.1'
__author__ = 'Tom Amon'

import requests
from bs4 import BeautifulSoup
import abc
from .ieagent import IEAgent, DatabaseRow, writeHTMLFile

    
class LebowIEAgent(IEAgent):

    _link="http://www.lebow.drexel.edu/faculty-and-research/faculty-directory"
        
    #TODO: Remove this when database in place
    _info_filename = "results/lebow.txt"

    def refresh(self, database):
        #TODO: Remove this when database in place
        database = open (self._info_filename, 'w')

        webpage = requests.get(self._link)
        try:
            webpage.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        soup = BeautifulSoup(webpage.text, "html.parser")

        elems = soup.findAll('div', {"class" : "user-profile-stub clearfix"})
        for i in range(0, len(elems)):
            e = elems[i]
            all_text = e.findAll(text=True)
            data = list(filter(lambda a: a != "\n", all_text))
            nameEdu = data[0].split(',', 1)

            prof = DatabaseRow()

            prof.name = nameEdu[0]
            if len(nameEdu) > 1:
                prof.education = nameEdu[1]
            prof.title = data[1]
            prof.department = data[2]
            prof.room = data[4]
            prof.phone = data[6]
            prof.email = data[8]
            if "Areas of Expertise" in data:
                aoe = data.index("Areas of Expertise")
                prof.interests = ", ".join(data[aoe+1:])

            prof.store(database)
    
        #TODO: Remove this when database in place
        database.close()

