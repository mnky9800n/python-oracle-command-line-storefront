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

ds = dataSet("jaiken1/jaiken1@tinman.cs.gsu.edu:1522/tinman")

lm = loginMenu()
sm = storeMenu()

print lm.cmdloop()

