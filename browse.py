

from helpers import *

ds = dataSet("jaiken1/jaiken1@tinman.cs.gsu.edu:1522/tinman")
ga = gatherer()

class Browse:
    global username
    def listSubjects(self):
        sql = "SELECT DISTINCT subject FROM bs_books"
        ds.execute(sql)
        rowCount = 0
        print """
============
= Subjects =
============
"""
        for row in ds:
            print ''.join(row)
            rowCount+=1
        print ""
        

    def printBooksInSubject(self,input,userLoggedIn):
        sql = "SELECT distinct subject FROM bs_books WHERE subject = :userSubject"
        ds.execute(sql,userSubject=input)
        for row in ds:
            sql = "SELECT title, author, price, isbn FROM bs_books WHERE subject = :userSubject"
            ds.execute(sql,userSubject=input)
            rowCount = 0
            for row in ds:
                print ''
                print 'Title: ' + row[0]
                print 'Author: ' + row[1]
                print 'Price: ' + str(row[2])
                print 'ISBN: ' + row[3]
                print ''
                rowCount+=1

    #This is only for subjects with more than one book in the table

                if rowCount%2==0:
                    putInCart = ga.getInput("Would you like to put either of these books in your cart? ('y' or 'n', press 'x' to go back to store menu): ","y|n|x$")
                    if putInCart == 'y':
                        booksToBuy = ga.getInput("Type the ISBN number of the book you would like to purchase and then hit <Enter>: ", "[\dX]+$")
                        howMany = ga.getInput("How many copies do you want? ","\d+$")
                        ds.execute("INSERT INTO bs_cart VALUES (:userID,:isbnNumber,:amount)", userID=userLoggedIn, isbnNumber=booksToBuy, amount=howMany)
                        break
                    if putInCart == 'x':
                        break
                    else:
                        continue

    #This is necessary because there may be n<2 books in a particular subject

            else:
                putInCart = ga.getInput("Would you like to put this in your cart? ('y' or 'n'): ","y|n$")
                if putInCart == 'y':
                    booksToBuy = ga.getInput("Type the ISBN numberof the book you would like to purchase and then hit <Enter>: ", "[\dX]+$")
                    howMany = int(ga.getInput("How many copies do you want? ","\d+$"))
                
    #if the book is already in the cart for the user just add another copy of the book for the user

                    sql = """
    BEGIN
        UPDATE bs_cart
            SET qty = qty + :moreBooks
            WHERE userid = :userID 
            AND isbn = :bookNumber;

        IF SQL%ROWCOUNT = 0 THEN
            INSERT INTO bs_cart (userid,isbn,qty)
            VALUES (:userID,:bookNumber,:moreBooks);
        END IF;
    END;
    """

                    ds.execute(sql,moreBooks=howMany,userID=userLoggedIn,bookNumber=booksToBuy)
            break
        else:
            print "That subject does not exist."

#just in case you need to know what is in your cart
    def printCart(self, userid):
        sql = "select bs_books.title, bs_books.price, bs_cart.qty from bs_books JOIN bs_cart ON bs_cart.isbn = bs_books.isbn JOIN bs_members ON bs_members.userid = bs_cart.userid where bs_members.userid = :username"
        ds.execute(sql,username=userid)
        rowCount=0
        print 'Your cart contains: '
        for row in ds:
            rowCount+=1
            print ''
            print 'Title: ' + row[0]
            print 'Price: ' + str(row[1])
            print 'Quantity: ' + str(row[2])
            print ''
        
        totalSql = "select sum(bs_cart.qty*bs_books.price) as totalCost from bs_books join bs_cart on bs_cart.isbn=bs_books.isbn where userid=:username"
        ds.execute(totalSql,username=userid)

        rowCount=0
        for row in ds:
            print 'Total: $' + str(row[0])