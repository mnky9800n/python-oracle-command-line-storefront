

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
            print row
            rowCount+=1

    def printBooksInSubject(self,input,userLoggedIn):
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
                putInCart = ga.getInput("Would you like to put either of these books in your cart? ('y' or 'n'): ","y|n$")
                if putInCart == 'y':
                    booksToBuy = ga.getInput("Type the ISBN number of the book you would like to purchase and then hit <Enter>: ", "[\dX]+$")
                    howMany = ga.getInput("How many copies do you want? ","\d+$")
                    ds.execute("INSERT INTO bs_cart VALUES (:userID,:isbnNumber,:amount)", userID=userLoggedIn, isbnNumber=booksToBuy, amount=howMany)
                else:
                    continue

#This is necessary because there may be n<2 books in a particular subject

        else:
            putInCart = ga.getInput("Would you like to put this in your cart? ('y' or 'n'): ","y|n$")
            if putInCart == 'y':
                booksToBuy = ga.getInput("Type the ISBN numberof the book you would like to purchase and then hit <Enter>: ", "[\dX]+$")
                howMany = ga.getInput("How many copies do you want? ","\d+$")

#if the book is already in the cart for the user just add another copy of the book for the user

                if ds.execute('select qty from bs_cart where userid = :userID and isbn = :bookNumber',userID=userLoggedIn,bookNumber=booksToBuy)>0:
                    ds.execute("UPDATE bs_cart SET bs_cart.qty = bs_cart.qty + :amount WHERE bs_cart.userid = :userID and bs_cart.isbn = :bookNumber",amount=howMany, userID=userLoggedIn,bookNumber=booksToBuy)

                else:
                    ds.execute("INSERT INTO bs_cart VALUES (:userID,:isbnNumber,:amount)", userID=userLoggedIn, isbnNumber=booksToBuy, amount=howMany)

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