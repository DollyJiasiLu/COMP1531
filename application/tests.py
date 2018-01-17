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
        course_offering = ""
        s.addClasses(course_offering)
        handle.addUser(s)
        self.assertFalse(validCourse(handle,s.getClasses()))

    def test_enrol_invalid_course(self):

        zID = "99998"     #this is a valid id
        s = Student(zID)
        course_offering = "Cump333"
        s.addClasses(course_offering)
        handle.addUser(s)
        self.assertFalse(validCourse(handle,s.getClasses()))

    def test_unique_student(self):

        zID = "99998"
        user = handle.getUser(zID)
        self.assertEqual(user.getName(), zID)


class TestEnrolGuest(unittest.TestCase):

    def test_enrol_guest_no_course(self):
        email = "test@test.com"
        g = Student(email)
        course_offering = ""
        g.addClasses(course_offering)
        handle.addUser(g)
        self.assertFalse(validCourse(handle,g.getClasses()))

    def test_enrol_guest_invalid_course(self):

        email = "test1@test.com"     #this is a valid id
        g = Student(email)
        course_offering = "Cump333"
        g.addClasses(course_offering)
        handle.addUser(g)
        self.assertFalse(validCourse(handle,g.getClasses()))

    def test_unique_guest(self):

        email = "test1@test.com"
        user = handle.getUser(email)
        self.assertEqual(user.getName(), email)


class TestCreateSurvey(unittest.TestCase):

    def test_add_valid_survey(self):

        s = Survey(1)
        s.setName("This is a test Survey")
        handle.addSurvey(s)
        self.assertTrue(goodSurveyName(s.getName()))

    def test_add_invalid_survey(self):

        s = Survey(1)
        s.setName(123)
        handle.addSurvey(s)
        self.assertFalse(goodSurveyName(s.getName()))

    def test_survey_no_questions(self):

        s = Survey(1)
        s.setName("This is a test Survey")
        handle.addSurvey(s)
        self.assertFalse(goodSurvey(s))

    def test_survey_no_courses(self):

        s = Survey(1)
        s.setName("This is a test Survey")
        handle.addSurvey(s)
        self.assertFalse(goodSurvey(s))

class TestAddQuestions(unittest.TestCase):

    def test_add_valid_question(self):

        q = Question(1)
        q.setName("This is a test Question?")
        handle.addQuestion(q)
        self.assertTrue(goodQuestion(q.getName()))

    def test_add_invalid_question(self):

        q = Question(1)
        q.setName(134)
        self.assertFalse(goodQuestion(q.getName()))

    def test_add_valid_answers(self):

        q = Question(1)
        q.setName("This is a test Question?")
        q.addAnswer("This is a valid answer")
        self.assertTrue(goodOption(q.getAnswers()[0]))

    def test_add_invalid_answers(self):

        q = Question(1)
        q.setName("This is a test Question?")
        q.addAnswer(134)
        self.assertFalse(goodOption(q.getAnswers()[0]))

if __name__=="__main__":
    unittest.main()
