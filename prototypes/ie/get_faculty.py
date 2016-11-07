import requests
from bs4 import BeautifulSoup

link = "http://drexel.edu/cci/contact/Faculty/"
webpage_filename = "test.html"
webpage = requests.get(link)
info_filename = "teacher_info.txt"

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