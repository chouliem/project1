import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Set up application
class Userinfo:
    def __init__(self, userId, userName, userPass):
        self.id = userId
        self.name = userName
        self.password = userPass


@app.route("/")
def index():
    message = " "
    return render_template("index.html", message=message)

@app.route("/loggedin", methods=["POST"])
def loggedin():
    username = request.form.get("name")
    userpass = request.form.get("password")
# checking if user exists and if exists check if password is matched
    matchuser = db.execute("select userid, username, userpass from userinfo where username = :username and userpass = :userpass", {"username": username, "userpass": userpass}).fetchone()
# print (f"{matchuser.userpass}")

    if matchuser == None:
        message = "Your username and password do not matched. Please try again."
        return render_template("index.html", message=message)
    else:
        return render_template("loggedin.html", name=username, password=userpass)


@app.route("/logout")
def logout():
    message = "You are logged out. Good Bye!"
    return render_template("index.html", message=message)

@app.route("/signup")
def signup():
    message = " "
    return render_template("signup.html", message=message)

@app.route("/signup2", methods=["POST"])
def signup2():
    username = request.form.get("name")
    userpass = request.form.get("password")
    # create new user
    db.execute("INSERT INTO userinfo (username, userpass) VALUES (:username, :userpass)",
        {"username": username, "userpass": userpass})
    db.commit()
    # print (f"{matchuser.userpass}")

    message = "You are signed up. Please Login"
    return render_template("index.html", message=message)

@app.route("/result", methods=["POST"])
def search():
    bkid = '%{}%'.format(request.form.get("bkid"))
    bktitle = '%{}%'.format(request.form.get("bktitle"))
    bkauthor = '%{}%'.format(request.form.get("bkauthor"))

    #querying database depends on user input
    results = db.execute("select * from bookinfo where bookisbn like :bookisbn and booktitle like :booktitle and bookauthor like :bookauthor",
            {"bookisbn": bkid, "booktitle": bktitle, "bookauthor":bkauthor}).fetchall()

    return render_template("result.html", results=results)

@app.route("/bookpage/<int:book_id>")
def bookpage(book_id):
    result = db.execute("select * from bookinfo where bookid = :bookid",
            {"bookid": book_id}).fetchone()

    return render_template("bookinfo.html", result=result)

@app.route("/searchagain")
def searchagain():
    message = " "
    return render_template("loggedin.html", message=message)
