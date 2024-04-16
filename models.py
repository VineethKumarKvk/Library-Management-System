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
    categoriesAvaliable = db.relationship('BookCategory',backref='locationDetails')

class BookCategory(db.Model):
    categoryID = db.Column(db.Integer,primary_key=True)
    categoryName = db.Column(db.String)
    rackID = db.Column(db.Integer,db.ForeignKey('book_location.rackID'),default=0)
    booksPresent = db.relationship('Books',backref='categoryDetails')

class Books(db.Model):
    bookID = db.Column(db.Integer,primary_key=True,autoincrement=True)
    bookName = db.Column(db.String)
    bookCategory = db.Column(db.String,db.ForeignKey('book_category.categoryID'))
    currentOwner = db.relationship('Users')

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
    booksAssigned = db.Column(db.Integer,db.ForeignKey('books.bookID'))

class Status(db.Model):
    statusID = db.Column(db.Integer,primary_key=True)
    statusName = db.Column(db.String)

class BookRequests(db.Model):
    requestID = db.Column(db.Integer,primary_key=True)
    requestedUserID = db.Column(db.Integer,db.ForeignKey('users.userID'))
    requestedBook = db.Column(db.Integer,db.ForeignKey('books.bookID'))
    status = db.Column(db.Integer,db.ForeignKey('status.statusID'))
    comment = db.Column(db.String,default='No comments Provided')

class AvailableBooks(db.Model):
    bookID = db.Column(db.Integer,primary_key=True,autoincrement=True)
    bookName = db.Column(db.String)
    bookCategory = db.Column(db.String,db.ForeignKey('book_category.categoryID'))

class AssignedBooks(db.Model):
    bookID = db.Column(db.Integer,primary_key=True,autoincrement=True)
    bookName = db.Column(db.String)
    bookCategory = db.Column(db.String,db.ForeignKey('book_category.categoryID'))
    currentBookOwner = db.Column(db.Integer,db.ForeignKey('users.userID'))