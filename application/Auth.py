from dbHandle import dbHandle
handle = dbHandle("survey.db")
def authenticator(username, password):
    myUser = handle.getUser(username)
    if(password == myUser.getPass()):
        return myUser
    else:
        return -1
