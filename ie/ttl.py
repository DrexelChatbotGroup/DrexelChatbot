
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
        self.property = ""
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
        self.property = _fix(self.property)
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
        if self.name:
        	entry += '    cb:name "%s" ; \n' % self.name
        if self.property:
        	entry += '    cb:property "%s" ; \n' % self.property
        if self.title:
        	entry += '    cb:title "%s" ; \n' % self.title
        if self.department:
        	entry += '    cb:department "%s" ; \n' % self.department
        if self.address:
   		    entry += '    cb:address "%s" ; \n' % self.address
        if self.room:
            entry += '    cb:room "%s" ; \n' %self.room
        if self.startTime:
	        entry += '    cb:startTime "%s" ; \n' % self.startTime
        if self.endTime:
	        entry += '    cb:endTime "%s" ; \n' % self.endTime
        if self.education:
	        entry += '    cb:education "%s" ; \n' % self.education
        if self.email:
	        entry += '    cb:email "%s" ; \n' % self.email
        if self.website:
	        entry += '    cb:website "%s" ; \n' % self.website
        if self.picture:
	        entry += '    cb:picture "%s" ; \n' % self.picture
        if self.publications:
	        entry += '    cb:publications "%s" ; \n' % self.publications
        if self.phone:
	        entry += '    cb:phone "%s" ; \n' % self.phone
        if self.interests:
	        entry += '    cb:interests "%s" ; \n' % self.interests

        #remove the last "; \n  and replace with a .
        entry = entry[:-3]
        entry += '.\n\n'
        ttlFile.write(entry)


def _fix(string):
    return " ".join(string.strip(' \t\n\r,').split())
