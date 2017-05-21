import unittest
from ie.ttl import TtlFile, TtlFileEntry
import os

class TestTtl(unittest.TestCase):
    filename = "testFile.ttl"
    ttl = None

    @classmethod
    def setUp(self):
        self.ttl = TtlFile(self.filename)

    @classmethod
    def tearDown(self):
       self.ttl.close()
       os.remove(self.filename) 

    def test_constructor_creates_file(self):
        self.assertTrue(os.path.isfile(self.ttl.filename))
    
    def test_header(self):
        self.ttl.close()
        f = open (self.filename, 'r')
        lines = f.readlines()
        self.assertTrue(lines[0].startswith("@base"))
        self.assertTrue(lines[1].startswith("@prefix"))
        self.assertTrue(lines[2].startswith("\n"))
        f.close()
    
    def test_write(self):
        testStr = "Testy test\n"
        testStr2 = "Testible testing tester!"
        self.ttl.write(testStr)
        self.ttl.write(testStr2)
        self.ttl.close()

        f = open (self.filename, 'r')
        lines = f.readlines()
        self.assertEqual(lines[3], testStr)
        self.assertEqual(lines[4], testStr2)
        f.close()

    def test_file_entry(self):
        ttl_fe = TtlFileEntry()
        ttl_fe.name = "name"
        ttl_fe.property = "property"
        ttl_fe.title = "title"
        ttl_fe.department = "department"
        ttl_fe.address = "address"
        ttl_fe.room = "room"
        ttl_fe.education = "education"
        ttl_fe.email = "email"
        ttl_fe.website = "website"
        ttl_fe.picture = "picture"
        ttl_fe.publications = "publications"
        ttl_fe.phone = "phone"
        ttl_fe.interests = "interests"
        ttl_fe.bio = "bio"
        ttl_fe.mStartTime = "mStartTime"
        ttl_fe.tStartTime = "tStartTime"
        ttl_fe.wStartTime = "wStartTime"
        ttl_fe.thStartTime = "thStartTime"
        ttl_fe.fStartTime = "fStartTime"
        ttl_fe.saStartTime = "saStartTime"
        ttl_fe.suStartTime = "suStartTime"
        ttl_fe.mEndTime = "mEndTime"
        ttl_fe.tEndTime = "tEndTime"
        ttl_fe.wEndTime = "wEndTime"
        ttl_fe.thEndTime = "thEndTime"
        ttl_fe.fEndTime = "fEndTime"
        ttl_fe.saEndTime = "saEndTime"
        ttl_fe.suEndTime = "suEndTime"
        ttl_fe.altnames = ["altname1", "altname2"] 

        ttl_fe.write_to(self.ttl)
        self.ttl.close()
 
        f = open (self.filename, 'r')
        fstr = f.read()
        f.close()

        self.assertTrue("name \"name\"" in fstr)
        self.assertTrue("name \"altname1\"" in fstr)
        self.assertTrue("name \"altname2\"" in fstr)
        self.assertTrue("property \"property\"" in fstr)
        self.assertTrue("title \"title\"" in fstr)
        self.assertTrue("department \"department\"" in fstr)
        self.assertTrue("address \"address\"" in fstr)
        self.assertTrue("room \"room\"" in fstr)
        self.assertTrue("education \"education\"" in fstr)
        self.assertTrue("email \"email\"" in fstr)
        self.assertTrue("website \"website\"" in fstr)
        self.assertTrue("picture \"picture\"" in fstr)
        self.assertTrue("publications \"publications\"" in fstr)
        self.assertTrue("phone \"phone\"" in fstr)
        self.assertTrue("interests \"interests\"" in fstr)
        self.assertTrue("bio \"bio\"" in fstr)
        self.assertTrue("mStartTime \"mStartTime\"" in fstr)
        self.assertTrue("tStartTime \"tStartTime\"" in fstr)
        self.assertTrue("wStartTime \"wStartTime\"" in fstr)
        self.assertTrue("thStartTime \"thStartTime\"" in fstr)
        self.assertTrue("fStartTime \"fStartTime\"" in fstr)
        self.assertTrue("saStartTime \"saStartTime\"" in fstr)
        self.assertTrue("suStartTime \"suStartTime\"" in fstr)
        self.assertTrue("mEndTime \"mEndTime\"" in fstr)
        self.assertTrue("tEndTime \"tEndTime\"" in fstr)
        self.assertTrue("wEndTime \"wEndTime\"" in fstr)
        self.assertTrue("thEndTime \"thEndTime\"" in fstr)
        self.assertTrue("fEndTime \"fEndTime\"" in fstr)
        self.assertTrue("saEndTime \"saEndTime\"" in fstr)
        self.assertTrue("suEndTime \"suEndTime\"" in fstr)
 

    def test_faculty_last_names(self):
        ttl_fe = TtlFileEntry()
        ttl_fe.name = "test this man"
        ttl_fe.property = "faculty"

        ttl_fe.write_to(self.ttl)
        self.ttl.close()
 
        f = open (self.filename, 'r')
        fstr = f.read()
        f.close()
        
        self.assertTrue("name \"test this man\"" in fstr)
        self.assertTrue("name \"man\"" in fstr)


    def test_fix_strings(self):
        ttl_fe = TtlFileEntry()
        ttl_fe.name = "name\n"
        ttl_fe.property = "property\t"
        ttl_fe.title = "title\r"
        ttl_fe.department = "   department       "
        ttl_fe.address = "\"address\""
        ttl_fe.room = "room           number"

        ttl_fe.write_to(self.ttl)
        self.ttl.close()
        
        f = open (self.filename, 'r')
        fstr = f.read()
        f.close()
        
        self.assertTrue("name \"name\"" in fstr)
        self.assertTrue("property \"property\"" in fstr)
        self.assertTrue("title \"title\"" in fstr)
        self.assertTrue("department \"department\"" in fstr)
        self.assertTrue("address \"\\\"address\\\"\"" in fstr)
        self.assertTrue("room \"room number\"" in fstr)

if __name__ == '__main__':
    unittest.main()
