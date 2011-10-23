

from helpers import *
from menus import *
import cmd, cx_Oracle, sys, re



ga = gatherer()

class loginMenu(cmd.Cmd):
    intro = """
**********************************************************************
***                                                                ***
***             Welcome to the Online Book Store                   ***
***                                                                ***
**********************************************************************

                         1. Member Login

                         2. New Member Registration

                         q. Quit

please type 'help' to explain your options
"""

    prompt = """Please choose an option: """

    def do_openMemberships(self,person):

        sql = 'SELECT * from bs_members'
        print connectToDatabase(sql, 'Y')

    def do_memberLogin(self,input):
        """
        Allows existing members to login
        format: memberLogin <username> <password>
        """
        tpl = input.partition(" ")

        if tpl[1]=="":
            print "Invalid input."
        else:
            username = tpl[0]
            password = tpl[2]

        sql = """SELECT userid, password
            FROM bs_members
            WHERE userid = '%s'
            AND password = '%s'""" % (username,password)

        connectAndCheck = ds.execute(sql)

        if connectAndCheck == tpl[1:2]:
            print 'good job'
        else:
            print connectAndCheck


    def do_newMemberRegistration(self,input):
        """Allows new members to register an account."""
        # this method should prompt the user for user information
        # after each prompt it should add the provided user data
        # to a new element of the same array.  when all the data is
        # correct it will use INSERT INTO members VALUES (userData)

        #TODO
        #street address (\d+)\s((\w)+\s)+
        #city [a-zA-Z]+
        #state \w{2}
        #zip (^\d{5}$)|(^\d{5}-\d{4}$)
        #phone (\d{3})[-.]?(\d{3})[-.]?(\d{4})
        #email \w+@\w\.\w$
        #userID \w+$
        #password \w{8}+
        #creditcard yes/no (y|n)
        #creditcard type (amex|visa)
        #creditcard number \d{16}
        userData = ['fname','lname','streetAddress','city','st','phone','zip','email','userID','password','CCtype','CC#']
        userData[0] = ga.getInput('Enter first name: ', "([a-zA-Z][a-zA-Z]*)")
        userData[1] = ga.getInput('Enter last name: ', "([a-zA-Z][a-zA-Z]*)")
        userData[2] = ga.getInput('Enter street address: ', "[\w\s]+")
        userData[3] = ga.getInput('Enter city: ', "[a-zA-Z]+$")
        userData[4] = ga.getInput('Enter state abbreviation: ', "\w{2}")
        userData[5] = ga.getInput('Enter zip code: ', "(^\d{5}$)|(^\d{5}-\d{4}$)")
        userData[6] = ga.getInput('Enter phone number: ', "(\d{3})[-.]?(\d{3})[-.]?(\d{4})")
        userData[7] = ga.getInput('Enter email: ', "\w+@\w+\.\w+$")
        userData[8] = ga.getInput('Enter userID: ', "\w+$")
        userData[9] = ga.getInput('Enter password: ', "\w{8}\w*")

        creditCardYN = ga.getInput('Do you want to store credit card information (y or n): ', "(y|n)")
        if creditCardYN == 'y':
            userData[10] = ga.getInput('Enter credit card type (amex/visa): ',"(amex|visa)")
            userData[11] = ga.getInput('Enter credit card number: ', "\d{16}")
        else:
            userData[10] = 'null'
            userData[11] = 'null'

        userDataStr = "'"+"','".join(userData)+"'"

        userDataSql = 'INSERT INTO bs_members VALUES ( :user )'
        ds.execute(userDataSql,user=userDataStr)

        #TODO - INSERT INTO members VALUES (userDataStr)

    def do_quit(self, person):
        """Quits the program"""
        return sys.exit

class storeMenu(cmd.Cmd):

    intro = """**********************************************************************
***                                                                ***
***                       Welcome to Online Book Store             ***
***                            Member Menu                         ***
***                                                                ***
**********************************************************************

                     1. Browse by Subject

                     2. Search by Author/Title/Subject

                     3. View/Edit Shopping Cart

                     4. Check Order Status

                     5. Check Out

                     6. One Click Check Out

                     7. View/Edit Personal Information

                     8. Logout"""

    def logOut():
        print "not yet"
