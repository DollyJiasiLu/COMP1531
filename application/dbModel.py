
import sqlite3
from create import createStatements
qDict = {'name': 0,'type':1,'isMandatory': 2,'isDeleted': 3,'id': 0, 'option': 1}
sDict = {'name': 0,'status': 1}
cDict = {'name': 0,'sem': 1}
uDict = {'id': 0,'pass': 1}


#take list of atrributes, table name & input attribute
class dbModel:
	def __init__(self,dbname):
		self._connection = sqlite3.connect(dbname)
		self._cursor = self._connection.cursor()
		for create in createStatements:
			self._cursor.execute(create)
			self._connection.commit()

	def getSurvey(self, id):
		if (id == None):
			query = "SELECT * from Surveys"
			return self._getEverything(query)
		query = "SELECT name, status, open, close from Surveys where ID = ?"
		survey = self._getQuery(query,[id])
		return survey

	# def getTimes(self,id):
	# 	query = "SELECT open, close from Surveys where ID = ?"
	# 	survey = self._getQuery(query,[id])
	# 	return survey[0]

	def getQuestion(self, id):
		if (id == None):
			query = "SELECT * from Questions"
			return self._getEverything(query)

		query = "SELECT question, type, isMandatory, isDeleted from Questions where ID = ?"
		question = self._getQuery(query,[id])
		return question

	def getClass(self, id):
		if (id == None):
			query = "SELECT * from Classes"
			return self._getEverything(query)

		query = "SELECT name, sem from Classes where ID = ?"
		classInfo = self._getQuery(query,[id])
		return classInfo

	def getUser(self, userID):
		query = "SELECT password, type from Users where ID = ?"
		user = self._getQuery(query,[userID])
		return user

	def getGuest(self, userID):
		if userID == None:
			query = "SELECT * from Guests"
			return self._getEverything(query)
		query = "SELECT password, courses from Guests where ID = ?"
		user = self._getQuery(query,[userID])
		return user

	def findCompleted(self, surveyID):
		query = "SELECT userID from completedSurvey where surveyID = ?"
		completed = self._getQuery(query,[surveyID])
		return completed

	def getOptions(self, qID):
		query = "SELECT ID, option from mcAnswers where qID = ?"
		answers = self._getQuery(query,[qID]) #empty if not mc
		return answers

	def getQRef(self, surveyID = None, qID = None):
		if surveyID == None and qID == None:
			return []
		elif surveyID != None:
			query = "SELECT qID from questionAllocation where surveyID = ?"
			questions = self._getQuery(query,[surveyID])
			return questions
		elif qId != None:
			query = "SELECT surveyID from questionAllocation where qID = ?"
			surveys = self._getQuery(query,[qID])
			return surveys

	def getEnrollments(self, userID = None, classID = None):
		if userID == None and classID == None:
			return []
		elif userID != None:
			query = "SELECT classID from enrollment where userID = ?"
			users = self._getQuery(query, [userID])
			return users
		elif classID != None:
			query = "SELECT userID from enrollment where classID = ?"
			classes = self._getQuery(query, [classID])
			return classes

	def getSurveyAllocation(self, classID = None, surveyID = None):
		if surveyID == None and classID == None:
			return []
		elif surveyID != None:
			query = "SELECT classID from surveyAllocation where surveyID = ?"
			classes = self._getQuery(query, [surveyID])
			return classes
		elif classID != None:
			query = "SELECT surveyID from surveyAllocation where classID = ?"
			surveys = self._getQuery(query,[classID])
			return surveys

	def getOptionResult(self, surveyID, option):
		query = "SELECT tally from mcResults where option = ? AND surveyID = ?"
		tally = self._getQuery(query,[option,surveyID])
		return tally[0]

	def getTextResponse(self, surveyID, qID):
		query = "SELECT answer from saResults where qID = ? AND surveyID = ?"
		answers = self._getQuery(query,[qID,surveyID])
		return answers

	def addSurvey(self, payload):
		query = "INSERT INTO Surveys (name, status, open, close) VALUES (?, ?, ?, ?)"
		self._setQuery(query, payload)
		query = "SELECT ID FROM Surveys ORDER BY ID DESC LIMIT 1"
		return self._getEverything(query)[0]

	def addQuestion(self, payload):
		query = "INSERT INTO Questions (question, type, isMandatory, isDeleted) VALUES (?, ?, ?, ?)"
		self._setQuery(query, payload)
		query = "SELECT ID FROM Questions ORDER BY ID DESC LIMIT 1"
		return self._getEverything(query)[0]

	def addClass(self, payload):
		query = "INSERT INTO Classes (name, sem) VALUES (?, ?)"
		self._setQuery(query, payload)
		query = "SELECT ID FROM Classes ORDER BY ID DESC LIMIT 1"
		#print("in model view")
		#print(self._getEverything(query)[0])

		return self._getEverything(query)[0][0]

	def addUser(self, payload):
		query = "INSERT INTO Users (ID, password, type) VALUES (?, ?, ?)"
		self._setQuery(query, payload)

	def addGuest(self, payload):
		query = "INSERT INTO Guests (ID, password, courses) VALUES (?, ?, ?)"
		self._setQuery(query, payload)

	def addCompleted(self, payload):
		query = "INSERT INTO completedSurvey (surveyID, userID) VALUES (?, ?)"
		self._setQuery(query, payload)

	def addOption(self, payload):
		query = "INSERT INTO mcAnswers (qID, option) VALUES (?, ?)"
		self._setQuery(query, payload)
		query = "SELECT ID FROM mcAnswers ORDER BY ID DESC LIMIT 1"
		return self._getEverything(query)[0]

	def addQRef(self, payload):
		query = "INSERT INTO questionAllocation (surveyID, qID) VALUES (?, ?)"
		self._setQuery(query, payload)

	def addEnrollment(self, payload):
		query = "INSERT INTO enrollment (classID, userID) VALUES (?, ?)"
		self._setQuery(query, payload)

	def addSurveyAllocation(self, payload):
		query = "INSERT INTO surveyAllocation (classID, surveyID) VALUES (?, ?)"
		self._setQuery(query, payload)

	def addOptionResult(self, payload):
		query = "INSERT INTO mcResults (surveyID, option, tally) VALUES (?, ?, ?)"
		self._setQuery(query, payload)

	def addTextResult(self, payload):
		query = "INSERT INTO saResults (surveyID, qID, answer) VALUES (?, ?, ?)"
		self._setQuery(query, payload)

	def updateSurvey(self, payload):
		query = "UPDATE Surveys SET name = ?, status = ?, open = ?, close = ? WHERE ID = ?"
		self._setQuery(query,payload)

	def updateQuestion(self, payload):
		query = "UPDATE Questions SET question = ?, type = ?, isMandatory = ?, isDeleted = ? WHERE ID = ?"
		self._setQuery(query,payload)

	def updateOption(self, payload):
		query = "UPDATE mcAnswers SET qID = ?, option = ? WHERE ID = ?"
		self._setQuery(query,payload)

	def updateTally(self, payload):
		query = "UPDATE mcResults SET  tally = ? WHERE surveyID = ? AND option = ?"
		self._setQuery(query,payload)

	def deleteSurveyAllocation(self, payload):
		query = "DELETE FROM surveyAllocation WHERE surveyID = ? AND classID = ?"
		self._setQuery(query, payload)

	def deleteQRef(self, payload):
		query = "DELETE FROM questionAllocation WHERE surveyID = ? AND qID = ?"
		self._setQuery(query, payload)

	def deleteGuest(self,payload):
		query = "DELETE FROM Guests WHERE ID = ?"
		self._setQuery(query, payload)

	def clearRecords(self):
		query = "DELETE FROM enrollment"
		try:
			self._getEverything(query)
		except:
			pass
		query = "DELETE FROM Classes"
		try:
			self._getEverything(query)
		except:
			pass
		query = "UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='Classes'"
		try:
			self._getEverything(query)
		except:
			pass

	def _setQuery(self, query, payload):
		self._cursor.execute(query,payload)
		self._connection.commit()

	def _getQuery(self, query, payload):
		#print("payload is:", payload)
		rows = self._cursor.execute(query,payload)
		self._connection.commit()
		result = []
		for row in rows:
			result.append(row)
		return result
	def _getEverything(self,query):
		rows = self._cursor.execute(query)
		self._connection.commit()
		result = []
		for row in rows:
			result.append(row)
		return result
	def closeDB(self):
		self._connection.close()

	def __del__(self):
		self.closeDB()
