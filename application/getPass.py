
import csv   							#This is for the login page

passwords = {}

with open('CSVs/Users.csv','r') as csv_in: #This opens the CSV for Users' Passwords, in readable form.
    data = []							#And adds it to the list called data.
    reader = csv.reader(csv_in)
    for row in reader:
        data.append(row)

for row in data:							#Then passwords is updated by the list data.
    passwords.update({row[0] : row[1]})
#print(passwords)
