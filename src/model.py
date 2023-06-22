from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os
APP = Flask(__name__)
APP.app_context().push()
# APP.config.from_object("config")
db_url = os.getenv('DATABASE_URL','postgres://admin:cDIhaMPJDvfyPdVKHN3zmjvZf9DP1svG@dpg-ci81v76nqql0ldf4vrdg-a/librarydb_500r')
APP.config["SQLALCHEMY_DATABASE_URI"]  = db_url
APP.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(APP)

migrate = Migrate(APP, db, render_as_batch=False)


class Books(db.Model):
    __tablename__="book"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(120))
    numbers_in_stock = db.Column(db.Integer, default=1)
    add_date = db.Column(db.String(120))
    days_for_borrow = db.Column(db.Integer, nullable=False, default=30)
    genres = db.Column(db.String(120))
    pages = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    status = db.Column(db.String(30), default='available')
    author_gender = db.Column(db.String(30))
    author_country = db.Column(db.String(80))
    def __repr__(self):
        return f"<Book: {self.id}, Title: {self.title}>"
    def short(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author
        }
    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'add_date': self.add_date,
            'in_stock': self.numbers_in_stock,
            'genres': self.genres,
            'pages': self.pages,
            'status':self.status,
            'days_for_borrow':self.days_for_borrow
        }
class Author(db.Model):
    __tablename__="author"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(50))
    country = db.Column(db.String(80))
    books_in_lib = db.Column(db.Integer)
    book_a = db.relationship('Books',backref='_author',lazy=True)
    def __repr__(self):
        return f"<Author: {self.id}, Name: {self.name}>"
    
    
class Patrons(db.Model):
    __tablename__="patron"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    date_of_birth = db.Column(db.String(80))
    gender = db.Column(db.String(20))
    address = db.Column(db.String(120))
    books_borrowed = db.Column(db.Integer)
    membership_time = db.Column(db.String(120))
    books_borrowing = db.Column(db.Integer)
    def __repr__(self):
        return f"Patron: {self.id} - Name: {self.name}"

book_lends = db.Table('book_loan_ticket', 
    db.Column('id', db.Integer, primary_key=True),
    db.Column('book_id',db.Integer, db.ForeignKey('book.id'),primary_key=True),
    db.Column('patron_id',db.Integer, db.ForeignKey('patron.id'),primary_key=True),
    db.Column('time_lend',db.String(80), default=datetime.now().strftime("%Y/%m/%d")),
    db.Column('return_date', db.String(80)),
    db.Column('status',db.String(80),default='active')
    )
