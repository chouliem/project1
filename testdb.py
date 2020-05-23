import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# class User:
#     def __init__(self, userId, userName, userPass):
#         self.id = userId
#         self.name = userName
#         self.password = userPass
#
# class Book:
#     def __init__(self, bookisbn, booktitle, bookauthor, bookyear):
#         self.isbn = bookisbn
#         self.title = booktitle
#         self.author = bookauthor
#         self.year = bookyear
#

def main():

    # username = 'hendry'
    # userpass = 'Ani'
    #
    # matchuser = db.execute("select userid, username, userpass from userinfo where username = :username and userpass = :userpass", {"username": username, "userpass": userpass}).fetchall()
#    print (f"{matchuser.userpass}")
    # print(matchuser)
    #
    # if len(matchuser) == 0:
    #    print ("no user is found")
    # else:
    #    print ("success")

# Part below to test database access for bookinfo
# Query base on ('0441012183', 'Dead to the World', 'Charlaine Harris', 2004)
#    bkid =''
    bkid = '%1012183%'
    bktitle = '%Dead%'
    bkauthor = '%Harris%'

#    print (bkid)
#   booktitle query
    # results = db.execute("select * from bookinfo where booktitle like :booktitle", {"booktitle": bktitle})
    # for result in results:
    #     print (result)

#   booktitle & bookauthor query
    results = db.execute("select * from bookinfo where booktitle like :booktitle and bookauthor like :bookauthor", {"booktitle": bktitle, "bookauthor":bkauthor}).fetchall()
    # for result in results:
    #     print (result)

#   bookisbn, booktitle & bookauthor query
    # results = db.execute("select * from bookinfo where bookisbn like :bookisbn and booktitle like :booktitle and bookauthor like :bookauthor", {"bookisbn": bkid, "booktitle": bktitle, "bookauthor":bkauthor}).fetchall()
    # for result in results:
    #     print (result)

#    results = db.execute("select * from bookinfo where bookisbn like :bookisbn and booktitle like :booktitle and bookauthor like :bookauthor", {"bookisbn": bkid, "booktitle": bktitle, "bookauthor":bkauthor}).fetchall()

    # for flight in flights
    #   print(f"{flight.origin} to {flight.destination}, {flight.duration} minutes.")

    for result in results:
#        print (f"ISBN : {result.bookisbn}, Title : {result.booktitle}, Author : {result.bookauthor}, Released year: {result.bookyear}")
        print (f"ID : {result.bookid}, ISBN : {result.bookisbn}, Title : {result.booktitle}, Author : {result.bookauthor}, Released year: {result.bookyear}")
    #conditional statements to search for particular input
    # if bkid != None:
    #     if bktitle != None:
    #         if bkauthor !=None:
    #            results = db.execute("select * from bookinfo where bookisbn like :bookisbn and booktitle like :booktitle and bookauthor like :bookauthor", {"bookisbn": bkid, "booktitle": bktitle, "bookauthor":bkauthor}).fetchall()
    #
    #         else:
    #
    #     else:
    #         if bkauthor !=None:
    #
    #         elif:
    #
    # elif
    #     if bktitle != None:
    #         if bkauthor !=None:
    #
    #         elif:
    #
    #     elif:
    #         if bkauthor !=None:
    #
    #         elif:
    #
    #
    # for result in results:
    #     print (result)



if __name__ == "__main__":
    main()
