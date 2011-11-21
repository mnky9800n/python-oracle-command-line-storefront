
from helpers import *
from menus import *

ds = dataSet("jaiken1/jaiken1@tinman.cs.gsu.edu:1522/tinman")
ga = gatherer()

class checkOut:
    def oneClick(self,person):
        global username
        #global username
        #userLoggedIn = username
        #needs to insert into odetails and orders the delete the values in cart

        # check for cart contents, if empty report back cart is empty
        insertSql = """
        INSERT INTO bs_orders (userid, ono)
        VALUES (:user, bs_orders_orderNumber.nextval);

        INSERT INTO bs_orders (shipaddress, shipcity, shipstate, shipzip)
        SELECT m.address, m.city, m.state, m.zip
        FROM bs_cart as c
        JOIN bs_members as m
        WHERE userid = :user;

        INSERT INTO bs_odetails (ono, isbn, qty, price)
        SELECT o.ono, c.isbn, c.qty, b.price
        FROM bs_orders as o
        JOIN bs_cart as c
        JOIN bs_books as b
        WHERE c.userid = :user
        """
        ds.execute(insertSql,user=username)

        sql = """
        SELECT b.title, o.qty, b.price
        FROM bs_odetails as o
        JOIN bs_books as b
        JOIN bs_orders as ord
        """
        print "RECEIPT"
        print "ships to your mom"
        