# project1
Project1 for CS50 - Build an online review website
Link to screencast - https://youtu.be/dzOPtqj2tk0

1. Registration - take username and password from user and create user in the database. (Done)
2. Login - take username and password from user, verify that the username and password are match, if match session id is set and user is allowed inside the application. If username and password does not match or come back with no result, the user is asked to retry again. (Done)
3. Logout - Once logout button is pressed, session will be cleared, and user will be taken back to login page. (Done)
4. Import - importing books data into the database. (Done)
5. Search - the site is able to search for any keyword given, if the result is found, the site will list all the matching book title. If nothing is found then the site will ask the user to put different keyword.
The only problem I found is capital letter or small letter make a difference in search result. But I think this is outside of the scope of this project. (Done)
6. Book Page - Once the user click on one of the search result link, the user will be taken to that particular book information page. Book page is showing, Book title, author, isbn number, released year, and book rating. It also let the user put rating and review that particular book. (Done)
7. Review Submission - in book page, user will be able to review and rate books and submit into the database. (Done)
8. Goodreads Review Data - review data from Goodreads is showing up in book page, along with all the data from our database. (Done)
9. API Access: - when a user is requesting API access through a browser the user just need to put in "http:\\address\api\isbn" in the address bar.

The way database is set up, it has 3 tables
1. userinfo : has 3 columns, userid, username and userPass
2. bookinfo : has 5 columns, bookid, bookisbn, booktitle, bookauthor, and bookyear
3. bkreview : has 6 columns, id, book_id, review, starred, reviewby, starredby. book_id is used as foreign key in reference to bookinfo table. review and starred are used for reviewing and rating book. reviewby and starredby are used as placeholder for user that give rating and review to that particular book.
