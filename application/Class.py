class Class:                        #A class with variables ID, name, semester and the surveys
    def __init__(self, ID):
        self._ID = ID
        self._name = ""
        self._sem = ""
        self._surveys = []          #The various methods

    def setID(self,ID):
        self._ID = ID

    def setName(self, name):        #This sets the name of the class
        self._name = name

    def setSem(self, sem):          #This should set the name of the semester
        self._sem = sem

    def setSurveys(self, surveys):  #This should set the surveys
        self._surveys = surveys

    def getID(self):                #This is the opposite, it returns the ID of the object
        return self._ID

    def getName(self):              #Returns the name
        return self._name

    def getSem(self):               #Returns the semester
        return self._sem

    def getSurveys(self):           #Returns the list of surveys
        return self._surveys

    def addSurvey(self, ID):        #This adds a survey with defined ID to the class.
        self._surveys.append(ID)
