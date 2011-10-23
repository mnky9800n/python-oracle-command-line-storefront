#
#
#  Author: John Aiken
#
# TODO
# 

from helpers import *
from menus import *
import cmd, cx_Oracle, sys, re


# functions

# classes

# program

lm = loginMenu()
sm = storeMenu()

# this needs to check if lm should be used or sm should
# be used.
#

quit = False

while True:
    lm.cmdloop()
    if ga.getInput('Are you sure you want to exit (type y or n): ', "(y|n)") == 'y':
        quit = True
        break
while quit == False:
    sm.cmdloop()