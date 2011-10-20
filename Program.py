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

import cmd, cx_Oracle, sys, re

# functions

def connectToDatabase(input,outputYorN):
    #_connstr = "wouldn't you like to know"
    
    conn = cx_Oracle.connect(_connstr)
    conn.autocommit = 1
    curs = conn.cursor()
    curs.execute(input)
    if outputYorN == 'Y':
        return curs.fetchall()
    elif outputYorN == 'N':
        pass
    else:
        print "Please use 'Y' or 'N' to decide the output"

def cleanNewMemberInfo(inputRequest,regex,replace):
    """This method validates data"""
    while True:
        try:
            userData = raw_input(inputRequest)
            cleanData = re.sub(regex,replace,userData.strip())
            return cleanData
            break
        except ValueError, other:
            print 'This is invalid data.  Please try again.'



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

        connectAndCheck = connectToDatabase(sql, 'Y')

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
        
        # regex = "'<regex>','<replace>'"        
        regexstr = "'[\s\d][\s\d]*'"
        replacestr = "''"
        userFirstName = cleanNewMemberInfo('Enter first name: ',regexstr,replacestr)
        userLastName = cleanNewMemberInfo('Enter last name: ',regexstr,replacestr)

        regexstr = "'[\s\s*]'"
        replacestr = ''
        streetAddress = cleanNewMemberInfo('Enter street address: ',regexstr,replacestr)

        regexstr = "'[\s\d][\s\d]*'"
        replacestr = ''
        userCity = cleanNewMemberInfo('Enter city: ',regexstr,replacestr)
        userState = cleanNewMemberInfo('Enter state: ',regexstr,replacestr)

        regexstr = "'[\s\D]*'"
        replacestr = ''
        userZip = cleanNewMemberInfo('Enter zip code: ',regexstr,replacestr)
        regexstr = "'[\s\D-]*'"
        userPhone = cleanNewMemberInfo('Enter phone: ',regexstr,replacestr)
        regexstr = "'[\s\d][\s\d]*'"
        userEmail = cleanNewMemberInfo('Enter email: ',regexstr,replacestr)
        userID = cleanNewMemberInfo('Enter userID: ',regexstr,replacestr)
        userPassword = cleanNewMemberInfo('Enter password: ',regexstr,replacestr)

        while True:
            try:
                userInput = raw_input("Do you want to store credit card information(y/n): ')
                # regexstr, replacestr
                userCreditType = cleanNewMemberInfo('Enter type of credit card(amex/visa): ',regexstr,replacestr)
                # regexstr, replacestr
                try:
                    userCreditCardNumber = cleanNewMemberInfo('Enter credit card number: ',regexstr,replacestr)
                    # regex that counts for 15 digits /^([\d]*){16}


            except userInput != 'y':
                break



        print userFirstName + userLastName + streetAddress

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

# program

lm = loginMenu()
sm = storeMenu()

print lm.cmdloop()

