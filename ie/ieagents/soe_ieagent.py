<<<<<<< Updated upstream

"""
Implementation of the IEAgent interface for the School of education
located here: http://drexel.edu/soe/faculty-and-staff/faculty/
=======
"""
UNFINISHED
Implementation of the IEAgent interface for the School of Education faculty website, located here:
http://drexel.edu/soe/faculty-and-staff/faculty/

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

>>>>>>> Stashed changes
"""

__all__ = ['SoeIEAgent']
__version__ = '0.1'
<<<<<<< Updated upstream
__author__ = 'Tom Amon'
=======
__author__ = 'Nanxi Zhang'
>>>>>>> Stashed changes

import requests
from bs4 import BeautifulSoup
import abc
from .ieagent import IEAgent, writeHTMLFile
import ttl

<<<<<<< Updated upstream

class SoeIEAgent(IEAgent):

    _flink = "http://drexel.edu"
    _link = "http://drexel.edu/soe/faculty-and-staff/faculty/"
    ttl_filename = "ttl/soe.ttl"
=======
    
class SoeIEAgent(IEAgent):

    _link = "http://www.drexel.edu/westphal/about/directory/"
    _flink = "http://www.drexel.edu"
    ttl_filename = "ttl/westphal.ttl"
>>>>>>> Stashed changes

    def write_ttl(self):
        ttl_file = ttl.TtlFile(self.ttl_filename)

        webpage = requests.get(self._link)
        try:
            webpage.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        soup = BeautifulSoup(webpage.text, "html.parser")
<<<<<<< Updated upstream

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
=======
        
        
        elems = soup.findAll('a')
        for i in range(0, len(elems)):
            e = elems[i]
            if "/directory/" in e["href"] and e["href"] != "/westphal/about/directory/":
                #print (e["href"])
                _plink= self._flink + e["href"]
                fpage = requests.get(_plink)
                try:
                    fpage.raise_for_status()
                except Exception as exc:
                    print('There was a problem: %s' % (exc))
                fsoup = BeautifulSoup(fpage.text, "html.parser")
                
                #writeHTMLFile(fsoup, "test.html")
                
                prof = ttl.TtlFileEntry()
                
                nameStr = fsoup.find('div', {"class" : "faculty-name"}).getText()
                #print (nameStr)
                titleStr = fsoup.find('div', {"class" : "title"}).getText()
                #print (titleStr)

                contactStr = fsoup.find('div', {"class" : "contact"}).getText()
                contactList = contactStr.splitlines()
                if "PH:" in contactList[3]:
                    phoneStr = contactList[3].split(": ")[1].replace(".","")
                #print(phoneStr)
                if "Email:" in contactList[4]:
                    emailStr = contactList[4].split(": ")[1]
                #print(emailStr)
                if "Website:" in contactList[5]:
                    websiteStr = contactList[5]
                    if websiteStr.split(": ")[1]:
                        websiteStr = websiteStr.split(": ")[1]
                    else:
                        websiteStr = contactList[6].strip()
                #print (websiteStr)

                locationStr = fsoup.find('div', {"class" : "location"}).getText()
                locationList = locationStr.splitlines()
                if len(locationList) > 2 and locationList[2]:
                    officeStr = locationList[2]
                #print (officeStr)

                #infoStr = fsoup.find('div', {"id" : "tabs"}).getText()
                #print (infoStr)
                
                prof.name = nameStr.split(',', 1)[0]
                prof.property = "faculty"
                if titleStr:
                    prof.title = titleStr
                prof.phone = phoneStr
                prof.email = emailStr
                prof.website = websiteStr
                prof.room = officeStr
                
                prof.write_to(ttl_file)
        
        ttl_file.close()
        return ttl_file
>>>>>>> Stashed changes
