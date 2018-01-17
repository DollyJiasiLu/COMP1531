import copy
from survey import Survey
from question import Question
from user import User, Student, Staff, Admin
from Class import Class
from results import Results
from testDB import *

from dbController import dbController, qDict, sDict, cDict, uDict, rDict
#editing, approval, published, closed, deleted
class dbHandle:
	def __init__(self,dbName):
		self._controller = dbController(dbName)

	def getSurvey(self, surveyID):

		survey = self._controller.getSurvey(surveyID)
		if (survey == -1):
			return -1
		sList = []
		#print("survey is: ", survey)
		for surv in survey:
			#print("surv is: ", surv)
			s = Survey(surv[sDict['id']])
			s.setName(surv[sDict['name']])
			s.setStatus(surv[sDict['status']])
			s.setOpen(surv[sDict['open']])
			s.setClose(surv[sDict['close']])
			for q in surv[sDict['qs']]:
				s.addQuestion(q)
			for c in surv[sDict['class']]:
				s.addCourse(c)
			for student in surv[sDict['completed']]:
				s.addCompleted(student)
				#print("this is in comp:",s.getCompleted())
				s.setOpen(surv[sDict['open']])
				s.setClose(surv[sDict['close']])
			sList.append(s)
		if surveyID == None:
			return sList
		else:
			#print(sList)
			return sList[0]

	def getQuestion(self, qID):
		question = self._controller.getQuestion(qID)
		#print(question)
		qList = []
		for quest in question:
			if (quest[qDict['type']] == 'm'):
				q = Question(quest[qDict['id']])
				for a in quest[qDict['option']]:
					q.addAnswer(a)
			elif(quest[qDict['type']] == 't'):
				q = Question(quest[qDict['id']])
			q.setType(quest[qDict['type']])
			q.setName(quest[qDict['name']])
			q.setMandatory(quest[qDict['isMandatory']])
			q.setDelete(quest[qDict['isDeleted']])
			qList.append(q)
		if qID == None:
			return qList
		else:
			return qList[0]

	def getOptionalQuestion(self, qID):
		question = self._controller.getQuestion(qID)
		#print(question)
		qList = []
		for quest in question:
			if quest[qDict['isMandatory']] != 1:
				if (quest[qDict['type']] == 'm'):
					q = Question(quest[qDict['id']])
					for a in quest[qDict['option']]:
						q.addAnswer(a)
				elif(quest[qDict['type']] == 't'):
					q = Question(quest[qDict['id']])
				q.setType(quest[qDict['type']])
				q.setName(quest[qDict['name']])
				q.setMandatory(quest[qDict['isMandatory']])
				q.setDelete(quest[qDict['isDeleted']])
				qList.append(q)
		if qID == None:
			return qList
		else:
			return qList[0]

	def getClass(self, classID):
		classes = self._controller.getClass(classID)
		#print("classes = ",classes)
		cList = []
		for course in classes:
			c = Class(course[cDict['id']])
			c.setName(course[cDict['name']])
			c.setSem(course[cDict['sem']])
			try:
				for s in course[cDict['survey']]:
					c.addSurvey(s)
			except:
				pass
			cList.append(c)
		if (classID == None):
			return cList
		else:
			try:
				return cList[0]
			except:
				return []

	def getUser(self, userID):
		user = self._controller.getUser(userID)
		if (user[0] == -1):
			u = User(-1)
			u.setPass(-1)
			return u
		if user[uDict['type']] == 1:
			u = Admin(user[uDict['id']])
		elif user[uDict['type']] == 2:
			u = Staff(user[uDict['id']])
		else:
			u = Student(user[uDict['id']])

		u.setPass(user[uDict['pass']])
		if u.type != 1:
			for c in user[uDict['class']]:
				u.addClasses(c)
		return u

	def getGuest(self, userID):
		users = self._controller.getGuest(userID)
		if (len(users) == 0):
			return []
		if (users[0] == -1):
			u = User(-1)
			u.setPass(-1)
			return u
		uList = []
		for user in users:
			u = Student(user[uDict['id']])
			u.setPass(user[uDict['pass']])
			u.setClasses(user[uDict['class']-1])
			uList.append(copy.deepcopy(u))
		if userID == None:
			return uList
		else:
			return uList[0]

	def getResults(self, surveyID):
		#print("finish getResults - handle")
		res = self._controller.getResults(surveyID)
		r = Results(surveyID)
		for q in range(0,len(res[rDict['qs']])):
			r.addQuestion(res[rDict['qs']][q],res[rDict['type']][q])
		for a in res[rDict['ans']]:
			r.addAnswer(a)
		return r

	def addSurvey(self, survey):
		s = []
		s.append(survey.getID())
		s.append(survey.getName())
		s.append(survey.getStatus())
		s.append(survey.getStrOpen())
		s.append(survey.getStrClose())

		s.append(survey.getQuestions())
		s.append(survey.getCourses())
		s.append(survey.getCompleted())

		s = self._controller.addSurvey(s)
		survey.setID(s)

		return survey
		# classes = []
		# for c in survey.getClass():
		# 	classes.append(c)
		# s.append(classes)

	def addQuestion(self, question):
		q = []
		q.append(question.getID())
		q.append(question.getName())
		q.append(question.getType())
		q.append(question.getisMandatory())
		q.append(question.getisDeleted())
		if question.getType() == 'm':
			q.append(question.getAnswers())
		ret = self._controller.addQuestion(q)
		question.setID(ret[0])
		question.setAnswers(ret[1])
		return question

	def addClass(self, course):
		c = []
		c.append(course.getID())
		c.append(course.getName())
		c.append(course.getSem())
		return self._controller.addClass(c)

	def addUser(self, user):
		u = []
		u.append(user.getName())
		u.append(user.getPass())
		u.append(user.type)
		try:
			self._controller.addUser(u)
		except:
			pass

	def addGuest(self,user):
		u = []
		u.append(user.getName())
		u.append(user.getPass())
		u.append(user.getClasses())
		self._controller.addGuest(u)

	def transferGuest(self,guestID):
		self._controller.transferGuest(guestID)

	def removeGuest(self,guestID):
		self._controller.removeGuest(guestID)

	def addEnrollment(self, userID, classID):
		self._controller.addEnrollment(userID, classID)

	def updateSurvey(self, survey):
		s = []
		s.append(survey.getID())
		s.append(survey.getName())
		s.append(survey.getStatus())
		s.append(survey.getStrOpen())
		s.append(survey.getStrClose())

		s.append(survey.getQuestions())
		s.append(survey.getCourses())
		s.append(survey.getCompleted())
		print("this is s:", s)
		self._controller.updateSurvey(s)

	def updateQuestion(self, question):
		q = []
		q.append(question.getID())
		q.append(question.getName())
		q.append(question.getType())
		q.append(question.getisMandatory())
		q.append(question.getisDeleted())
		if question.getType() == 'm':
			#q.append([question.getAnswerID(),question.getAnswerText()])
			q.append(question.getAnswers())
		#print("updating q: ",q)
		self._controller.updateQuestion(q)

	def updateResults(self, results):
		res = []
		res.append(results.getSurvey())
		res.append(results.getQuestions())
		res.append(results.getTypes())
		res.append(results.getAnswers())
		self._controller.updateResults(res)

	def clearDB(self):
		self._controller.clearRecords()

	def __del__(self):
		del self._controller
