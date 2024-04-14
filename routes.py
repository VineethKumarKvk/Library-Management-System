from app import app
from models import *
from flask import request,jsonify
from flask_jwt_extended import jwt_required,create_access_token,get_jwt_identity,JWTManager
from werkzeug.security import check_password_hash,generate_password_hash

app.config['JWT_SECRET_KEY'] = 'thisisverysecret'
jwt = JWTManager(app)


#Write all routes here

@app.route('/login',methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    existingUser = Users.query.filter_by(emailID=email).first()
    if(existingUser):
        if(check_password_hash(existingUser.password,password)):
            token = create_access_token(identity=existingUser.emailID)
            return jsonify(token=token)
        return '',403
    return '',404

@app.route('/register',methods=['POST'])
def register():
    email = request.json['email']
    password = request.json['password']
    username = request.json['username']
    role = request.json['role']
    existingUser = Users.query.filter_by(emailID=email).first()
    if(not existingUser):
        newUser = Users(emailID=email,password=generate_password_hash('1234',method='pbkdf2:SHA256',salt_length=3),userName=username,role=role)
        db.session.add(newUser)
        db.session.commit()
        return jsonify(success='User Added'),201
    return 'User already existed please login using your credentials',409


@app.route('/getAllBooks',methods=['GET'])
def get_all_books():
    existingBooks = db.session.query(Books,BookCategory).join(BookCategory,Books.bookCategory == BookCategory.categoryID).all()
    output = []
    
    if(existingBooks):
        for book,category in existingBooks:
            output.append({'Book Name':book.bookName,'Category':category.categoryName})
        return jsonify(output)
    
    return 'No books found',404

