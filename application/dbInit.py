import csv
from user import User
from Class import Class
from dbHandle import dbHandle


def getCSVList(name):
	lst = []
	with open('CSVs/' + name, 'r') as file:
		reader = csv.reader(file)
		lines = []
		for row in reader:
			if row not in lines:
				lines.append(row)
	return lines

def formatUser(user):
	u = User(user[0])
	u.setPass(user[1])
	if user[2] == "staff":
		u.type = 2
	elif user[2] == "student":
		u.type = 3
	else:
		u.type = 1

	return u

def formatClass(cls):
	c = Class(-1)
	c.setName(cls[0])
	c.setSem(cls[1])
	return c

def getClassID(course, lst, IDs):

	return IDs[lst.index(course)]

def dbInit():
	handle = dbHandle('survey.db')
	handle.clearDB()
	courses = getCSVList('courses.csv')
	classIDs = []
	for c in courses:
		cls = formatClass(c)
		try:
			classIDs.append(handle.addClass(cls))
		except:
			pass

	users = getCSVList('passwords.csv')
	for u in users:
		usr = formatUser(u)
		try:
			handle.addUser(usr)
		except:
			pass



	enrollments = getCSVList('enrolments.csv')
	for e in enrollments:
		classID = getClassID(e[1:], courses, classIDs)
		try:
			handle.addEnrollment(e[0], classID)
		except:
			pass

	del handle
