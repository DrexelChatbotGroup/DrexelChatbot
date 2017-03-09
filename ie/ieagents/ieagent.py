"""
Contains the interface for all classes that will get data from a single website.
Also contains a data structure that can be used by those classes to store the data. 
"""

__all__ = ['IEAgent']
__version__ = '0.2'
__author__ = 'Tom Amon'

import abc

class IEAgent(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def write_ttl(self):
        """Writes a ttl file containing all the data from this source"""
        return

def writeHTMLFile(soup, filename):
    webpage_file = open (filename, 'w')
    webpage_file.write(soup.prettify())
    webpage_file.close()
    
