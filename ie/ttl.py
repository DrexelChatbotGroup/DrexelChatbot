
"""
Provides classes to more easily write the ttl files used by the database. 
"""

__all__ = ["TtlFile", "TtlFileEntry"]
__version__ = '0.1'
__author__ = 'Tom Amon'


class TtlFile:

    def __init__(self, filename):
        self._filename = filename
        self._f = open (self._filename, 'w')
        self._write_header()
    
    def __del__(self):
        self._f.close()

    def _write_header(self):
        header1 = "@base <http://drexelchatbot.com/rdf/> ."
        header2 = "@prefix cb: <http://drexelchatbot.com/rdf/> ."
        self._f.write("%s\n%s\n\n" % (header1, header2))

    def write(self, string):
        self._f.write(string)

    def close(self):
        self._f.close()


class TtlFileEntry:

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

    def _fix_strings(self):
        self.name = _fix(self.name)
        self.prop = _fix(self.prop)
        self.title = _fix(self.title)
        self.department = _fix(self.department)
        self.address = _fix(self.address)
        self.room = _fix(self.room)
        self.startTime = _fix(self.startTime)
        self.endTime = _fix(self.endTime)
        self.education = _fix(self.education)
        self.email = _fix(self.email)
        self.website = _fix(self.website)
        self.picture = _fix(self.picture)
        self.publications = _fix(self.publications)
        self.phone = _fix(self.phone)
        self.interests = _fix(self.interests)

    def write_to(self, ttlFile):
        self._fix_strings()
        ttlFile.write("Name: %s\n" % self.name)
        ttlFile.write("Property: %s\n" % self.prop)
        ttlFile.write("Title:  %s\n" % self.title)
        ttlFile.write("Department: %s\n" % self.department)
        ttlFile.write("Address: %s\n" % self.address)
        ttlFile.write("Room: %s\n" % self.room)
        ttlFile.write("Start time: %s\n" % self.startTime)
        ttlFile.write("End time: %s\n" % self.endTime)
        ttlFile.write("Education: %s\n" % self.education)
        ttlFile.write("Email:  %s\n" % self.email)
        ttlFile.write("Website:  %s\n" % self.website)
        ttlFile.write("Picture: %s\n" % self.picture)
        ttlFile.write("Publications:  %s\n" % self.publications)
        ttlFile.write("Phone:  %s\n" % self.phone)
        ttlFile.write("Interests:  %s\n" % self.interests)
        ttlFile.write("\n\n")


def _fix(string):
    return " ".join(string.strip(' \t\n\r,').split())
