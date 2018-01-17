import csv

class Question:
	def __init__(self, ID): #this is only for use by the getQuestionList() function
		self._ID = ID
		self._question = ""			#changed from _name to _question (question class does not have an _name field)
		self._options = []
		self._type = ""
		self._isMandatory = True
		self._isDeleted = False



#Methods of the class Question is here



	def setID(self, id):
		self._ID = id

	def setName(self, name): 		#This gets question from the interface and is processed through routes.py
							 		#and this is set through EditQuestion and AddQuestion in routes.py
		self._question = name

	def addAnswer(self, answer):      #Every question is meant to have answers which can be set
									  #administrators- processed in routes.py
		self._options.append(answer)

	def setType(self, qtype):      #Every question is meant to have answers which can be set
										  #administrators- processed in routes.py
		self._type = qtype

	def setMandatory(self, val):      #Every question is meant to have answers which can be set
										  #administrators- processed in routes.py
		self._isMandatory = val

	def setDelete(self, val):
		self._isDeleted = val

	def setAnswers(self,answers):
 		self._options = answers

	def getID(self):                  #this is meant to get the ID of the question- this returns the ID
		return self._ID

	def getName(self):				 #returns the question to be pronted on page
									 #this is passed through to AddQuestion and TakeSurvey functions in routes.py
		return self._question

	def getAnswers(self):			#these returns the answers that is set to each quesiton
									#get passed into AddQuestion function in routes.py
		return self._options

	def getSpecificAnswer(self, num):		#returns the actual answer given a number
		return self._options[num]

	def getType(self):						#returns the type of question
		return self._type

	def getisMandatory(self):				#returns whether the questions is mandatory
		return self._isMandatory

	def getisDeleted(self):					#returns as to whether the questions is actually deleted or not
		return self._isDeleted




"""
format for questions is:
qID, name
answer1, answer2, answer3, ...

"""
def getQuestionList(): 											#This function is meant to get the question list that
																#questions csv.
	lst = []
	with open('CSVs/questions.csv', 'r') as file:
		reader = csv.reader(file)							    #opens the csv file, as readable and stores it in reader.
		i = 0
		lines = []
		for row in reader:
			lines.append(row)									#Lines list reads every row in the csv file and updates the list
																#By the end of this, list is meant to have all the questions that is stored
			if i%2 == 1:
				current = Question(int(lines[0][0]))			#current is of class question and gets appended everytime- so
																#everytime a new object of class Question is created

				current.setName(lines[0][1])					#current's variables get updated- its name,etc
				for answer in lines[1]:						    #the answers for the question is set to current
					current.addAnswer(answer)
				lst.append(current)								#lst is the final array that stores the questions and is returned
				lines = []
			i += 1
	return lst

def saveQuestionList(list):										#saves the question into the csv file.
	with open('CSVs/questions.csv', 'w') as file:
		writer = csv.writer(file)
		for q in list:													#for every quesiton in list, writer gets updated- which is the
																		#variable for the csv file.
			writer.writerows([[q.getID(), q.getName()], q.getAnswers()])
