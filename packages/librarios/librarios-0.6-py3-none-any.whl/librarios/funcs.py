# FILE FOR FUNCTIONS/VARIABLES REQUIRED IN MAIN FILE

# FUNCS 

import getpass

def greet():
    print('''\n -------------------WELCOME TO LIBRARIOS --------------------
           \n           Your personal Library Management System''')

def getn():
    rname=input("\nEnter the name of person : ")
    return rname

def getb():
    rbook=input("\nEnter the name of book which is being issued : ")
    return rbook

def getp():
    rphno=input("\nEnter the phone number of person : ")
    return rphno

# VARIABLES

usern= input("Enter your MySql username : ")

pwd = getpass.getpass(f"Enter password for {usern} to continue : ")

val_entry = "INSERT INTO library (issued_on, name, book, phone_no) VALUES (%s, %s, %s, %s)"
sel_all = "SELECT * FROM library"
sel_book = "SELECT book FROM library WHERE name = '%s'"
sel_phno = "SELECT phone_no FROM library WHERE name = '%s'"
del_ent = "DELETE FROM library WHERE = (%s)"
updt_phno = "UPDATE library SET phone_no = '%s' WHERE name = '%s'"
updt_book = "UPDATE library SET book = '%s' WHERE name = '%s'"








