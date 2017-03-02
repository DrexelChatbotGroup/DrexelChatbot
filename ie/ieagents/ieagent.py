"""
Contains the interface for all classes that will get data from a single website.
Also contains a data structure that can be used by those classes to store the data. 
"""

__all__ = ['IEAgent']
__version__ = '0.1'
__author__ = 'Tom Amon'

import abc

class IEAgent(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def refresh(self, database):
        """refresh the database"""
        return


class DatabaseRow(object):

    def __init__(self):
        self.name = ""
        self.prop = ""
        self.title = ""
        self.department = ""
        self.address = ""
        self.room = ""
        self.startTime = ""
        self.endTime = ""
        self.education = ""
        self.email = ""
        self.website = ""
        self.picture = ""
        self.publications = ""
        self.phone = ""
        self.interests = ""

    def _fixStrings(self):
        self.name = _fixStr(self.name)
        self.prop = _fixStr(self.prop)
        self.title = _fixStr(self.title)
        self.department = _fixStr(self.department)
        self.address = _fixStr(self.address)
        self.room = _fixStr(self.room)
        self.startTime = _fixStr(self.startTime)
        self.endTime = _fixStr(self.endTime)
        self.education = _fixStr(self.education)
        self.email = _fixStr(self.email)
        self.website = _fixStr(self.website)
        self.picture = _fixStr(self.picture)
        self.publications = _fixStr(self.publications)
        self.phone = _fixStr(self.phone)
        self.interests = _fixStr(self.interests)

    def store(self, database):
        self._fixStrings()
        #TODO: Repalce will calls to store info in database
        database.write("Name: %s\n" % self.name)
        database.write("Property: %s\n" % self.prop)
        database.write("Title:  %s\n" % self.title)
        database.write("Department: %s\n" % self.department)
        database.write("Address: %s\n" % self.address)
        database.write("Room: %s\n" % self.room)
        database.write("Start time: %s\n" % self.startTime)
        database.write("End time: %s\n" % self.endTime)
        database.write("Education: %s\n" % self.education)
        database.write("Email:  %s\n" % self.email)
        database.write("Website:  %s\n" % self.website)
        database.write("Picture: %s\n" % self.picture)
        database.write("Publications:  %s\n" % self.publications)
        database.write("Phone:  %s\n" % self.phone)
        database.write("Interests:  %s\n" % self.phone)
        database.write("\n\n")


def _fixStr(string):
    return " ".join(string.strip(' \t\n\r,').split())
