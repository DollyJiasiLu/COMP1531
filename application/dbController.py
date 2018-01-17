from dbModel import dbModel
import copy

qDict = {'id': 0, 'name': 1, 'type': 2,'isMandatory': 3,'isDeleted': 4, 'option': 5}
sDict = {'id': 0, 'name': 1, 'status': 2, 'open': 3,'close': 4,'qs': 5, 'class': 6, 'completed': 7}
cDict = {'id': 0, 'name': 1, 'sem': 2, 'survey': 3}
uDict = {'id': 0, 'pass': 1, 'type': 2,'class': 3}
rDict = {'id': 0, 'qs': 1, 'type': 2, 'ans': 3}

class dbController:
	def __init__(self,dbName):
		self._model = dbModel(dbName)

	def getSurvey(self, surveyID):

		survey = self._model.getSurvey(surveyID)
		#print("survey is :", survey)
		survList = []
		for s in survey:
			s = list(s)
			#print("s is: ", s)
			if surveyID != None:
				s.insert(0,surveyID)
			sList = []
			for surv in self._model.getQRef(surveyID = s[sDict['id']]):
				sList.append(surv[0])
			s.append(copy.deepcopy(sList))
			sList = []
			for surv in self._model.getSurveyAllocation(surveyID = s[sDict['id']]):
				sList.append(surv[0])
			s.append(copy.deepcopy(sList))
			sList = []
			for surv in self._model.findCompleted(s[sDict['id']]):
				sList.append(surv[0])
			s.append(copy.deepcopy(sList))
			survList.append(s)

		return survList

	def getQuestion(self, qID):
		question = self._model.getQuestion(qID)
		#print("model gives: ",question)
		qList = []
		for q in question:
			q = list(q)
			if qID != None:
				q.insert(0, qID)
			if q[qDict['type']] == 'm':
				qs = []
				for quest in self._model.getOptions(q[qDict['id']]):
					qs.append(quest)
				q.append(qs)
			qList.append(q)
		return qList

	def getClass(self, classID):
		c = self._model.getClass(classID)
		retC = []
		for course in c:
			course = list(course)
			if (classID != None):
				course.insert(0, classID)
				cList = []
				for cls in self._model.getSurveyAllocation(classID = course[0]):
					cList.append(cls[0])
				course.append(cList)
			retC.append(course)
		return retC

	def getUser(self, userID):
		#if userID == None:
			#return -1
		#print(userID)
		user = self._model.getUser(userID)
		if (len(user) == 0):
			return [-1,-1,-1]
		else:
			user = list(user[0])
		user.insert(0,userID)
		eList = []
		for enrol in self._model.getEnrollments(userID = userID):
			eList.append(enrol[0])
		user.append(eList)
		return user

	def getGuest(self, userID):
		users = self._model.getGuest(userID)
		uList = []
		for user in users:
			if (len(user) == 0):
				u = [-1,-1,-1]
				return u
			else:
				u = list(user)
				if userID != None:
					u.insert(0,userID)
			uList.append(copy.deepcopy(u))

		return uList

	def getResults(self, surveyID):
		res = [surveyID]				#res[0] = sID, res[1] = [q1,q2,q3,...], res[2] =
		s = self.getSurvey(surveyID)[0]
		qs = [self._model.getQuestion(q) for q in s[sDict['qs']]]
		qList = []
		aList = []
		types = []
		for indx,q in enumerate(qs):
			q = list(q[0])
			q.insert(0,s[sDict['qs']][indx])
			qs[indx] = q
		#print("qs: ", qs)
		for q in qs:
			answers = []
			types.append(q[qDict['type']])
			qList.append(q[0])
			#print("q[qDict['type']]:",q[qDict['type']])
			if q[qDict['type']] != 't':
				options = self._model.getOptions(q[0]) #list option arrays
				#print("options: ",options)
				for i in range(0,len(options)): #get option array
					answers.append([options[i][0],self._model.getOptionResult(surveyID, options[i][0])[0]])#[optionID, answers]
			else:
				rows = self._model.getTextResponse(surveyID,q[qDict['id']])
				ans = []
				for row in rows:
					ans.append(row[0])
				answers.append(ans) #[optionID, answers]
			aList.append(copy.deepcopy(answers)) #list of strings or list of tallies
			print("ANS: ",aList)
		res.append(qList)
		res.append(types)
		res.append(aList)
		return res

	def addSurvey(self, survey):
		surveyID = self._model.addSurvey(survey[1:5])[0]
		for q in survey[sDict['qs']]:
			self._model.addQRef([surveyID,q])
			question = self.getQuestion(q)[0]
			qType = question[qDict['type']]
			# if qType == 'm':
			# 	options = question[qDict['option']]
			# 	for o in options:
			# 		self._model.addOptionResult([surveyID, o[0], 0])

		for c in survey[sDict['class']]:
			self._model.addSurveyAllocation([c,surveyID])
		return surveyID

	def addQuestion(self, question):
		qID = self._model.addQuestion(question[1:5])
		qType = question[qDict['type']]
		IDs = []
		if qType == 'm':
			options = question[qDict['option']]
			for o in options:
				IDs.append([self._model.addOption([qID[0], o])[0],o])
		#print("questions:",question)
		return [qID[0],IDs]

	def addClass(self, course):
		classID = self._model.addClass(course[1:3])
		return classID

	def addUser(self, user):
		self._model.addUser(user[0:3])

	def addGuest(self,user):
		self._model.addGuest(user)

	def transferGuest(self,uID):
		info = self.getGuest(uID)[0]
		courses = info[uDict["class"]-1]
		info[uDict["type"]] = 3
		self._model.addUser(info[0:3])
		for c in map(int,courses.split(',')):
			self.addEnrollment(uID,c)
		#add user to db and courses
		#map(int,request.form["course-IDs"].split(','))
		print("This literally does nothing")
		self.removeGuest(uID)
	def removeGuest(self,ID):
		self._model.deleteGuest([ID])

	def addEnrollment(self, userID, classID):
			self._model.addEnrollment([classID, userID])

	def updateSurvey(self, survey):
		surveyID = survey[sDict['id']]
		curr = self.getSurvey(surveyID)[0]
		currQ = curr[sDict['qs']]
		currC = curr[sDict['class']]
		self._model.updateSurvey([survey[sDict['name']],survey[sDict['status']],\
		survey[sDict['open']],survey[sDict['close']],surveyID])
		currStudents = curr[sDict['completed']]


		if (curr[sDict['status']] == 1 and \
		survey[sDict['status']] == 2 or survey[sDict['status']] == 3):
			try:						#only add results when approved
				for q in survey[sDict['qs']]:
					question = self.getQuestion(q)[0]
					qType = question[qDict['type']]
					if qType == 'm':
						options = question[qDict['option']]
						for o in options:
							self._model.addOptionResult([surveyID, o[0], 0])
			except:
				pass
				#this means the survey was reverted to 3
		for c in survey[sDict['class']]:
			if c not in currC:
				self._model.addSurveyAllocation([c, surveyID])
		for c in currC:
			#print("survey says",survey[sDict['class']], "but db says",currC)
			if c not in survey[sDict['class']]:
				#print("deleteing these",c)
				self._model.deleteSurveyAllocation([surveyID,c])

		for q in survey[sDict['qs']]:
			if q not in currQ:
				self._model.addQRef([surveyID,q])
		for q in currQ:
			if q not in survey[sDict['qs']]:
				self._model.deleteQRef([surveyID,q])
		#print("completed s is:",survey[sDict['completed']])
		for c in survey[sDict['completed']]:
			if c not in currStudents:
				self._model.addCompleted([surveyID, c])

	def updateQuestion(self, question):
		qID = question[qDict['id']]

		curr = self._model.getQuestion(qID)
		currOptions = question[qDict['option']]
		for option in currOptions:
			self._model.updateOption((qID,option[1],option[0]))


	def updateResults(self, res):
		sID = res[rDict['id']]
		qs = res[rDict['qs']]
		types = res[rDict['type']]
		answers = res[rDict['ans']]
		for i,q in enumerate(qs):
			#print("this is q", q)
			if types[i] == 'm':
				for a in answers[i]:
					self._model.updateTally([a[1],sID,a[0]])
			else:
				self._model.addTextResult([sID, q, answers[i][0]])

	def clearRecords(self):
		self._model.clearRecords()

	def __del__(self):
		del self._model
