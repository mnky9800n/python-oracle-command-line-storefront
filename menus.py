import cmd
from helpers import *

ds = dataSet("jaiken1/jaiken1@tinman.cs.gsu.edu:1522/tinman")
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
        firstName = ga.getInput('Enter first name: ', "[\w^\d][\w^\d]*")

        print firstName

        #userDataSql = 'INSERT INTO bs_members VALUES ( :user )'
        #ds.execute(userDataSql,user=userDataStr)

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
