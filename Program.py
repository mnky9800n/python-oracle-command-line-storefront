#
#
#  Author: John Aiken
#
# TODO
# 

from helpers import *
from menus import *

lm = loginMenu()
sm = storeMenu()

while True:
    while lm.cmdloop()==True:
        pass
    while sm.cmdloop()==True:
        pass

