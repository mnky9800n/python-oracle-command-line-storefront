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
    lm.cmdloop()
    sm.cmdloop()