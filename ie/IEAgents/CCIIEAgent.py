import requests
from bs4 import BeautifulSoup
import abc
from .IEAgent import IEAgent

class CCIIEAgent(IEAgent):

	def refresh(self):
		link = "http://drexel.edu/cci/contact/Faculty/"
		webpage_filename = "results\cci.html"
		info_filename = "results\cci.txt"
		webpage = requests.get(link)

		try:
		    webpage.raise_for_status()
		except Exception as exc:
		    print('There was a problem: %s' % (exc))

		soup = BeautifulSoup(webpage.text, "html.parser")

		webpage_file = open (webpage_filename, 'w')
		webpage_file.write(soup.prettify())
		webpage_file.close()

		info_file = open (info_filename, 'w')
		elems = soup.select('tr')
		for i in range(1, len(elems)):
			data = elems[i].select('div')
			for d in data:
				info_file.write(d.getText())

		info_file.close()

if __name__ == "__main__":
	iea = CCIIEAgent()
	iea.refresh()