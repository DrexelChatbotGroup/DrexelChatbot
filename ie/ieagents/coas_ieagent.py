"""
Implementation of the IEAgent interface for the CCI faculty website 
located here: http://drexel.edu/coas/faculty-research/faculty-directory/

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

__all__ = ['CCIIEAgent']
__version__ = '0.1'
__author__ = 'Tom Amon'

import requests
from bs4 import BeautifulSoup
import abc
from .ieagent import IEAgent


class CoasIEAgent(IEAgent):
    _link = "http://drexel.edu/coas/faculty-research/faculty-directory/"
        
    #TODO: Remove this when database in place
    _info_filename = "results/coas.txt"

    def refresh(self, database):
        #TODO: Remove this when database in place
        database = open (self._info_filename, 'w')

        webpage = requests.get(self._link)
        try:
            webpage.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        soup = BeautifulSoup(webpage.text, "html.parser")

        #elems = soup.select('tr')
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

            prof = _CoasProfessor()
            if image is not None:
                prof.picture = "http://drexel.edu" + image['src'].strip(' \t\n\r')
            prof.name = h2_fname_list[0].strip(' \t\n\r')
            if len(h2_fname_list) > 1:
                prof.degree = h2_fname_list[1].strip(' \t\n\r')
            prof.title = div_fcontact.contents[1].getText().strip(' \t\n\r')
            prof.office = location_list[0].strip(' \t\n\r')
            prof.email = location_list[1].strip(' \t\n\r')
            prof.phone = location_list[2].strip(' \t\n\r')
            prof.department = data.find_all('td')[1].getText().strip(' \t\n\r')
            
            prof.store(database)
    
        #TODO: Remove this when database in place
        database.close()


class _CoasProfessor():
    picture = ""
    name = ""
    degree = ""
    title = ""
    office = ""
    email = ""
    phone = ""
    department = ""

    def store(self, database):
        #TODO: Repalce will calls to store info in database
        database.write("Picture: %s\n" % self.picture)
        database.write("Name: %s\n" % self.name)
        database.write("Degree: %s\n" % self.degree)
        database.write("Title:  %s\n" % self.title)
        database.write("Office:  %s\n" % self.office)
        database.write("Email:  %s\n" % self.email)
        database.write("Phone:  %s\n" % self.phone)
        database.write("Department:  %s\n" % self.department)
        database.write("\n\n")


