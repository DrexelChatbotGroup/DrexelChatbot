"""
Implementation of the IEAgent interface for the School of education
located here: http://drexel.edu/soe/faculty-and-staff/faculty/
"""

__all__ = ['SoeIEAgent']
__version__ = '0.1'
__author__ = 'Tom Amon'

import requests
from bs4 import BeautifulSoup
import abc
from .ieagent import IEAgent, writeHTMLFile
import ttl

class SoeIEAgent(IEAgent):

    _flink = "http://drexel.edu"
    _link = "http://drexel.edu/soe/faculty-and-staff/faculty/"
    ttl_filename = "ttl/soe.ttl"

    def write_ttl(self):
        ttl_file = ttl.TtlFile(self.ttl_filename)

        webpage = requests.get(self._link)
        try:
            webpage.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        soup = BeautifulSoup(webpage.text, "html.parser")

        elems = soup.findAll('div', {"class" : "faculty-container"})
        for i in range(0, len(elems)):
            data = elems[i]
            a = data.find('a')
            if a is None:
                continue
            a_href = a['href']
            prof_link = self._flink + a_href

            prof = self._parse_prof_site(prof_link) 
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

        header = soup.find("div", {"class" : "profile-header"})

        img_src = header.find("img")["src"]
        picture = self._flink + img_src

        faculty_txt_div = header.find("div", {"class" : "faculty-txt"})
        info = faculty_txt_div.select("li")
        room = info[0].getText()
        phone = info[1].getText()
        email = info[2].getText()

        name_div = header.find("div", {"class" : "faculty-name"})
        name = name_div.getText().split(",")[0]
        
        edu_div = header.find("div", {"class" : "faculty-edu"})
        next_sib = edu_div.find("h2").next_sibling
        education = "" 
        while next_sib != None:
            if '<br/>' not in str(next_sib):
                education += str(next_sib) + "; "
            next_sib = next_sib.next_sibling

        prof = ttl.TtlFileEntry()
        prof.property = "faculty"
        prof.website = website
        prof.picture = picture
        prof.room = room 
        prof.phone = phone 
        prof.email = email 
        prof.name = name
        prof.education = education 

        return prof
