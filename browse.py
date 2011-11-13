

from helpers import *

import cx_Oracle

ds = dataSet()
ga = gatherer()

class Browse:
    def listSubjects():
        sql = "SELECT DISTINCT subject FROM bs_books"
        ds.execute(sql)
        rowCount = 0
        for row in ds:
            rowCount+=1
            print row

    def printBooksInSubject(self,input,user):
        sql = "SELECT title, author, price, isbn FROM bs_books WHERE subject = :userSubject"
        ds.execute(sql,userSubject=input)
        rowCount = 0
        for row in ds:
            print row
            rowCount+=1
            if rowCount%2==0:
                putInCart = ga.getInput("Would you like to put either of these books in your cart? ('y' or 'n'): ","y|n$")
                if putInCart == 'y':
                    booksToBuy = ga.getInput("Type the ISBN number you would like to purchase and then hit <Enter>: ", "\dX+$")
                    howMany = ga.getInput("How many copies do you want? ","\d+$")
                    ds.execute("INSERT INTO bs_cart VALUES (:userID,:isbnNumber,:amount)", userID=user, isbnNumber=booksToBuy, amount=howMany)
                else:
                    continue