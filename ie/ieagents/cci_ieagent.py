"""
Implementation of the IEAgent interface for the CCI faculty website 
located here: http://drexel.edu/cci/contact/Faculty/
"""

__all__ = ['CCIIEAgent']
__version__ = '0.1'
__author__ = 'Tom Amon'

import requests
from bs4 import BeautifulSoup
import abc
from .ieagent import IEAgent

class CCIIEAgent(IEAgent):

	_link = "http://drexel.edu/cci/contact/Faculty/"
	_webpage_filename = "results\cci.html"
	_info_filename = "results\cci.txt"

	def refresh(self, database):
		webpage = requests.get(self._link)

		try:
		    webpage.raise_for_status()
		except Exception as exc:
		    print('There was a problem: %s' % (exc))

		soup = BeautifulSoup(webpage.text, "html.parser")

		webpage_file = open (self._webpage_filename, 'w')
		webpage_file.write(soup.prettify())
		webpage_file.close()

		info_file = open (self._info_filename, 'w')
		elems = soup.select('tr')
		for i in range(1, len(elems)):
			data = elems[i].select('div')
			for d in data:
				info_file.write(d.getText())

		info_file.close()
