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
    name = ""
    prop = ""
    title = ""
    department = ""
    address = ""
    room = ""
    startTime = ""
    endTime = ""
    education = ""
    email = ""
    website = ""
    picture = ""
    publications = ""
    phone = ""
    interests = ""

    def store(self, database):
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
