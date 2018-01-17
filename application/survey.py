import csv, datetime
# import datetime.datetime.strptime as toObj
# import datetime.datetime.strftime as toStr
#import datetime.datetime as Time
class Survey:

	def __init__(self, id): #variables of class survey- ID and name is sent TO the class.
		self._name = ""
		self._courses = []
		self._status = 0
		self._ID = id
		self._qIDs = []
		self._completed = []
		self._open = None
		self._close = None
		self._url = "localhost:8004/survey/"+str(id)

#Methods for the class Survey is here

	def setID(self, id):  #this sets the ID and the URL for the survey
		self._ID = id	 #Every survey has to have an unique ID and URL
		self._url = "localhost:8004/survey/"+str(id) 	# sets the ID by the ID that is passed through the function
														# URL is set by the ID number which is added to the URL to
														# open the surveys tab.
													 	#should check that name is unique
	def setName(self, name):		   #this sets the name of the survey which gets stored
										#This is input related -admin
		self._name = name

	def setStatus(self,status):
		self._status = status

	def setOpen(self,date):
		if date != None:
			self._open = datetime.datetime.strptime(date,"%Y-%m-%dT%H:%M")
		else:
			self._open = None

	def setOpenObj(self,date):
		date = datetime.datetime.strftime(date,"%Y-%m-%dT%H:%M")
		self.setOpen(date)

	def setClose(self,date):
		if date != None:
			self._close = datetime.datetime.strptime(date,"%Y-%m-%dT%H:%M")
		else:
			self._open = None

	def setCloseObj(self,date):
		date = datetime.datetime.strftime(date,"%Y-%m-%dT%H:%M")
		self.setClose(date)

	def addCompleted(self,student):
		if student not in self._completed:
			self._completed.append(student)

	def addCourse(self, course):         #This adds another course to the survey										 #This means that surveys for multiple courses can be added
		if course not in self._courses:
			self._courses.append(course) #checks whether the specific course is in the class, if not adds it

	def addQuestion(self, q):  			#adds a certain question to the class.
		if q not in self._qIDs: 		#based on question IDs-since everything has a specific ID
			self._qIDs.append(q)		#if not, adds the qID and hence the question

	def removeCourse(self, course):
		if course in self._courses:
			self._courses.remove(course) #removes all values with instance 'course'

	def removeQuestion(self, q):         #removes question with instance q
		if q in self._qIDs:				 #checks if the question (by qID) is there, if so, deletes that specific question
			self._qIDs.remove(q)

	def getName(self):						#returns the name of the survey- which gets passed through and gets printed on the interface
											#Output related- students/public
		return self._name

	def getStatus(self):
		return self._status

	def getCompleted(self):
		return self._completed


	def getCourses(self):				#returns the courses available, under the class
		return self._courses			#output related- goes through routes.py

	def getQuestions(self):				#returns the questions in the class
		return self._qIDs

	def getID(self):					# Every survey has an unique ID- which allows it to be distinguished
		return self._ID					#This function returns it

	def getCompleted(self):
		return self._completed

	def getOpen(self):
		if self._open == None:
			return None
		return self._open

	def getStrOpen(self):
		if self._open == None:
			return None
		return datetime.datetime.strftime(self._open,"%Y-%m-%dT%H:%M")

	def getStrClose(self):
		if self._close == None:
			return None
		return datetime.datetime.strftime(self._close,"%Y-%m-%dT%H:%M")

	def getClose(self):
		if self._close == None:
			return None
		return self._close

	def getURL(self):					#returns the URL of the survey
		return self._url
#Survey Related functions:
#saved in following format:
"""
ID, name, url
course1, course2, ...
qID1, qID2, qID3, ...


"""

# def getSurveyList():
# 	lst = []
# 	with open('CSVs/surveys.csv', 'r') as file:
# 		reader = csv.reader(file)
# 		i = 0
# 		lines = []
# 		for row in reader:
# 			lines.append(row)
# 			if i%3 == 2:
# 				current = Survey(int(lines[0][0]), lines[0][1])
# 				for course in lines[1]:
# 					current.addCourse(course)
# 				for q in lines[2]:
# 					current.addQuestion(int(q))
# 				lst.append(current)
# 				lines = []
# 			i += 1
# 	return lst
#
# def saveSurveyList(list):
# 	with open('CSVs/surveys.csv', 'w') as file:
# 		writer = csv.writer(file)
# 		for survey in list:
# 			writer.writerows([[survey.getID(), survey.getName(), survey.getURL()], \
# 			survey.getCourses(), survey.getQuestions()])
