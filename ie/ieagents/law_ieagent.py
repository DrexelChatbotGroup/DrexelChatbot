"""
Implementation of the IEAgent interface for the School of Law,
located here: http://drexel.edu/law/faculty/fulltime_fac/

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

__all__ = ['LawIEAgent']
__version__ = '0.2'
__author__ = 'Tom Amon'

import requests
from bs4 import BeautifulSoup
import abc
from .ieagent import IEAgent, writeHTMLFile
import ttl


class LawIEAgent(IEAgent):

    _flink = "http://drexel.edu"
    _link = "http://drexel.edu/law/faculty/fulltime_fac/"
    ttl_filename = "ttl/law.ttl"

    def write_ttl(self):
        ttl_file = ttl.TtlFile(self.ttl_filename)

        webpage = requests.get(self._link)
        try:
            webpage.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        soup = BeautifulSoup(webpage.text, "html.parser")

        fac_list = soup.find('div', {"class" : "datasetrenderer faculty-list"})
        elems = fac_list.findAll('div', {"class" : "info"})
        pics = fac_list.findAll('div', {"class" : "headshot no-scale"})
        for i in range(0, len(elems)):
            data = elems[i]
            pic_a_href = pics[i].select('img')[0]['src']
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
        name = prof_div.getText()
        h2_list = soup.findAll('h2')
        title1 = h2_list[0].getText()
        title2 = h2_list[1].getText()
        if title1 and title2:
            title = title1 + "; " + title2
        elif title1:
            title = title1 
        elif title2:
            title = title2
        grey_box = soup.find('div', {"class" : "grey-box"})
        a_href = grey_box.select('a')[0]['href']
        email = a_href.split(':')[1]
        text_list = (grey_box.getText().split('\n'))
        office = text_list[2].split(':')[1]
        phone = text_list[4].split(':')[1]
        
        prof = ttl.TtlFileEntry()
        prof.property = "faculty"
        prof.name = name
        prof.title = title
        prof.email = email
        prof.room = office
        prof.phone = phone

        return prof
