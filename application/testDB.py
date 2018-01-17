from question import Question
def goodSurveyName(name):
    if type(name) != type(""):
        return False
    if len(name) == 0 or len(name) > 100:
        return False
    return True

def goodSurvey(s):
    if len(s.getQuestions()) == 0:
        return False
    if len(s.getCourses()) == 0:
        return False
    return True

def goodQuestion(name):
    if type(name) != type(""):
        return False
    if len(name) == 0 or len(name) > 200:
        return False
    return True

def goodOption(option):
    if type(option) != type(""):
        return False
    if len(option) == 0 or len(option) > 100:
        return False
    return True

def validCourse(handle,c):
    try:
        int(c)
        c = handle.getClass(c)
        c.getSem()
    except:
        return False
    return True

def validQuestion(handle,q):
    try:
        int(q)
        q = handle.getQuestion(q)
        q.getAnswers()

    except:
        print("invalid q - id is:",q)
        return False
    return True

def validUser(handle,user):
    try:
        if handle.getUser(user).getName() != -1:
            return False #testing if already is db
        if handle.getGuest(user).getName() != -1:
            return False
        if type(user) != type(""):
            return False
        if len(user) < 1:
            return False
        if len(user) > 50:
            return False
    except:
        pass
    return True

def validEmail(handle,email):
    try:
        if handle.getUser(email).getName() != -1:
            return False #testing if already is db
        if handle.getGuest(email).getName() != -1:
            return False
        if type(email) != type(""):
            return False
        if "@" not in email:
            return False
        if len(email) < 3:
            return False
        if len(email) > 50:
            return False
    except:
        pass
    return True
