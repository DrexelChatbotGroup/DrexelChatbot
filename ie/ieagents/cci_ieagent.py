"""
Implementation of the IEAgent interface for the College of computing and
infomatics faculty website, located here: http://drexel.edu/cci/contact/Faculty/

Data is stored in an html table, with each person have a single row(tr).
The data, very conviently, is all in their own div. So just going through 
each div of the row should everything. The data is in the order:
Name
Title
Department
Interests
Email
Phone
Room

"""

__all__ = ['CciIEAgent']
__version__ = '0.2'
__author__ = 'Tom Amon'

import requests
from bs4 import BeautifulSoup
import abc
from .ieagent import IEAgent
import ttl


class CciIEAgent(IEAgent):

    _flink = "http://drexel.edu/"
    _link = "http://drexel.edu/cci/contact/Faculty/"
    ttl_filename = "ttl/cci.ttl"

    def write_ttl(self):
        ttl_file = ttl.TtlFile(self.ttl_filename)

        webpage = requests.get(self._link)
        try:
            webpage.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        soup = BeautifulSoup(webpage.text, "html.parser")

        elems = soup.select('tr')
        for i in range(1, len(elems)):
            data = elems[i].select('div')
            img_src = data[0].select('img')[0]['src']
            a_href = data[1].select('a')[0]['href']
            prof_link = self._flink + a_href
            data = list(map(lambda x: x.getText(), data))

            print(data[1])
            prof = self._parse_prof_site(prof_link) 
            prof.picture = self._flink + img_src
            prof.name = data[1]
            prof.property = "faculty"
            prof.title = data[2]
            prof.department = data[3]
            prof.interests = data[4].split(':')[1]
            prof.email = data[5].split(":")[1]
            if not data[6].isspace():
                prof.phone = data[6].split(":")[1]
            if not data[7].isspace():
                prof.room = data[7].split(":")[1]

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

        center_rail = soup.find('div', {"id" : "center-rail"})
        divs = center_rail.findAll('div')
        bio_block = divs[3]
        edu_block = divs[4].find("ul")
        #if that isnt the block, the next is 
        if not edu_block:
            edu_block = divs[5].find("ul")
        educations = edu_block.findAll("li")
        edu_str = ""
        for e in educations:
            edu_str += e.getText() + ". \n"

        pub_str = ""
        if len(divs) > 6:
            pub_block = divs[6].find("ul")
            #if that isnt the block, either the next is or this professor doesn't have one
            if not pub_block and len(divs) > 7:
                pub_block = divs[7].find("ul")
            if pub_block:
                publications = pub_block.findAll("li")
                pub_number = 3
                count = 0
                for p in publications:
                    pub_str += p.getText() + ". \n"
                    count+=1
                    if count == pub_number:
                        break

        website_block = soup.find("div", {"id" : "bodytag_2_rightrail_0_pnlSite"})
        website_str = ""
        if website_block:
            website_str = website_block.select("a")[0].getText()

        prof = ttl.TtlFileEntry()
        prof.bio = bio_block.getText()
        prof.education = edu_str
        prof.publications = pub_str
        prof.website = website_str 

        return prof
