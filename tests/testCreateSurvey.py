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




if __name__== "__main__":
    unittest.main()
