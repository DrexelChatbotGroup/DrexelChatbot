
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
        self.education = ""
        self.email = ""
        self.website = ""
        self.picture = ""
        self.publications = ""
        self.phone = ""
        self.interests = ""
        self.bio = ""
        self.mStartTime = ""
        self.tStartTime = ""
        self.wStartTime = ""
        self.thStartTime = ""
        self.fStartTime = ""
        self.saStartTime = ""
        self.suStartTime = ""
        self.mEndTime = ""
        self.tEndTime = ""
        self.wEndTime = ""
        self.thEndTime = ""
        self.fEndTime = ""
        self.saEndTime = ""
        self.suEndTime = ""
        self.altnames = [] 

    def _fix_strings(self):
        self.name = _fix(self.name)
        self.property = _fix(self.property)
        self.title = _fix(self.title)
        self.department = _fix(self.department)
        self.address = _fix(self.address)
        self.room = _fix(self.room)
        self.education = _fix(self.education)
        self.email = _fix(self.email)
        self.website = _fix(self.website)
        self.picture = _fix(self.picture)
        self.publications = _fix(self.publications)
        self.phone = _fix(self.phone)
        self.interests = _fix(self.interests)
        self.bio = _fix(self.bio)
        fixednames = []
        for name in self.altnames:
            fixedname = _fix(name) 
            fixednames.append(fixedname)
        self.altnames = fixednames
        self.mStartTime = _fix(self.mStartTime)
        self.tStartTime = _fix(self.mStartTime)
        self.wStartTime = _fix(self.mStartTime)
        self.thtartTime = _fix(self.mStartTime)
        self.fStartTime = _fix(self.mStartTime)
        self.saStartTime = _fix(self.mStartTime)
        self.suStartTime = _fix(self.mStartTime)
        self.mEndTime = _fix(self.mEndTime)
        self.tEndTime = _fix(self.mEndTime)
        self.wEndTime = _fix(self.mEndTime)
        self.thEndTime = _fix(self.mEndTime)
        self.fEndTime = _fix(self.mEndTime)
        self.saEndTime = _fix(self.mEndTime)
        self.suEndTime = _fix(self.mEndTime)

    def write_to(self, ttlFile):
        self._fix_strings()
        name = self.name.split()
        firstname = name[0]
        lastname = name[len(name)-1]
        entry  = "<#%s-%s>\n" % (firstname, lastname)
        if self.name:
            entry += '    cb:name "%s" ; \n' % self.name
            if self.property == "faculty":
                entry += '    cb:name "%s" ; \n' % lastname
        if self.altnames:
            for name in self.altnames:
                entry += '    cb:name "%s" ; \n' % name
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
        if self.bio:
            entry += '    cb:bio "%s" ; \n' % self.bio
        if self.mStartTime:
            entry += '    cb:mStartTime "%s" ; \n' % self.mStartTime
        if self.tStartTime:
            entry += '    cb:tStartTime "%s" ; \n' % self.tStartTime
        if self.wStartTime:
            entry += '    cb:wStartTime "%s" ; \n' % self.wStartTime
        if self.thStartTime:
            entry += '    cb:thStartTime "%s" ; \n' % self.thStartTime
        if self.fStartTime:
            entry += '    cb:fStartTime "%s" ; \n' % self.fStartTime
        if self.saStartTime:
            entry += '    cb:saStartTime "%s" ; \n' % self.saStartTime
        if self.suStartTime:
            entry += '    cb:suStartTime "%s" ; \n' % self.suStartTime
        if self.mEndTime:
            entry += '    cb:mEndTime "%s" ; \n' % self.mEndTime
        if self.tEndTime:
            entry += '    cb:tEndTime "%s" ; \n' % self.tEndTime
        if self.wEndTime:
            entry += '    cb:wEndTime "%s" ; \n' % self.wEndTime
        if self.thEndTime:
            entry += '    cb:thEndTime "%s" ; \n' % self.thEndTime
        if self.fEndTime:
            entry += '    cb:fEndTime "%s" ; \n' % self.fEndTime
        if self.saEndTime:
            entry += '    cb:saEndTime "%s" ; \n' % self.saEndTime
        if self.suEndTime:
            entry += '    cb:suEndTime "%s" ; \n' % self.suEndTime

        #remove the last "; \n  and replace with a .
        entry = entry[:-3]
        entry += '.\n\n'
        ttlFile.write(entry)


def _fix(string):
    return " ".join(string.strip(' \t\n\r,').split()).replace("\"", "\\\"")
