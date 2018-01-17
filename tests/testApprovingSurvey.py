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

class TestApprovingSurvey(unittest.TestCase):

    #creates a survey and approves it.
    #Checks if survey is approved and passes if it is.
    def testApprovingSurvey(self):

        q1 = Question(1)
        q2 = Question(2)

        q1.setName("this is a test q 1")
        q2.setName("this is a test q 2")
        q1.setType('m')
        q2.setType('a')
        q1.addAnswer("answer 1")
        q1.addAnswer("answer 2")

        s = Survey(1)
        s.setName("This is a test Survey")
        s.addQuestion(q1)
        s.addQuestion(q2)
        s.setStatus(1)
        self.assertEqual(s.getStatus(),1)


    #creates a survey and rejects it.
    #Checks if survey is rejected and passes if it is.
    def testRejectSurvey(self):

        q1 = Question(1)
        q2 = Question(2)

        q1.setName("this is a test q 1")
        q2.setName("this is a test q 2")
        q1.setType('m')
        q2.setType('a')
        q1.addAnswer("answer 1")
        q1.addAnswer("answer 2")

        s = Survey(1)
        s.setName("This is a test Survey")
        s.addQuestion(q1)
        s.addQuestion(q2)
        s.setStatus(2)
        self.assertEqual(s.getStatus(),2)

if __name__== "__main__":
    unittest.main()
