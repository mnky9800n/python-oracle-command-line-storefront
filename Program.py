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


# functions

def connectAndQuery(input):
    _connstr = "wouldn't you like to know"
    conn = cx_Oracle.connect(_connstr)
    curs = conn.cursor()
    curs.execute(input)
    return curs.fetchall()

# classes

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

    def do_memberLogin(username,password):
        """
        Allows existing members to login
        format: memberLogin <username> <password>
        """
        connectAndQuery(
                        """SELECT userid, password 
                        FROM members 
                        WHERE userid = """
                        + "'" + username + "'" +
                        """AND password = """
                        + "'" + password + "'"
                        )

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

print lm.cmdloop()

