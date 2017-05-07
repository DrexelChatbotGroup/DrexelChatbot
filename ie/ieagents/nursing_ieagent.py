"""
Implementation of the IEAgent interface for the College of Nursing and Health Professions,
located here: 
"""

__all__ = ['NursingIEAgent']
__version__ = '0.1'
__author__ = 'Tom Amon'

import requests
from bs4 import BeautifulSoup
import abc
from .ieagent import IEAgent, writeHTMLFile
import ttl


class NursingIEAgent(IEAgent):

    _flink = "http://drexel.edu"
    _link = "http://drexel.edu/cnhp/faculty/profiles/"
    ttl_filename = "ttl/nursing.ttl"

    def write_ttl(self):
        ttl_file = ttl.TtlFile(self.ttl_filename)

        webpage = requests.get(self._link)
        try:
            webpage.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        soup = BeautifulSoup(webpage.text, "html.parser")

        elems = soup.findAll('tr', {"class" : "FacultyTableRow"})
        for i in range(0, len(elems)):
            data = elems[i]
            pic_a_href = data.select('img')[0]['src']
            a_href = data.select('a')[0]['href']
            pic_link = self._flink + pic_a_href
            prof_link = self._flink + a_href

            prof = self._parse_prof_site(prof_link) 
            prof.picture = pic_link
            prof.website = prof_link
            prof.write_to(ttl_file)
    
        ttl_file.close()
        return ttl_file

    def _parse_prof_site(self, website):
        webpage = requests.get(website)
        try:
            webpage.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        soup = BeautifulSoup(webpage.text, "html.parser")

        prof_div = soup.find('div', {"class" : "faculty-profile"})
        data = prof_div.getText().strip().split("\n")

        name = data[0]
        education = data[1]
        title = data[2]
        department = data[4]

        if data[6] and data[7]:
            phone = data[6] + "; " + data[7]
        elif data[6]:
            phone = data[6]
        elif data[7]:
            phone = data[7]
        else:
            phone = ""

        email = data[8]
        room = data[9]

        bio = ""
        if data[12]:
            bio = data[12]
        elif data[13]:
            bio = data[13]
        elif data[14]:
            bio = data[14]
        else:
            for j in range(0, len(data)):
                print(str(j) + ":" + data[j])


        interests = ""
        if(len(data) > 14):
            for d in data[14:]:
                if d.startswith("Research Interests"):
                    interests = d.split(":")[1]

        prof = ttl.TtlFileEntry()
        prof.property = "faculty"
        prof.name = name
        prof.education = education 
        prof.title = title
        prof.department = department
        prof.email = email
        prof.room = room 
        prof.phone = phone
        prof.bio = bio
        prof.interests = interests

        return prof
