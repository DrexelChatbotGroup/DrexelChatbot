"""
Implementation of the IEAgent interface for the College of Arts and Sciences
faculty, located here: http://drexel.edu/coas/faculty-research/faculty-directory/

Data is stored in an html table, with each person have a single row(tr).
The data is stored in a complex way, with many nested div's and paragraphs.
However, they use a consistent class naming scheme, which allows for searching
for the data by class name. 
The basic order of the data is:
Picture
Name
Degree
Title
Office
Phone
Bio
Department

"""

__all__ = ['CoasIEAgent']
__version__ = '0.1'
__author__ = 'Tom Amon'

import requests
from bs4 import BeautifulSoup
import abc
from .ieagent import IEAgent
import ttl


class CoasIEAgent(IEAgent):
    _link = "http://drexel.edu/coas/faculty-research/faculty-directory/"
    _ttl_filename = "ttl/coas.ttl"

    def write_ttl(self):
        ttl_file = ttl.TtlFile(self._ttl_filename)

        webpage = requests.get(self._link)
        try:
            webpage.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        soup = BeautifulSoup(webpage.text, "html.parser")

        elems = soup.findAll('tr', {"class" : "FacultyTableRow"})
        for i in range(0, len(elems)):
            data = elems[i]
            div_facultyHeadshot = data.find('div', {"class" : "facultyHeadshot"})
            image = div_facultyHeadshot.img
            div_fac_info = data.find('div', {"class" : "fac-info"})
            h2_fname = div_fac_info.find('h2', {"class" : "fname"})
            h2_fname_list = h2_fname.getText().split(",", 1)
            div_fcontact = div_fac_info.find('div', {"class" : "fcontact"})
            location_text = div_fcontact.contents[3].getText()
            location_list = location_text.split("\n")

            prof = ttl.TtlFileEntry()

            if image is not None:
                prof.picture = "http://drexel.edu" + image['src']
            prof.name = h2_fname_list[0]
            prof.property = "faculty"
            if len(h2_fname_list) > 1:
                prof.degree = h2_fname_list[1]
            prof.title = div_fcontact.contents[1].getText()
            prof.office = location_list[0]
            prof.email = location_list[1]
            prof.phone = location_list[2]
            prof.department = data.find_all('td')[1].next_element
            
            prof.write_to(ttl_file)
    
        ttl_file.close()
        return ttl_file
