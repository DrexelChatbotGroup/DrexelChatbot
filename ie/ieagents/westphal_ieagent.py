"""
Implementation of the IEAgent interface for the College of Media Arts & Design faculty website, located here:
http://www.drexel.edu/westphal/about/directory/

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

__all__ = ['WestphalIEAgent']
__version__ = '0.1'
__author__ = 'Nanxi Zhang'

import requests
from bs4 import BeautifulSoup
import abc
from .ieagent import IEAgent, writeHTMLFile
import ttl

    
class WestphalIEAgent(IEAgent):

    _link = "http://www.drexel.edu/westphal/about/directory/"
    _flink = "http://www.drexel.edu"
    ttl_filename = "ttl/westphal.ttl"

    def write_ttl(self):
        ttl_file = ttl.TtlFile(self.ttl_filename)

        webpage = requests.get(self._link)
        try:
            webpage.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        soup = BeautifulSoup(webpage.text, "html.parser")
        
        
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
                if titleStr:
                    prof.title = titleStr
                prof.phone = phoneStr
                prof.email = emailStr
                prof.website = websiteStr
                prof.room = officeStr
                
                prof.write_to(ttl_file)
        
        ttl_file.close()
        return ttl_file
