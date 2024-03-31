from app import app
from flask_sqlalchemy import SQLAlchemy
import  os

basePath = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(basePath,'LibraryDb.db')
db = SQLAlchemy(app)

#write all the models here

