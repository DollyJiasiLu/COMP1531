class User:
    def __init__(self, ID):
        self._ID = ID
        self._password = ""
        self.type = -1
    def setID(self, ID):
        self._ID = ID

    def setName(self, username):
        self._ID = username

    def setPass(self, password):
        self._password = password

    def getName(self):
        return self._ID

    def getPass(self):
        return self._password


class Admin(User):
    def __init__(self, ID):
        User.__init__(self, ID)
        self.type = 1

class Staff(User):
    def __init__(self, ID):
        User.__init__(self, ID)
        self.type = 2
        self._currentlyTeaching = []

    def addClasses(self, ID):
        self._currentlyTeaching.append(ID)

    def setSurveys(self, surveys):
        self._currentlyTeaching = surveys
    def getClasses(self):
        return self._currentlyTeaching

class Student(User):
    def __init__(self, ID):
        User.__init__(self, ID)
        self.type = 3
        self._currentlyEnrolled = []

    def addClasses(self, ID):
        self._currentlyEnrolled.append(ID)
    def getClasses(self):
        return self._currentlyEnrolled

    def setClasses(self, surveys):
        self._currentlyEnrolled = surveys
