
class Results:
    def __init__(self, ID):
        self._sID = ID
        self._Qs = []
        self._answers = []
        self._types = []
    def setSurvey(self, ID):
        self._sID = ID

    def getSurvey(self):
        self._sID;

    def addQuestion(self, qID, Qtype):
        self._Qs.append(qID)
        self._types.append(Qtype)

    def addAnswer(self,ans):
        return self._answers.append(ans)

    def setAnswers(self,ans):
        self._answers = ans

    def getSurvey(self):
        return self._sID

    def getQuestions(self):
        return self._Qs

    def getTypes(self):
        return self._types

    def getAnswers(self):
        return self._answers
