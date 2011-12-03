
from helpers import *
from menus import *

ds = dataSet("jaiken1/jaiken1@tinman.cs.gsu.edu:1522/tinman")
ga = gatherer()

# checkout

class checkOut:
    
    def __init__(self):
        self.orderNumber = None
        self.cartIsEmpty = True
 #   def __iter__(self):
 #       return self.orderNumber

    global username
    def oneClick(self,userLoggedIn):

        #this checks if there is a credit card available, if there isn't it denies one click check out
        sql = """
SELECT creditcardnumber, creditcardtype
    FROM bs_members
    WHERE userid = :userid
        """
        ds.execute(sql,userid=userLoggedIn)

        for row in ds:
            if row == (None,None):
                print """
One click check out is not available if you do not have a credit card on file.
    """
                
            else:
                break

        #this checks to see if the user has anything in the cart
        cartSql = """
SELECT userid FROM bs_cart WHERE userid = :userid
        """
        ds.execute(cartSql,userid=userLoggedIn)

        #this places the contents of the cart into the order tables
        insertSql = """
    BEGIN
        INSERT INTO bs_orders (userid, ono, timePurchased)
            VALUES (:userid, orderNum_seq.NEXTVAL,(SELECT current_timestamp FROM dual));

        COMMIT;

        UPDATE bs_orders
            SET shipaddress = (SELECT address FROM bs_members WHERE userid = :userid)
                , shipcity = (SELECT city FROM bs_members WHERE userid = :userid)
                , shipstate = (SELECT state FROM bs_members WHERE userid = :userid)
                , shipzip = (SELECT zip FROM bs_members WHERE userid = :userid)
            WHERE userid = :userid
            AND timePurchased IN 
                (
                SELECT MAX(timePurchased)
                    FROM bs_orders
                    WHERE userid = :userid
                    GROUP BY userid
                );

        INSERT INTO bs_odetails (ono, isbn, qty, price)
            SELECT orderNum_seq.CURRVAL, bs_cart.isbn, bs_cart.qty, bs_books.price
                FROM bs_orders, bs_cart, bs_books
                WHERE bs_orders.userid = :userid
                AND bs_cart.userid = :userid
                AND bs_books.isbn = bs_cart.isbn;

        DELETE FROM bs_cart
            WHERE userid = :userid;
    END;
            """
            

        #if the cart has contents this for loop is executed
        for row in ds:
            ds.execute(insertSql,userid=userLoggedIn)
            sql = """
    SELECT ono
        FROM bs_orders
        WHERE userid = :userid
        AND timePurchased IN
            (
            SELECT MAX(timePurchased)
                FROM bs_orders
                WHERE userid = :userid
                GROUP BY userid
            )
            """

            ds.execute(sql,userid=userLoggedIn)
            for row in ds:
                self.orderNumber = ''.join(str(i) for i in row)
                self.cartIsEmpty = False
            break
        
        #if the cart does not have any contents the user is told to try again
        else:
            print """
You have nothing in your cart!
                """
            self.cartIsEmpty = True
        


    def printReceipt(self,userLoggedIn,userOno):

        #
        # group by order number so that receipts can be separated 
        # make totals match each receipt
        #
        #

        print """
===============================================================================
=                                                                             =
=                                  Receipt                                    =
=                                                                             =
===============================================================================
-------------------------------------------------------------------------------
ISBN        Title                                                $  Qty   Total
-------------------------------------------------------------------------------"""
        sql = """
SELECT bs_books.isbn, bs_books.title, CAST(bs_odetails.qty AS varchar(50)), CAST((bs_odetails.qty*bs_odetails.price) AS varchar(50)) as total
    FROM bs_odetails
    JOIN bs_books
    ON bs_books.isbn = bs_odetails.isbn
    JOIN bs_orders
    ON bs_orders.ono = bs_odetails.ono
    WHERE userid = :userid
    AND bs_orders.ono = :orderNumber
    ORDER BY bs_orders.ono
"""
        ds.execute(sql,userid=userLoggedIn,orderNumber=userOno)
        for row in ds:
            print '   '.join(row)

        sql = """
SELECT CAST(SUM(qty*price) AS varchar(50))
    FROM bs_odetails
    WHERE bs_odetails.ono = :orderNumber
    """
        ds.execute(sql, orderNumber=userOno)
        for row in ds:
            print "Total: " + ''.join(row)

    def bigCheckOut(self, username):

        sql = """
        BEGIN

        IF :shipAddressExists = 'y' THEN
            UPDATE bs_members
            SET address = :address
            ,city = :city
            ,state = :state
            ,zip = :zip
            WHERE userid = :userid;
        END IF;

        IF :creditCardupdate = 'y' THEN
            UPDATE bs_members
            SET creditcardtype = :cctype
            ,creditcardnumber = :ccnumber
            WHERE userid = :userid;
        END IF;

        END;
        """
        class userNewInfo:
            def __init__(self):
                self.cctype = None
                self.ccnumber = None
                self.city = None
                self.state = None
                self.streetAddress = None
                self.zipCode = None

        userInfo = userNewInfo()
        userInfo.CCupdate = ga.getInput("Would you like to update your creditcard ('y' or 'n')? ", "y|n$")
        if userInfo.CCupdate == 'y':
            userInfo.ccnumber = ga.getInput("Please enter the new CC Number: ","\d{16}$")
            userInfo.cctype = ga.getInput("Please enter type ('visa' or 'amex'): ", "amex|visa$")

        userInfo.shipUpdate = ga.getInput("Would you like to update your shipping address ('y' or 'n')? ", "y|n$")
        if userInfo.shipUpdate == 'y':
            userInfo.streetAddress = ga.getInput('Enter street address: ', "[\w\s]+$")
            userInfo.city = ga.getInput('Enter city: ', "[a-zA-Z ']+$")
            userInfo.state = ga.getInput('Enter state abbreviation: ', "\w{2}$")
            userInfo.zipCode = ga.getInput('Enter zip code: ', "^\d{5}(-\d{4})?$")
        if userInfo.CCupdate == 'y' or userInfo.shipUpdate == 'y':
            ds.execute(sql, userid=username,shipAddressExists=userInfo.shipUpdate,creditCardupdate=userInfo.CCupdate, cctype=userInfo.cctype, ccnumber=userInfo.ccnumber,address=userInfo.streetAddress,city=userInfo.city,state=userInfo.state,zip=userInfo.zipCode)

