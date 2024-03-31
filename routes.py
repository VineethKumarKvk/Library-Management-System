from app import app
from models import *
from flask import request,jsonify
from flask_jwt_extended import jwt_required,create_access_token,get_jwt_identity,JWTManager
from werkzeug.security import check_password_hash,generate_password_hash

app.config['JWT_SECRET_KEY'] = 'thisisverysecret'
jwt = JWTManager(app)


#Write all routes here
