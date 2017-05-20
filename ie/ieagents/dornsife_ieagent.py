"""
Implementation of the IEAgent interface for the school of public health,
located here: http://drexel.edu/cci/contact/Faculty/
"""

__all__ = ['HsmIEAgent']
__version__ = '0.2'
__author__ = 'Tom Amon'

import requests
from bs4 import BeautifulSoup
import abc
from .ieagent import IEAgent, writeHTMLFile
import ttl


class DornsifeIEAgent(IEAgent):

    _flink = "http://drexel.edu/"
    _link = "http://drexel.edu/dornsife/academics/faculty/"
    ttl_filename = "ttl/dornsife.ttl"

    def write_ttl(self):
        ttl_file = ttl.TtlFile(self.ttl_filename)

        webpage = requests.get(self._link)
        try:
            webpage.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        soup = BeautifulSoup(webpage.text, "html.parser")

        elems = soup.find('tbody').select('tr')
        for i in range(0, len(elems)):
            data = elems[i].select('td')

            img = data[0].find('img')
            picture = ""
            if img:
                img_src = data[0].find('img')['src']
                picture = self._flink + img_src

            info = data[1].getText().split("\n")
            name = info[1].split(',')[0]
            title = info[2]
            phone = info[3]
            email = info[4]

            department = data[2].getText()
            
            prof = ttl.TtlFileEntry()
            prof.name = name
            prof.property = "faculty"
            prof.picture = picture
            prof.title = title
            prof.phone = phone
            prof.email = email
            prof.department = department
            prof.write_to(ttl_file)

        ttl_file.close()
        return ttl_file
