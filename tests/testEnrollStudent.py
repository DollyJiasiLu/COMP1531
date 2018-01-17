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

class TestEnrolStudent(unittest.TestCase):

    def test_enrol_student_no_course(self):
        zID = "99999"     #this is a valid id
        s = Student(zID)
        course_offering = ""       #this couse offering is invalid
        s.addClasses(course_offering)
        handle.addUser(s)
        self.assertFalse(validCourse(handle,s.getClasses()))

    def test_enrol_invalid_course(self):

        zID = "99998"     #this is a valid id
        s = Student(zID)
        course_offering = "Cump333"     #this course doesnt exist in the database
        s.addClasses(course_offering)
        handle.addUser(s)
        self.assertFalse(validCourse(handle,s.getClasses()))

    def test_non_unique_student(self):

        zID = "100"     #this ID has already been assigned
        user = handle.getUser(zID)
        self.assertEqual(user.getName(), zID)

if __name__=="__main__":
    unittest.main()
