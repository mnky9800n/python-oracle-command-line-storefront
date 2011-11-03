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

while True:
    while lm.cmdloop()==True:
        pass
    while sm.cmdloop()==True:
        pass

