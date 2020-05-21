import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

class User:
    def __init__(self, userId, userName, userPass):
        self.id = userId
        self.name = userName
        self.password = userPass


def main():

    username = 'Hendry'
    userpass = 'Ani'

    matchuser = db.execute("select userid, username, userpass from userinfo where username = :username", {"username": username}).fetchone()
    print (f"{matchuser.userpass}")

    if matchuser.userpass == userpass:
       print ("user is match")
    else:
       print ("failed")

if __name__ == "__main__":
    main()
