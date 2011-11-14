

from helpers import *
from menus import *
#from browse import *

import cmd, cx_Oracle, sys, re

ga = gatherer()

#variables

#functions

#classes

class loginMenu(cmd.Cmd):

    def postloop():
        print 'You have logged in as: ' + username

    intro = """
**********************************************************************
***                                                                ***
***             Welcome to the Online Book Store                   ***
***                                                                ***
**********************************************************************

                         1. memberLogin

                         2. newMemberRegistration

                         3. quit

type 'help' to list available commands.
"""
    prompt = """Please choose an option: """


    def do_printMenu(self,person):
        """
        Prints main menu.
        format: printMenu <no args>
        """
        print """
**********************************************************************
***                                                                ***
***             Welcome to the Online Book Store                   ***
***                                                                ***
**********************************************************************

                         1. Member Login

                         2. New Member Registration

                         q. Quit

type 'help' to list available commands.
"""

    def do_openMemberships(self,person):
        """
        Lists open membership userID's.
        This will be removed in later versions.
        format: openMemberships <no args>
        """
        ds.execute('SELECT userID FROM bs_members')
        rowCount = 0
        for row in ds:
            rowCount+=1
            print row


    def do_memberLogin(self,input):
        global username
        """
        Allows existing members to login.
        format: memberLogin <username> <password>
        """

        tpl = input.partition(" ")

        if tpl[1]=="":
            print """
Incorrect syntax for memberLogin.
format: memberLogin <username> <password>
"""
        else:
            username = tpl[0]
            password = tpl[2]
            sql = """SELECT userid, password
                FROM bs_members
                WHERE userid = :userid
                AND password = :pword"""
            
            connectAndCheck = ds.execute(sql, userid=username,pword=password)
            tplStr = ''.join(tpl)

            for row in ds:
                if ' '.join(row) == tplStr:
                    #TODO - this should pass the logged in user info to something 
                    #       the storeMenu class can use.
                    return True
            print 'Incorrect userID or password.  Please try again.'

    def do_newMemberRegistration(self,input):
        """
        Allows new members to register an account.
        Users will be prompted with a series of questions to acquire
        accurate and complete account information.
        format: newMemberRegistration <no args>
        """

        class userData:
            pass

        newUser = userData()
        newUser.fname = ga.getInput('Enter first name: ', "[a-zA-Z ']+$")  #o'neill
        newUser.lname = ga.getInput('Enter last name: ', "[a-zA-Z ']+$")
        newUser.streetAddress = ga.getInput('Enter street address: ', "[\w\s]+$")
        newUser.city = ga.getInput('Enter city: ', "[a-zA-Z ']+$")
        newUser.state = ga.getInput('Enter state abbreviation: ', "\w{2}$")
        newUser.zipCode = ga.getInput('Enter zip code: ', "^\d{5}(-\d{4})?$")
        newUser.phoneNumber = ga.getInput('Enter phone number: ', "(\d{3})[-.]?(\d{3})[-.]?(\d{4})$")
        newUser.email = ga.getInput('Enter email: ', "\w+@\w+\.\w+$")
        
        checkSql = 'SELECT userid FROM bs_members WHERE userid = :checkUser'
        while True:
            newUser.userID = ga.getInput('Enter userID: ', "\w+$")
            ds.execute(checkSql,checkUser=newUser.userID)
            for row in ds:
                if row[0] == newUser.userID:
                    print 'That user name is already in use.  Please enter a new username.'
                    break
            else:
                break


#            try:
#                ds.execute(check.sql,userid=check.user) == None
#                break
#            except DatabaseError:
#                print 'That user name is already in use.  Please enter a new username.'

        newUser.password = ga.getInput('Enter password: ', "\w{8}\w*$")
        creditCardYN = ga.getInput('Do you want to store credit card information (y or n): ', "(y|n)$")
        if creditCardYN == 'y':
            newUser.CCtype = ga.getInput('Enter credit card type (amex/visa): ',"(amex|visa)$")
            newUser.CCnumber = ga.getInput('Enter credit card number: ', "\d{16}$")
        else:
            newUser.CCtype = None
            newUser.CCnumber = None
                   
        userDataSql = 'INSERT INTO bs_members VALUES ( :fname, :lname, :street, :city, :state, :zip, :phone, :email, :userID, :password, :cardtype, :cardnumber)'

        print 'You have registered successfully.'
        print 'Name:                                '+newUser.fname+' '+newUser.lname
        print 'Address:                             '+newUser.streetAddress
        print 'City:                                '+newUser.city
        print 'Phone:                               '+newUser.phoneNumber
        print 'Email:                               '+newUser.phoneNumber
        print 'UserID:                              '+newUser.userID
        print 'Password:                            '+newUser.password
        if newUser.CCtype == None and newUser.CCnumber == None:
            pass
        else:
            print 'Credit card type:                    '+newUser.CCtype
            print 'Credit card number:                  '+newUser.CCnumber

        ds.execute(userDataSql, fname=newUser.fname, lname=newUser.lname, street=newUser.streetAddress, city=newUser.city, state=newUser.state, zip=newUser.zipCode, phone=newUser.phoneNumber, email=newUser.email, userID=newUser.userID, password=newUser.password, cardtype=newUser.CCtype, cardnumber=newUser.CCnumber)


    def do_quit(self, person):
        """
        Quits the program.
        format: quit <no args>
        """
        sys.exit()

class storeMenu(cmd.Cmd):

    intro = """**********************************************************************
***                                                                ***
***                  Welcome to Online Book Store                  ***
***                          Member Menu                           ***
***                                                                ***
**********************************************************************

                     1. Browse by Subject

                     2. Search by Author/Title/Subject

                     3. View/Edit Shopping Cart

                     4. Check Order Status

                     5. Check Out

                     6. One Click Check Out

                     7. View/Edit Personal Information

                     8. logOut
 
type 'help' to list available commands.
""" + "Logged in as: " + username
    prompt = """Please choose an option: """
    def do_logOut(self,person):
        """
        Logs user out and returns them to the 
        login menu.
        format: logOut <no args>
        """
        #TODO - this should obliterate any logged in info kept 
        #       to access the db with.  It should also return
        #       the user to the login menu
        return True

#    def do_Browse(self,person):
