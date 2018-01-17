import hashlib

users = ['user1','user2','user3','user4','user5']

passwords = []
passwords.append((hashlib.md5('password'.encode('utf-8')).hexdigest()))
passwords.append((hashlib.md5('userlogin'.encode('utf-8')).hexdigest()))
passwords.append((hashlib.md5('randomstuff'.encode('utf-8')).hexdigest()))
passwords.append((hashlib.md5('something'.encode('utf-8')).hexdigest()))
passwords.append((hashlib.md5('ceebsman'.encode('utf-8')).hexdigest()))

print(passwords[0])
file = open('Users.csv','w+')
for i in range(0,len(passwords)):
    file.write(users[i] + ',' + str(passwords[i]))
    if i != (len(passwords) - 1):
        file.write('\n')
file.close()
