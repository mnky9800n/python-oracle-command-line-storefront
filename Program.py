#
#
#  Author: John Aiken
#
#
# TODO
# 1 - connect to oracledb
# 2 -  login menu
# 3 -  login 
# 4 -  logged in menu
# 5 -  log out

#from cx_Oracle import *

import cmd, cx_Oracle, sys

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

    def do_memberLogin(username, person):
        """Allows existing members to login"""
        while True:
            try:
                 username = input('please enter a user name: ')
                 password = input('please enter a password: ')
                 break
            except ValueError:
                print "Please try again!"

    def do_newMemberRegistration(self, person):
        """Allows new members to register an account"""

    def do_quit(self, person):
        """Quits the program"""
        return sys.exit

    def do_itsATrap(self, person):
        trap = """           .          .
 .          .                  .          .              .
       +.           _____  .        .        + .                    .
   .        .   ,-~"     "~-.                                +
              ,^ ___         ^. +                  .    .       .
             / .^   ^.         \         .      _ .
            Y  l  o  !          Y  .         __CL\H--.
    .       l_ `.___.'        _,[           L__/_\H' \\--_-          +
            |^~"-----------""~ ^|       +    __L_(=): ]-_ _-- -
  +       . !                   !     .     T__\ /H. //---- -       .
         .   \                 /               ~^-H--'
              ^.             .^            .      "       +.
                "-.._____.,-" .                    .
         +           .                .   +                       .
  +          .             +                                  .
         .             .      .       -Row
                                                        .

                                ->DeathStar<-

"""
        print trap

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

lm = loginMenu()
sm = storeMenu()

class accessDatabase(cx_Oracle,loginMenu,storeMenu):
   
    _connstr='the joker lives here'

    def memberLogin(username, password):
        conn = conn.connect(_connstr)
        curs = conn.cursor()
        while True:
            try:
                checkUserId = curs.execute('SELECT userid FROM members WHERE userid =' + "'"+ username + "'")
                checkPassword = curs.execute('SELECT password FROM members WHERE password =' + "'" + password + "'")
                if checkUserId == username:
                    if checkPassword == password:
                        sm.cmdloop()
                else:
                    #ask for username and password again
                    pass
            except:
                print 'please try again' #im not entirely sure I understand exceptions

    def connectToDatabase(self, userName, password):
        connstr='jaiken1/jaiken1@tinman.cs.gsu.edu:1522/tinman'
        print "You're using Oracle Client Tools v"+".".join(map(str,cx_Oracle.clientversion()))
        conn = cx_Oracle.connect(connstr)
        curs = conn.cursor()
        curs.execute('select * from bs_books')
        print curs.description

        for row in curs:
            print row
        conn.close()

print lm.cmdloop()

