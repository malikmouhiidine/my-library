# My Library

a Flask web-based application that helps the user to organize and put his or her books in one place,

## Description

helps the user to organize and put his or her books in one place but instead
of the hall file he can just give the link that reaches the book, and he got on the home page a list of all the books that he added and can add how many he likes of books and can delete
any book that no more needs plus this site allow the user to search for a book title and it (the site) give him the description and the infolink and he can add it to his homepage (list) plus this site allow the user to register and logging in and logging out whatever he likes without losing any data.

## Getting Started

### Libraries and prerequisites

* `pip install` these libraries.
  * `pip install os`
  * `pip install datetime`
  * `pip install cs50`
  * `pip install flask`
  * `pip install Flask-Session`
  * `pip install tempfile2`
  * `pip install Werkzeug`

### Running the Flask web-based application

* Create a `library.db` database in the same directory of the project
* Create a users table \
                        ```
                            CREATE TABLE IF NOT EXISTS "users" (
                                    "id"    INTEGER NOT NULL,
                                    "username"      TEXT NOT NULL,
                                    "hash"  TEXT NOT NULL,
                                    PRIMARY KEY("id" AUTOINCREMENT)
                            );
                        ```
* Create a books table \
                        ```
                            CREATE TABLE IF NOT EXISTS "books" (
                                    "id"    INTEGER NOT NULL,
                                    "title" TEXT NOT NULL,
                                    "url"   TEXT NOT NULL,
                                    "description"   TEXT NOT NULL
                            , "date"        NUMERIC NOT NULL);
                        ```
* Get an [google books api](https://developers.google.com/books/docs/v1/getting_started) and set it as an envirement variable as `API_KEY` to enable the search feature
* use `Flask run`  command to run the project

## Authors

Malik Mouhiidine
[@MMouhiidine](https://twitter.com/MMouhiidine)
