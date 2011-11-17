

from helpers import *

ga = gatherer()

class Browse:
    global username
    def listSubjects(self):
        sql = "SELECT DISTINCT subject FROM bs_books"
        ds.execute(sql)
        rowCount = 0
        for row in ds:
            rowCount+=1
            print row

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
            if rowCount%2==0:
                putInCart = ga.getInput("Would you like to put either of these books in your cart? ('y' or 'n'): ","y|n$")
                if putInCart == 'y':
                    booksToBuy = ga.getInput("Type the ISBN number of the book you would like to purchase and then hit <Enter>: ", "[\dX]+$")
                    howMany = ga.getInput("How many copies do you want? ","\d+$")
                    ds.execute("INSERT INTO bs_cart VALUES (:userID,:isbnNumber,:amount)", userID=userLoggedIn, isbnNumber=booksToBuy, amount=howMany)
                else:
                    continue
        else:
            putInCart = ga.getInput("Would you like to put this in your cart? ('y' or 'n'): ","y|n$")
            if putInCart == 'y':
                booksToBuy = ga.getInput("Type the ISBN numberof the book you would like to purchase and then hit <Enter>: ", "[\dX]+$")
                howMany = ga.getInput("How many copies do you want? ","\d+$")
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