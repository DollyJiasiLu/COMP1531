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


class TestAddQuestions(unittest.TestCase):

    def test_add_valid_question(self):

        q = Question(1)
        q.setName("This is a test Question?")
        handle.addQuestion(q)
        self.assertTrue(goodQuestion(q.getName()))

    def test_add_invalid_question(self):

        q = Question(1)
        q.setName(134)
        handle.addQuestion(q)
        self.assertFalse(goodQuestion(q.getName()))

    def test_add_valid_answers(self):

        q = Question(1)
        q.setName("This is a test Question?")
        q.addAnswer("This is a valid answer 1")
        q.addAnswer("This is a valid answer 2")
        alist = q.getAnswers()
        handle.addQuestion(q)
        self.assertTrue(goodOption(alist[0]))

    def test_add_invalid_answers(self):

        q = Question(1)
        q.setName("This is a test Question?")
        q.addAnswer(134)
        handle.addQuestion(q)
        self.assertFalse(goodOption(q.getAnswers()))

    def test_add_optional_question(self):

        q = Question(1)
        q.setName("This is a optional test question?")
        q.addAnswer("This is a sample answer 1")
        q.addAnswer("This is a sample answer 2")
        q.setType('m')
        q.setMandatory(False)
        handle.addQuestion(q)
        self.assertTrue(validQuestion(handle,q.getID()))


if __name__== "__main__":
    unittest.main()
