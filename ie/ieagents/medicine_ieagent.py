"""
Implementation of the IEAgent interface for the College of Medicine
located here: http://drexel.edu/medicine/faculty/profiles/
"""

__all__ = ['MedicineIEAgent']
__version__ = '0.1'
__author__ = 'Tom Amon'

import requests
from bs4 import BeautifulSoup
import abc
from .ieagent import IEAgent, writeHTMLFile
import ttl


class MedicineIEAgent(IEAgent):

    _flink = "http://drexel.edu"
    _link = "http://drexel.edu/medicine/faculty/profiles/"
    ttl_filename = "ttl/medicine.ttl"

    def write_ttl(self):
        ttl_file = ttl.TtlFile(self.ttl_filename)

        webpage = requests.get(self._link)
        try:
            webpage.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        soup = BeautifulSoup(webpage.text, "html.parser")

        elems = soup.findAll('h3', {"class" : "profile-name"})
        for i in range(0, len(elems)):
            data = elems[i]
            a_href = data.select('a')[0]['href']
            prof_link = self._flink + a_href
            name = data.getText()

            prof = self._parse_prof_site(prof_link) 
            prof.name = name
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

        prof_div = soup.find('div', {"class" : "profile-col1"})
        img = prof_div.select('img')
        picture = ""
        if img:
            img_src = img[0]['src']
            picture = self._flink + img_src
        name = prof_div.select('h1')[0].getText()
        title = prof_div.select('h2')[0].getText()

        department = ''
        department_p = prof_div.find("p", {"id" : "bodytag_2_centerrail_0_pDepartment"})
        if department_p:
            department = department_p.getText().split(":")[1]

        bio = ''
        bio_div = prof_div.find("div", {"id" : "bodytag_2_centerrail_0_divPatientCareBio"})
        if bio_div:
            bio_p = bio_div.select("p")
            if bio_p:
                bio = bio_p[0].getText()
            else:
                bio = bio_div.getText()

        interests = ''
        interests_div = prof_div.find("div", {"id" : "bodytag_2_centerrail_0_divResearchOverviewText"})
        if interests_div:
            interests = interests_div.getText()

        education = ''
        education_div = prof_div.find("ul", {"id" : "bodytag_2_centerrail_0_ulEducation"})
        if education_div:
            for e in education_div:
                if education:
                    education = education + "; " + e.getText()
                else:
                    education = e.getText()

        email = "" 
        room = ""
        phone = ""
        grey_box = soup.find('div', {"class" : "grey-box"})
        if grey_box:
            a = grey_box.select('a')
            if a:
                a_href = a[0]['href']
                email = a_href.split(":")[1]

            grey_box_br = grey_box.select('br')
            grey_box_text = list(map(lambda x: x.getText(), grey_box_br))
            for j in range(0, len(grey_box_text) - 1):
                g = grey_box_text[j]
                g_next = grey_box_text[j + 1]
                grey_box_text[j] = g[:-len(g_next)]

            phone_index = -1
            for j in range(0, len(grey_box_text)):
                e = grey_box_text[j]
                if e.startswith("Phone"):
                    phone_index = j
                    break

            for e in grey_box_text[:phone_index]:
                if room:
                    room += ", " +  e
                else:
                    room = e

            if phone_index != -1:
                phone = grey_box_text[phone_index].split(":")[1]

        prof = ttl.TtlFileEntry()
        prof.property = "faculty"
        prof.picture = picture
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
