from flask import Flask, render_template, json, request, redirect
from server import app
from getPass import passwords
from question import Question #, saveQuestionList, getQuestionList
from survey import Survey #, saveSurveyList, getSurveyList
from user import User, Student, Staff, Admin
from Class import Class
from Auth import authenticator
from dbInit import dbInit
from dbHandle import dbHandle
from testDB import goodOption, goodQuestion, goodSurveyName, validCourse, validQuestion, validEmail
import hashlib, copy, csv, datetime

app = Flask(__name__)
dbInit()
handle = dbHandle("survey.db")
#
# testsurvey = Survey(-1)
# testquestion = Question(-1)
# testquestion._question = "this is just a test question, but that doesnt mean your answer cant be wrong"
# testquestion._type = "M"
# qtest = handle.addQuestion(testquestion)
# testsurvey._qIDS = [qtest.getID()]
# testsurvey._courses = [68]
# stest = handle.addSurvey(testsurvey)
# stest.setName("This is a test survey, for testing purposes, ya feel?")
# stest.setStatus(1)
# handle.updateSurvey(stest)




# qList = getQuestionList()
# sList = getSurveyList()
qList = []
sList = []
cList = []
tList = []
oList = []
uNames = []
user = User(-1)
user.type = -1;
surveyID = 0
@app.route("/", methods=["GET", "POST"])
def main():

    if (user.type == 1):
        if request.method == "POST":
            try:
                u = request.form["approve"]
                handle.transferGuest(u)
            except:
                 u = request.form["reject"]
                 handle.removeGuest(u)
        cDict = {}
        for c in handle.getClass(None):
            cDict[str(c.getID())] = c
        return render_template("index.html", uList = handle.getGuest(None), cDict = cDict)
    if (user.type == 2):
        # Student = Authentication Module
        return redirect("/staffHome")
    if (user.type == 3):
        if "@" not in user.getName():
            return redirect("/studentHome")
        return redirect("/guestHome")

    else:
        return redirect("/login")

#@app.route("/login")
#ef showLogin():
#    print("sending login page")
#    return render_template("login.html")

@app.route("/questions", methods=["GET", "POST"])
def showQuestions():
    if (user.type != 1):
        return redirect("/")

    print("showing added questions")
    if request.method == "POST":
        try:
            return redirect("/editQuestion/" + request.form["question"])
        except:
            qID = int(request.form["delete"])
            question = handle.getQuestion(qID)
            question.setDelete(True)
            handle.updateQuestion(question)

            return redirect("/questions")

    else:
        return render_template("questions.html", qList = handle.getQuestion(None))

@app.route("/createMCQuestion", methods=["GET", "POST"])
def addMCQuestion():
    global loggedIn
    if (user.type != 1 and user.type != 2):
        return redirect("/login")

    print("sending question page")
    if request.method == "POST":
            global qList
            q = Question(-1)
            q.setName(request.form["question"])
            if not goodQuestion(q.getName()):
                return redirect("/questions")
            finished = 0
            i = 0
            q.setType('m')
            while not finished:
                try:
                    q.addAnswer(request.form["a"+str(i)])
                    if not goodOption(request.form["a"+str(i)]):
                        return redirect("/questions") #only checked if valid
                    i = i+1
                except:
                    finished = 1

            print(q.getID())
            print(q.getName())
            print(q.getAnswers())
            q = handle.addQuestion(q)
            print(q.getAnswers())
            return redirect("/questions")

    else:
        return render_template("createMCQ.html", numAnswers = 2)

@app.route("/createTextQuestion", methods=["GET", "POST"])
def addTextQuestion():
    global user
    if (user.type != 1):
        return redirect("/login")

    print("sending question page")
    if request.method == "POST":
            global qList
            q = Question(-1)
            q.setName(request.form["question"])
            if not goodQuestion(q.getName()):
                return redirect("/questions")
            q.setType('t')
            print(q.getID())
            print(q.getName())
            print(q.getAnswers())
            q = handle.addQuestion(q)
            return redirect("/questions")
    else:
        return render_template("createTextQ.html")

@app.route("/createSurvey", methods=["GET", "POST"])
def createSurvey():
    if (user.type != 1):
        return redirect("/")
    print("create survey page")
    if request.method == "POST":
        s = Survey(-1)
        s.setName(request.form["name"])
        if not goodSurveyName(s.getName()):
            return redirect("/questions")
        s.setStatus(0)
        s.setOpen(request.form["activation"] if (request.form["activation"] != "") else None)
        s.setClose(request.form["close"] if (request.form["close"] != "") else None)
        print("times recieved: ", s.getOpen()," and ", s.getClose())
        print("courses recieved: ",map(int,request.form["course-IDs"].split(',')))
        for course in map(int,request.form["course-IDs"].split(',')):
            if validCourse(handle,course):
                s.addCourse(course)
            print("hello course: ", course)
        for q in request.form.getlist("question"):
            if validQuestion(handle,q):
                s.addQuestion(int(q))
            if len(s.getQuestions()) < 1:
                return redirect("/surveys")
        s = handle.addSurvey(s)
        return redirect("/surveys")

    else:
        #k = handle.getQuestion(None)
        #print("********************")
        #for q in k:
            #print(q.getAnswers())
        return render_template("createSurvey.html", qList = handle.getQuestion(None), courses = handle.getClass(None))

@app.route("/surveys", methods=["GET", "POST"])
def displaySurveys():
    if (user.type != 1):
        return redirect("/")
    now = datetime.datetime.now()
    print("showing all surveys")
    if request.method == "POST":
        try:
            rString = ""
            survey = request.form["chosenSurvey"]
            toUpdate = handle.getSurvey(survey)
            activ = request.form[survey+"activation"]
            close = request.form[survey+"close"]
            toUpdate.setOpen(activ)
            toUpdate.setClose(close)
            if toUpdate.getStatus() == 3 and now > toUpdate.getOpen():
                rString = "activate"
                toUpdate.setStatus(2)
            elif toUpdate.getStatus() == 2 and now < toUpdate.getOpen():
                rString = "close?" + toUpdate.getStrOpen()
                toUpdate.setStatus(3)
                print("returning: ",)
            elif toUpdate.getStatus() == 3 and now < toUpdate.getOpen():
                rString = "keep?" + toUpdate.getStrOpen()
            toUpdate.setOpen(activ)
            toUpdate.setClose(close)
            handle.updateSurvey(toUpdate)
            print("returning: ",rString)
            return rString
        except:
            try:
                survey = request.form["delete"]
                toDel = handle.getSurvey(survey)
                toDel.setStatus(3)
                toDel.setOpen(None)
                toDel.setClose(None)
                handle.updateSurvey(toDel)
            except:
                try:
                    survey = request.form["approval"]
                    toApprove = handle.getSurvey(survey)
                    toApprove.setStatus(1)
                    handle.updateSurvey(toApprove)
                except:
                    return redirect("/editSurvey/" + request.form["survey"])
            return redirect("/surveys")
    else:
        now = datetime.datetime.now()
        qDict = {}
        sDict = {}
        cDict = {}
        for s in handle.getSurvey(None):
            if s.getStatus() == 3:
                if s.getOpen() != None and s.getOpen() > now:
                    sDict[s.getID()] = s
            else:
                sDict[s.getID()] = s
        for q in handle.getQuestion(None):
            if q.getisDeleted() == False:
                qDict[q.getID()] = q
        for c in handle.getClass(None):
            cDict[c.getID()] = c
        return render_template("surveys.html", sDict = sDict, qDict = qDict, cDict = cDict)


@app.route("/editSurvey/<id>", methods=["GET", "POST"])
def editSurvey(id):
    if (user.type != 1):
        return redirect("/")
    id = int(id)
    chosenSurvey = handle.getSurvey(id)
    print("create survey page")
    if request.method == "POST":
        s = Survey(id)
        s.setName(request.form["name"])
        s.setStatus(0)
        print("courses recieved: ",map(int,request.form["course-IDs"].split(',')))
        for course in map(int,request.form["course-IDs"].split(',')):
            s.addCourse(course)
            print("hello course: ", course)
        for q in request.form.getlist("question"):
            print("is working",q)
            s.addQuestion(int(q))
        print("adding: ",s.getQuestions())
        s = handle.updateSurvey(s)
        chosenSurvey = s
        return redirect("/")

    else:
        cList = [handle.getClass(c) for c in chosenSurvey.getCourses()]
        return render_template("editSurvey.html", survey = chosenSurvey, \
            qList = handle.getQuestion(None), courses = cList, cList = handle.getClass(None))

@app.route("/thankyou")
def Thankyoupage():
        return render_template("ThankYou.html")

@app.route("/staffHome", methods = ["GET", "POST"])
def staffHomePage():
    global user
    #global cList
    #global sList
    filtcList = []
    filtsList = []
    cDict = {}
    sDict = {}
    if (user.type != 2):
        return redirect("/")
    print("showing staff home")
    for c in user.getClasses():
        cDict[c] = handle.getClass(c)
        for s in cDict[c].getSurveys():
            sDict[s] = handle.getSurvey(s)

    for s in sDict:
        for c in sDict[s].getCourses():
            if c not in user.getClasses():
                sDict[s].removeCourse(c)
    for s in sDict:
        for c in sDict[s].getCourses():
            cDict[c] = handle.getClass(c)

    name = user.getName()


    return render_template("staffHome.html", cDict = cDict, sDict = sDict, now = datetime.datetime.now(), name = name)

@app.route("/guestHome")
def guestHomePage():
    global sList
    sDict = {}
    cDict = {}
    global handle
    global cList
    global user
    if (user.type != 3 or "@" not in user.getName()):
        return redirect("/")

    print("showing all surveys")
    # for classes in user, add surveys for that class

    classes = user.getClasses()
    for course in classes:
        # print(courses[0])
        cDict[course] = handle.getClass(course)
        # print(course)
        #cList.append(course)
    #print(cList)
    for course in cList:
        for survey in course.getSurveys():
            s = handle.getSurvey(survey)
            if (s.getStatus() == 2 and user.getName() not in s.getCompleted()):
                sDict[s.getID()] = s
        # for surveys in that course add to clist
    return render_template("guestHome.html", sDict = sDict, qList = handle.getQuestion(None), cDict = cDict, now = datetime.datetime.now())


@app.route("/studentHome")
def studentHomePage():
    global sList
    tList = []
    cDict = {}
    global handle
    global cList
    global user
    if (user.type != 3 or "@" in user.getName()):
        return redirect("/")

    print("showing all surveys")
    # for classes in user, add surveys for that class
    for c in handle.getClass(None):
        cDict[c.getID()] = c
    classes = user.getClasses()
    for courses in classes:
        # print(courses[0])
        course = handle.getClass(courses)
        # print(course)
        if course not in cList:
            cList.append(course)
    #print(cList)
    idList = []
    for course in cList:
        for survey in course.getSurveys():
            s = handle.getSurvey(survey)
            if (s.getStatus() == 2 and user.getName() not in map(str,s.getCompleted())) or s.getStatus() == 3:
                if s.getID() not in idList:
                    tList.append(s)
                    idList.append(s.getID())
        # for surveys in that course add to clist
    return render_template("studentHome.html", sList = tList, qList = handle.getQuestion(None), cDict = cDict, now = datetime.datetime.now())

@app.route("/survey/<id>", methods=["GET", "POST"])
def takeSurvey(id):
    if (user.type != 3):
        return redirect("/")
    id = int(id)
    print("showing survey " + str(id))
    chosenSurvey = handle.getSurvey(id)

    for u in chosenSurvey.getCompleted():
        if str(user.getName()) == str(u):
            return redirect("/studentHome")
    qList = [handle.getQuestion(q) for q in chosenSurvey.getQuestions()]

    if request.method == "POST":
        currRes = handle.getResults(id)
        newAns = currRes.getAnswers()
        print("current format: ",newAns)
        types = currRes.getTypes()
        for i,currQ in enumerate(qList):
            try:
                inc = request.form[str(currQ.getID())]
            except:
                inc = ""
                if currQ.getisMandatory() == True:
                    return redirect("/studentHome")
            if inc != "":
                if currQ.getType() == 'm':
                    optionList = [str(a[0]) for a in currQ.getAnswers()]
                    print("option list; ",optionList)
                    newAns[i][optionList.index(inc)][1] += 1
                    pass #optional question
                else:
                    newAns[i] = [inc]

            print("newAns", newAns[i], " i ", i)
            # newAns[i] = inc
        print("adding to db",newAns)
        currRes.setAnswers(newAns)
        handle.updateResults(currRes)
        chosenSurvey.addCompleted(user.getName())
        handle.updateSurvey(chosenSurvey)



        return redirect("/thankyou")
    else:
        for q in qList:
            print(q.getType())
        return render_template("takeSurvey.html", qList = qList, survey = chosenSurvey)

@app.route("/reviewsurvey/<id>", methods=["GET", "POST"])
def reviewsurvey(id):
    global surveyID
    if (user.type != 2):
        return redirect("/")
    id = int(id)
    surveyID = id
    print("showing survey " + str(id))
    global sList
    global qList
    now = datetime.datetime.now()
    chosenSurvey = []
    chosenSurvey = handle.getSurvey(id)
    if request.method == "POST":
        try:
            request.form['review']
            if chosenSurvey.getClose() < now:
                newOpen = now + datetime.timedelta(days=31)
                chosenSurvey.setOpenObj(newOpen)
                newClose = now + datetime.timedelta(days=32)
                chosenSurvey.setCloseObj(newClose)
            if chosenSurvey.getOpen() == None or (now > chosenSurvey.getOpen() and \
            (chosenSurvey.getClose() == None or now < chosenSurvey.getClose())):
                chosenSurvey.setStatus(2)
            else:
                chosenSurvey.setStatus(3)
            handle.updateSurvey(chosenSurvey)
            return redirect("/")
        except:
            pass
        try:
            request.form['reject']
            chosenSurvey.setStatus(0)
            handle.updateSurvey(chosenSurvey)
            return redirect("/")
        except:
            pass
        return redirect("/staffquestion")
    else:
        qDict = {}
        for q in chosenSurvey.getQuestions():
            qDict[q] = handle.getQuestion(q)
        return render_template("reviewsurvey.html", qDict = qDict, survey = chosenSurvey,sList = sList)

@app.route("/staffSurvey", methods = ["GET", "POST"])
def staffSurvey():
    global user
    global cList
    global sList
    filtcList = []
    filtsList = []
    if (user.type != 2):
        return redirect("/")
    print("showing all surveys")
    for course in sList:
        print("found this course", course._name)
        print("this is sList", sList[1]._name)
        name = handle.getClass(course._courses[0])
        filtcList.append(name._name)
        filtsList.append(course._url)

    else:
        return render_template("staffEditSurvey.html", filtcList = filtcList, filtsList = filtsList)

@app.route("/results", methods=["GET", "POST"])
def resultDashboard():
    if (user.type != 1):
        return redirect("/")
    print("showing all results")
    if request.method == "POST":
        survey = request.form["delete"]
        toDel = handle.getSurvey(survey)
        toDel.setStatus(4)
        handle.updateSurvey(toDel)
        return redirect("/results")
    else:
        qDict = {}
        sDict = {}
        cDict = {}
        for s in handle.getSurvey(None):
            if s.getStatus() >= 1 and s.getStatus() < 4:
                sDict[s.getID()] = s
        for q in handle.getQuestion(None):
            qDict[q.getID()] = q
        for c in handle.getClass(None):
            cDict[c.getID()] = c
        return render_template("resultsDashboard.html", sDict = sDict, qDict = qDict, cDict = cDict, now = datetime.datetime.now())
    return redirect("/results")

@app.route("/staffquestion", methods=["GET","POST"])
def optionalStaff():
    global surveyID
    print(surveyID)
    if request.method == "POST":
        try:
            request.form['mcq']
            return redirect("/staffCreateMCQ")
        except:
            pass
        try:
            request.form['t']
            return redirect("/staffCreateText")
        except:
            pass
        try:
            request.form['add']
            s = handle.getSurvey(surveyID)
            for q in request.form.getlist("question"):
                if int(q) not in map(int,s.getQuestions()):
                    s.addQuestion(int(q))
            handle.updateSurvey(s)
            print("this question will be  added to survey")
            path = "/reviewsurvey/"+surveyID
            print(path)
            return redirect(path)
        except:
            pass
        try:                                            #AMAN PLZ CHECK
            survey = request.form['delete']
            toDel = handle.getSurvey(survey)
            toDel.setStatus(3)
            handle.updateSurvey(toDel)
            return redirect('/staffquestion')
        except:
            pass
        return redirect('/staffquestion')
    else:
        return render_template("optionalquestion.html", qList=handle.getOptionalQuestion(None),courses = handle.getClass(None))


@app.route("/staffCreateMCQ", methods=["GET", "POST"])
def staffMCQ():
    global loggedIn
    if (user.type != 1 and user.type != 2):
        return redirect("/login")

    print("sending question page")
    if request.method == "POST":
        global qList
        q = Question(-1)
        q.setName(request.form["question"])
        finished = 0
        i = 0
        q.setMandatory(False)
        q.setType('m')
        while not finished:
            try:
                q.addAnswer(request.form["a" + str(i)])
                i = i + 1
            except:
                finished = 1

        print(q.getID())
        print(q.getName())
        print(q.getAnswers())
        q = handle.addQuestion(q)
        print(q.getAnswers())
        return redirect("/staffquestion")
    else:
        return render_template("staffCreateMCQ.html", numAnswers=2)

@app.route("/staffCreateText",methods=["GET", "POST"])
def staffText():
    global loggedIn
    if (user.type != 1 and user.type != 2):
        return redirect("/login")

    print("sending question page")
    if request.method == "POST":
            global qList
            q = Question(-1)
            q.setName(request.form["question"])
            q.setType('t')
            q.setMandatory(False)
            print(q.getID())
            print(q.getName())
            print(q.getAnswers())
            q = handle.addQuestion(q)
            return redirect("/staffquestion")
    else:
        return render_template("staffCreateTextQ.html")


@app.route("/results/<id>", methods=["GET", "POST"])
def showResults(id):
    now = datetime.datetime.now()
    id = int(id)
    print("showing results of " + str(id))

    chosenSurvey = handle.getSurvey(id)
    #if chosenSurvey.getStatus() == 0:
    #    return redirect("/surveys")
    if not (chosenSurvey.getStatus() >= 1 or chosenSurvey.getStatus() <= 3):
        return redirect("/")
    if user.type == 2 or user.type == 3:
        if chosenSurvey.getStatus() != 3 or chosenSurvey.getOpen() != None:
            if chosenSurvey.getOpen() == None or chosenSurvey.getOpen() > now:
                return redirect("/")

    qDict = {}
    for q in chosenSurvey.getQuestions():
        qDict[q] = handle.getQuestion(q)

    results = handle.getResults(id)

    optionText = {}
    optionTally = {}
    textAnswers = {}
    for index,q in enumerate(results.getAnswers()):
        qID = chosenSurvey.getQuestions()[index]
        tempIDs = []
        tempText = []
        try:
            print("textAnswer Q is",q)
            for a in q:
                int(a[0])
                optionTally[a[0]] = int(a[1])
        except:
            print("textAnswer Q is",q)
            for a in q:
                if qID in textAnswers:
                    textAnswers[qID].append(a[0])
                else:
                    textAnswers[qID] = a


    print("THE OPTIONS GIVEN: ",textAnswers)
    for q in chosenSurvey.getQuestions():
        for o in qDict[q].getAnswers():
            optionText[o[0]] = o[1]
    print("giving optionTexts:", optionText, "giving optionTally:",optionTally)
    return render_template("results.html", qDict = qDict, survey = chosenSurvey, \
        results = handle.getResults(id), oTally = optionTally, oText = optionText, textAnswers = textAnswers)

@app.route("/register",methods=["GET","POST"])
def registerUser():

    if request.method == "POST":
        name = request.form["name"]
        if not validEmail(handle,name):
            print("invalid email")
            return redirect("/register")
        usr = Student(name)
        usr.setPass(request.form["pass"])
        usr.setClasses(request.form["course-IDs"])
        user = handle.addGuest(usr)
        return redirect("/")
    return render_template("register.html",courses = handle.getClass(None),incorrect='false')

@app.route("/login",methods=["GET", "POST"])
def processLogin():
    global loggedIn
    global cList
    global sList
    now = datetime.datetime.now()
    if request.method == "POST":
        _user = request.form['username']
        _password = request.form['password']

        global user
        user = authenticator(_user, _password)
        if user == -1:
            return render_template("login.html", incorrect = 'true')

        for s in handle.getSurvey(None):
            stat = s.getStatus()
            print("STAT:",stat,s.getClose(),s.getOpen())
            if stat == 2 and s.getClose() != None:
                if s.getClose() < now:
                    s.setStatus(3)
                    s.setOpen(None)
                    s.setClose(None)
                    handle.updateSurvey(s)
            elif stat == 3 and s.getClose() != None and s.getOpen() != None:
                print("updating this:",s.getID())
                print("this is open and now:",s.getOpen(),now)
                if now > s.getOpen() and now < s.getClose():
                    print("updating")
                    s.setStatus(2)
                    handle.updateSurvey(s)

        if (user.type == 2):
            loggedIn = 2
            cList = [handle.getClass(c) for c in user.getClasses()]
            sIDs = []
            for c in cList:
                print(c._name)
                print(c.getSurveys())
                for s in c.getSurveys():
                    sIDs.append(s)
            #print("the sids",sIDs[0])
            for s in sIDs:
                sList.append(handle.getSurvey(s))
            for j in sList:
                if j.getStatus() != 1:
                    sList.remove(j)
            qIDs = []
            #print("this is the sList", sList[0]._ID)
            for s in sList:
                for q in s.getQuestions():
                    qIDs.append(q)
            qList = [handle.getQuestion(q) for q in qIDs]
            #print("this is in login", cList[0]._name, sList, qList)
            return redirect("/staffHome")

        if (user.type == 3):
            loggedIn = 3
            cList = [handle.getClass(c) for c in user.getClasses()]

            sIDs = []
            for c in cList:
                for s in c.getSurveys():
                    sIDs.append(s)
            sList = [handle.getSurvey(s) for s in sIDs]
            for s in sList:
                if s.getStatus() != 2:
                    sList.remove(s)
                elif user.getName() in s.getCompleted():
                    sList.remove(s)
            qIDs = []
            for s in sList:
                for q in s.getQuestions():
                    qIDs.append(q)
            qList = [handle.getQuestion(q) for q in qIDs]

            if "@" in user.getName():
                return redirect("/guestHome")
            return redirect("/studentHome")

        loggedIn = 1
        cList = handle.getClass(None)
        sList = handle.getSurvey(None)
        qList = handle.getQuestion(None)
        return redirect("/")
    return render_template("login.html", incorrect = 'false')
