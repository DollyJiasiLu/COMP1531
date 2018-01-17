import unittest
import os
from dbModel import *
from dbHandle import *
from dbController import *
from survey import *
from question import *
from user import *
from Class import *
from testDB import *
from dbInit import *

handle = dbHandle("survey.db")
dbInit()

class TestEnrolGuest(unittest.TestCase):

    def test_enrol_guest_no_course(self):
        email = "test@test.com"         #this is a valid email
        g = Student(email)
        course_offering = ""            #invalid course
        g.addClasses(course_offering)
        handle.addUser(g)
        self.assertFalse(validCourse(handle,g.getClasses()))

    def test_enrol_guest_invalid_course(self):

        email = "test1@test.com"     #this is a valid email
        g = Student(email)
        course_offering = "Cump333"         #coursse doesnt exist in database
        g.addClasses(course_offering)
        handle.addUser(g)
        self.assertFalse(validCourse(handle,g.getClasses()))

    def test_non_unique_guest(self):

        email = "test@test.com"         #this user is already in the database
        user = handle.getUser(email)
        self.assertEqual(user.getName(), email)

if __name__=="__main__":
    unittest.main()
