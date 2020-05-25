import os
import requests

from flask import Flask, session, render_template, request, jsonify
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

class Bookinfo:
    def __init__(self, id, isbn, title, author, year, review, averating, numberofreviewer):
        self.id = id
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.review = review
        self.averating = averating
        self.numberofreviewer = numberofreviewer


@app.route("/")
def index():
    message = " "
    return render_template("index.html", message=message)

@app.route("/loggedin", methods=["POST", "GET"])
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
        if session.get("loggedinusers") is None:
            session["loggedinusers"] = []
        if request.method == "POST":
            user = matchuser.userid
            session["loggedinusers"].append(user)
            # session["loggedinusers"] = user

        return render_template("loggedin.html", name=username, password=userpass, id=matchuser.userid)

#Route for logging out
@app.route("/logout")
def logout():
    session.pop("loggedinusers", None)
    message = "You are logged out. Good Bye!"
    return render_template("index.html", message=message)

#Route for signing up
@app.route("/signup")
def signup():
    message = " "
    return render_template("signup.html", message=message)

#Signed up and input user data into database
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

#shows book search
@app.route("/result", methods=["POST"])
def search():
    bkid = '%{}%'.format(request.form.get("bkid"))
    bktitle = '%{}%'.format(request.form.get("bktitle"))
    bkauthor = '%{}%'.format(request.form.get("bkauthor"))

    #querying database depends on user input
    results = db.execute("select * from bookinfo where bookisbn like :bookisbn and booktitle like :booktitle and bookauthor like :bookauthor",
            {"bookisbn": bkid, "booktitle": bktitle, "bookauthor":bkauthor}).fetchall()
    count = db.execute("select * from bookinfo where bookisbn like :bookisbn and booktitle like :booktitle and bookauthor like :bookauthor",
            {"bookisbn": bkid, "booktitle": bktitle, "bookauthor":bkauthor}).rowcount

    if count == 0:
        message = "Nothing is found. Please try again"
        return render_template("loggedin.html", message=message)
    else:
        return render_template("result.html", results=results)

@app.route("/bookpage/<int:book_id>")
def bookpage(book_id):
    result = db.execute("select * from bookinfo where bookid = :bookid",
            {"bookid": book_id}).fetchone()

    #getting book data from goodreads.com
    url="https://www.goodreads.com/book/review_counts.json"
    params = {"key": "kCOIhaJM9idAhbeuVWOXeA", "isbns": "0441018645"}
    params["isbns"]=result.bookisbn
    res=requests.get(url,params=params)
    if res.status_code != 200:
        raise Exception ("Error: API request unsuccesful")

    averating = res.json()["books"][0]["average_rating"]
    ratingcount = res.json()["books"][0]["ratings_count"]

    return render_template("bookinfo.html", result=result, averating=averating, ratingcount=ratingcount)

@app.route("/searchagain")
def searchagain():
    message = " "
    return render_template("loggedin.html", message=message)


@app.route("/ratebook/<int:book_id>", methods=["POST"])
def ratebook(book_id):
    userrate = request.form.get("userrate")
    userreview = request.form.get("userreview")
    userid = session["loggedinusers"][0]

    #make sure book requested information is in my system.
    result = db.execute("select * from bookinfo where bookid = :bookid",
            {"bookid": book_id}).rowcount

    if result == 1:
        #check if a particular user had reviewed a particular book, if he had then can't review again, else he will review the book.
        reviewed = db.execute("select * from bkreview where book_id = :book_id and reviewby = :userid", {"book_id": book_id, "userid": userid}).rowcount

        if reviewed == 0:
            db.execute("INSERT INTO bkreview (book_id, review, starred, reviewby, starredby) VALUES (:book_id, :review, :starred, :reviewby, :starredby)",
                {"book_id": book_id, "review": userreview, "starred": userrate, "reviewby": userid, "starredby": userid})
            db.commit()
            message = "Thank you for the review"
        else:
            message = "Sorry you had reviewed this book previously"
    # message = (f"{userrate} and {userreview} and {userid}")
    return render_template("loggedin.html", message=message)

@app.route("/api/<string:isbn>")
def book_api(isbn):
    #makesure book data exists in database

    count = db.execute("select bookisbn from bookinfo where bookisbn = :bookisbn",
            {"bookisbn": isbn}).rowcount
    if count == 0:
        return jsonify({"error": "Invalid ISBN"}), 422

    result = db.execute("select * from bookinfo where bookisbn = :bookisbn",
            {"bookisbn": isbn}).fetchone()

    #getting book data from goodreads.com
    url="https://www.goodreads.com/book/review_counts.json"
    params = {"key": "kCOIhaJM9idAhbeuVWOXeA", "isbns": "0441018645"}
    params["isbns"]=result.bookisbn
    res=requests.get(url,params=params)
    if res.status_code != 200:
        raise Exception ("Error: API request unsuccesful")

    averating = res.json()["books"][0]["average_rating"]
    ratingcount = res.json()["books"][0]["ratings_count"]

    return jsonify({
        "title": result.booktitle,
        "author": result.bookauthor,
        "year": result.bookyear,
        "isbn": result.bookisbn,
        "review_count": ratingcount,
        "average_score": averating
    })
