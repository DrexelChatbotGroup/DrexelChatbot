"""
Implementation of the IEAgent interface for the CCI faculty website 
located here: http://drexel.edu/cci/contact/Faculty/

Data stored in a html table, with each person have a single row(tr).
The data, very conviently, all in their own div. So just going through each
div of the row should get all the data. The data is in the order:
Name
Title
Department
Interests
Email
Phone
Office

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
	# _webpage_filename = "results/cci.html"
	_info_filename = "results/cci.txt"

	def refresh(self, database):
		webpage = requests.get(self._link)

		try:
		    webpage.raise_for_status()
		except Exception as exc:
		    print('There was a problem: %s' % (exc))

		soup = BeautifulSoup(webpage.text, "html.parser")

		# writes a html file, for debugging purposes
		# webpage_file = open (self._webpage_filename, 'w')
		# webpage_file.write(soup.prettify())
		# webpage_file.close()

		info_file = open (self._info_filename, 'w')
		elems = soup.select('tr')
		for i in range(1, len(elems)):
			data = elems[i].select('div')
			prof = _CCI_Professor()
			prof.name = data[1].getText().strip(' \t\n\r')
			prof.title = data[2].getText().strip(' \t\n\r')
			prof.department = data[3].getText().strip(' \t\n\r')
			prof.interests = data[4].getText().strip(' \t\n\r').split(':')[1]
			prof.email = data[5].getText().strip(' \t\n\r').split(":")[1]
			if data[6].getText().strip(' \t\n\r'):
				prof.phone = data[6].getText().strip(' \t\n\r').split(":")[1]
			if data[7].getText().strip(' \t\n\r'):
				prof.office = data[7].getText().strip(' \t\n\r').split(":")[1]
			prof.store(info_file)

		info_file.close()


class _CCI_Professor():
	name = ""
	title = ""
	department = ""
	interests = ""
	email = ""
	phone = ""
	office = ""

	def store(self, database):
		database.write("Name: %s\n" % self.name)
		database.write("Title:  %s\n" % self.title)
		database.write("Department:  %s\n" % self.department)
		database.write("Interests:  %s\n" % self.interests)
		database.write("Email:  %s\n" % self.email)
		database.write("Phone:  %s\n" % self.phone)
		database.write("Office:  %s\n" % self.office)
		database.write("\n\n")
