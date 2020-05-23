import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for bkid, bktitle, bkauthor, bkyear in reader:
        db.execute("INSERT INTO bookinfo (bookisbn, booktitle, bookauthor, bookyear) VALUES (:bookisbn, :booktitle, :bookauthor, :bookyear)",
                    {"bookisbn": bkid, "booktitle": bktitle, "bookauthor": bkauthor, "bookyear": bkyear})
        print(f"Added book from {bkid}, {bktitle}, {bkauthor}, {bkyear}.")
    db.commit()

if __name__ == "__main__":
    main()
