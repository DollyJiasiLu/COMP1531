
from survey import Survey, getSurveyList, saveSurveyList
from question import Question, getQuestionList, saveQuestionList
s = Survey("test", 0, "/test")
s.addCourse("COMP2041 17s2")
s.addCourse("COMP1531 17s2")
s.addCourse("COMP2041 17s2")
s.addQuestion(0)
s.addQuestion(1)
s.addQuestion(2)
s.addQuestion(3)
s.removeQuestion(0)
s.removeQuestion(1)


t = Survey("test", 0, "/test")
t.addCourse("COMP2041 17s2")
t.addCourse("COMP1531 17s2")
t.addCourse("COMP2041 17s2")
t.addQuestion(0)
t.addQuestion(1)
t.addQuestion(2)
t.addQuestion(3)

saveSurveyList([s,t])

q = Question(0)
q.setName("testQ")
q.addAnswer("lol kek")
q.addAnswer("idk man")
q.addAnswer("i dislike python")


r = Question(1)
r.setName("testQ2")
r.addAnswer("kek kek")
r.addAnswer("ceebs")
r.addAnswer("defs ceebs")

saveQuestionList([r,q])

lst = getSurveyList()


qlst = getQuestionList()

for survey in lst:
	print([[survey.getID(), survey.getName(), survey.getURL()], \
		survey.getCourses(), survey.getQuestions()])
for q in qlst:
	x

