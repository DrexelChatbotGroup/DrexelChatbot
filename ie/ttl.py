
"""
Provides classes to more easily write the ttl files used by the database. 
"""

__all__ = ["TtlFile", "TtlFileEntry"]
__version__ = '0.1'
__author__ = 'Tom Amon'


class TtlFile:

    def __init__(self, filename):
        self.filename = filename
        self._f = open (self.filename, 'w')
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
        name = self.name.split()
        entry  = "<#%s-%s>\n" % (name[0], name[1])
        entry += '    cb:name "%s" ; \n' % self.name
        entry += '    cb:property "%s" ; \n' % self.prop
        entry += '    cb:title "%s" ; \n' % self.title
        entry += '    cb:department "%s" ; \n' % self.department
        entry += '    cb:address "%s" ; \n' % self.address
        entry += '    cb:startTime "%s" ; \n' % self.startTime
        entry += '    cb:endTime "%s" ; \n' % self.endTime
        entry += '    cb:education "%s" ; \n' % self.education
        entry += '    cb:email "%s" ; \n' % self.email
        entry += '    cb:website "%s" ; \n' % self.website
        entry += '    cb:picture "%s" ; \n' % self.picture
        entry += '    cb:publications "%s" ; \n' % self.publications
        entry += '    cb:phone "%s" ; \n' % self.phone
        entry += '    cb:interests "%s" ; \n' % self.interests

        #remove the last few characters and replace with a .
        entry = entry[:-3]
        entry += '.\n\n'
        ttlFile.write(entry)


def _fix(string):
    return " ".join(string.strip(' \t\n\r,').split())
