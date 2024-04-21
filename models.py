from app import app
from flask_sqlalchemy import SQLAlchemy
import  os

basePath = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(basePath,'LibraryDb.db')
db = SQLAlchemy(app)

#write all the models here
class BookLocation(db.Model):
    rackID = db.Column(db.Integer,primary_key=True)
    floorName = db.Column(db.String)

class BookCategory(db.Model):
    categoryID = db.Column(db.Integer,primary_key=True)
    categoryName = db.Column(db.String)
    booksPresent = db.relationship('Books',backref='categoryDetails')

class Status(db.Model):
    statusID = db.Column(db.Integer,primary_key=True)
    statusName = db.Column(db.String)

class Books(db.Model):
    bookID = db.Column(db.Integer,primary_key=True,autoincrement=True)
    bookName = db.Column(db.String)
    bookCategory = db.Column(db.String,db.ForeignKey('book_category.categoryID'))
    status = db.Column(db.Integer,db.ForeignKey('status.statusID'),default=0)
    rack = db.Column(db.Integer,db.ForeignKey('book_location.rackID'))
    borrowerID = db.Column(db.Integer,db.ForeignKey('users.userID'))

class Roles(db.Model):
    roleID = db.Column(db.Integer,primary_key=True)
    roleName = db.Column(db.String,unique=True)
    colleagues = db.relationship('Users',backref='roleDetails')

class Users(db.Model):
    userID = db.Column(db.Integer,primary_key=True,autoincrement=True)
    userName = db.Column(db.String)
    emailID = db.Column(db.String,unique=True)
    password = db.Column(db.String)
    role = db.Column(db.Integer,db.ForeignKey('roles.roleID'))

class BookRequests(db.Model):
    requestID = db.Column(db.Integer,primary_key=True)
    requestedUser = db.Column(db.Integer,db.ForeignKey('users.userID'))
    requestedBook = db.Column(db.Integer,db.ForeignKey('books.bookID'))
    requestStatus = db.Column(db.Integer,db.ForeignKey('status.statusID'))

class AvailableBooks(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    bookID = db.Column(db.Integer,db.ForeignKey('books.bookID'),unique=True)

class AssignedBooks(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    requestID = db.Column(db.Integer,db.ForeignKey('book_requests.requestID'))
    bookID = db.Column(db.Integer,db.ForeignKey('books.bookID'),unique=True)