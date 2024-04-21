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
    email = request.form['email']
    password = request.form['password']
    existingUser = Users.query.filter_by(emailID=email).first()
    if(existingUser):
        if(check_password_hash(existingUser.password,password)):
            token = create_access_token(identity=existingUser.emailID)
            return jsonify(token=token),200
        return '',403
    return '',404

@app.route('/register',methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    username = request.form['username']
    role = request.form['role']
    existingUser = Users.query.filter_by(emailID=email).first()
    if(not existingUser):
        newUser = Users(emailID=email,password=generate_password_hash('1234',method='pbkdf2:SHA256',salt_length=3),userName=username,role=role)
        db.session.add(newUser)
        db.session.commit()
        return jsonify(success='User Added'),201
    return 'User already existed please login using your credentials',409


@app.route('/getAllBooks',methods=['GET'])
def get_all_books():
    existingBooks = db.session.query(Books,BookCategory,Status).join(BookCategory,Books.bookCategory == BookCategory.categoryID)\
                                                                .join(Status,Books.status == Status.statusID).all()
    output = []
    
    if(existingBooks):
        for book,category,status in existingBooks:
            output.append({'Book Name':book.bookName,'Category':category.categoryName,'Status':status.statusName})
        return jsonify(output),200
    
    return 'No books found',404

@app.route('/getAvailableBooks',methods=['GET'])
def get_available_books():
    existingBooks = db.session.query(AvailableBooks,Books,BookCategory).join(Books,Books.bookID == AvailableBooks.bookID)\
                                                                        .join(BookCategory,Books.bookCategory == BookCategory.categoryID).all()
    output = []
    
    if(existingBooks):
        for availableBook,book,category in existingBooks:
            output.append({'Book ID':availableBook.bookID,'Book Name':book.bookName,'Category':category.categoryName})
        return jsonify(output),200
    
    return 'No books found',404

@app.route('/getCurrentOwner/<int:bookid>',methods=['GET'])
@jwt_required()
def get_current_owner(bookid):
    userRole = Users.query.filter_by(emailID = get_jwt_identity()).first()
    if userRole.role == 1:
        existingBook = Books.query.filter_by(bookID=bookid).first()
        if(existingBook):
            if(existingBook.status == 0):
                return jsonify(message=f"The Book '{existingBook.bookName}' is Available.No Current Owner"),200
            elif(existingBook.status == 2 and existingBook.borrowerID):
                borrower = Users.query.filter_by(userID=existingBook.borrowerID).first()
                return jsonify(message = f"The book '{existingBook.bookName}' is requested by {borrower.userName}"),200
            elif(existingBook.status == 1 and existingBook.borrowerID):
                borrower = Users.query.filter_by(userID=existingBook.borrowerID).first()
                return jsonify(message = f"The book '{existingBook.bookName}' is Currenlty Owned by {borrower.userName}"),200
            return jsonify(error="Something error"),404
        return jsonify(message="The requested book is Invalid. No such book present in Library"),404
    return jsonify(error="You are not privileged to view this data"),403

@app.route('/requestABook',methods=['PUT'])
@jwt_required()
def request_a_Book():
    loggedInUser = Users.query.filter_by(emailID=get_jwt_identity()).first()
    if loggedInUser.role == 2:
        bookid = request.args['bookid']
        existingBook = Books.query.filter_by(bookID=bookid).first()
        if(existingBook):
            if((existingBook.borrowerID == loggedInUser.userID) and existingBook.status == 2):
                return jsonify(error=f"You already requested '{existingBook.bookName}' book. Please wait for librarian approval"),404
            if((existingBook.borrowerID == loggedInUser.userID) and existingBook.status == 1):
                return jsonify(error=f"You are the current owner for '{existingBook.bookName}' book. Librarian approved your request"),404
            if(existingBook.status == 0):
                existingBook.status = 2
                existingBook.borrowerID = loggedInUser.userID
                bookRequest = BookRequests(requestedUser=loggedInUser.userID,requestedBook=existingBook.bookID,requestStatus=2)
                availableBook = AvailableBooks.query.filter_by(bookID=existingBook.bookID).first()
                if(availableBook):
                    db.session.delete(availableBook)
                db.session.add(bookRequest)
                db.session.commit()
                return jsonify(message = f"Request for book '{existingBook.bookName}' is created."),200
            return jsonify(error=f"The requested book '{existingBook.bookName}' is already taken by some one"),404
        return jsonify(error="The book which is requested is invalid"),404
    return jsonify(error="You are not privileged to request the book only students are previleged"),403

@app.route('/getRequestedBookStatus',methods=['GET'])
@jwt_required()
def get_Requested_Book_Status():
    loggedInUser = Users.query.filter_by(emailID=get_jwt_identity()).first()
    if loggedInUser.role == 2:
        output = []
        bookRequests = db.session.query(BookRequests,Status,Books,BookCategory).join(Books,Books.bookID == BookRequests.requestedBook)\
                                                                        .join(BookCategory,BookCategory.categoryID == Books.bookCategory)\
                                                                        .join(Status,BookRequests.requestStatus == Status.statusID)\
                                                                        .filter(BookRequests.requestedUser == loggedInUser.userID).all() 
        if bookRequests:
            for bookReq,status,book,bookCat in bookRequests:
                output.append({
                    "Request ID":bookReq.requestID,
                    "Book Name":book.bookName,
                    "Book Category":bookCat.categoryName,
                    "Status": status.statusName,
                })
            return jsonify(output),200
        return jsonify(error="There are no Book requests from your side"),404
    return jsonify(error="You are not privileged to To view the Requested books only students are previleged"),403

@app.route('/showAllBookRequests',methods=['GET'])
@jwt_required()
def show_all_book_requests():
    loggedInUser = Users.query.filter_by(emailID=get_jwt_identity()).first()
    if loggedInUser.role == 1:
        output = []
        bookRequests = db.session.query(BookRequests,Status,Books,BookCategory,Users).join(Books,Books.bookID == BookRequests.requestedBook)\
                                                                        .join(BookCategory,BookCategory.categoryID == Books.bookCategory)\
                                                                        .join(Status,BookRequests.requestStatus == Status.statusID)\
                                                                        .join(Users,Users.userID == BookRequests.requestedUser)\
                                                                        .filter(BookRequests.requestStatus == 2)\
                                                                        .all() 
        if bookRequests:
            for bookReq,status,book,bookCat,users in bookRequests:
                output.append({
                    "Request ID":bookReq.requestID,
                    "Book Name":book.bookName,
                    "Book Category":bookCat.categoryName,
                    "Requested User Details": {
                        "User ID":users.userID,
                        "User Name":users.userName,
                        "User Email ID":users.emailID,
                    },
                    "Status": status.statusName,
                })
            return jsonify(output),200
        return jsonify(error="No Book Requests from any user"),404
    return jsonify(error="You are not privileged to To view the All the Requested books only Staff are previleged"),403

@app.route('/grantABook',methods=['PUT'])
@jwt_required()
def grant_A_Book():
    loggedInUser = Users.query.filter_by(emailID=get_jwt_identity()).first()
    if loggedInUser.role == 1:
        reqID = request.args['reqID']
        existingReq = BookRequests.query.filter_by(requestID = reqID).first()
        if(existingReq):
            if(existingReq.requestStatus == 2):
                existingBook = Books.query.filter_by(bookID = existingReq.requestedBook).first()
                existingBook.status = 1
                existingBook.rack = None
                existingReq.requestStatus = 1
                assignedBooks = AssignedBooks(requestID = existingReq.requestID,bookID = existingReq.requestedBook)
                db.session.add(assignedBooks)
                db.session.commit()
                return jsonify(message=f"The request with '{reqID}' is approved and book is granted for the user"),200
            elif(existingReq.requestStatus == 1):
                return jsonify(error=f"This request is already approved"),404
            elif(existingReq.requestStatus == 4):
                return jsonify(error=f"This request is already Closed"),404
            else:
                currentStatus = Status.query.filter_by(statusID = existingReq.requestStatus).first()
                return jsonify(error=f"Something error The current status for this request is '{currentStatus.statusName}'"),404
        return jsonify(error=f"Invalid request ID"),404   
    return jsonify(error="You are not privileged to grant Requested books only Staff are previleged"),403

@app.route('/rejectABook',methods=['PUT'])
@jwt_required()
def reject_A_Book():
    loggedInUser = Users.query.filter_by(emailID=get_jwt_identity()).first()
    if loggedInUser.role == 1:
        reqID = request.args['reqID']
        existingReq = BookRequests.query.filter_by(requestID = reqID).first()
        if(existingReq):
            if(existingReq.requestStatus == 2):
                existingBook = Books.query.filter_by(bookID = existingReq.requestedBook).first()
                existingBook.status = 0
                existingBook.borrowerID = None
                existingReq.requestStatus = 3
                availableBook = AvailableBooks.query.filter_by(bookID=existingBook.bookID).first()
                if(not availableBook):
                    db.session.add(AvailableBooks(bookID=existingBook.bookID))
                db.session.commit()
                return jsonify(message=f"The request with '{reqID}' is Rejected "),200
            elif(existingReq.requestStatus == 1):
                return jsonify(error=f"This request is already approved"),404
            elif(existingReq.requestStatus == 4):
                return jsonify(error=f"This request is already Closed"),404
            else:
                currentStatus = Status.query.filter_by(statusID = existingReq.requestStatus).first()
                return jsonify(error=f"Something error The current status for this request is '{currentStatus.statusName}'"),404
        return jsonify(error=f"Invalid request ID"),404   
    return jsonify(error="You are not privileged to grant Requested books only Staff are previleged"),403

@app.route('/showAllAssignedBooks',methods=['GET'])
@jwt_required()
def show_all_AssignedBooks():
    loggedInUser = Users.query.filter_by(emailID=get_jwt_identity()).first()
    if loggedInUser.role == 1:
        output = []
        bookRequests = db.session.query(AssignedBooks,Status,Books,BookCategory,Users).join(Books,Books.bookID == AssignedBooks.bookID)\
                                                                        .join(BookCategory,BookCategory.categoryID == Books.bookCategory)\
                                                                        .join(Status,Books.status == Status.statusID)\
                                                                        .join(Users,Users.userID == Books.borrowerID)\
                                                                        .all() 
        if bookRequests:
            for assignBook,status,book,bookCat,users in bookRequests:
                output.append({
                    "Request ID":assignBook.requestID,
                    "Book Name":book.bookName,
                    "Book Category":bookCat.categoryName,
                    "Current Borrower Details": {
                        "User ID":users.userID,
                        "User Name":users.userName,
                        "User Email ID":users.emailID,
                    },
                    "Status": status.statusName,
                })
            return jsonify(output),200
        return jsonify(error="No books are granted all books are available"),404
    return jsonify(error="You are not privileged to To view the All the Requested books only Staff are previleged"),403

@app.route('/returnABook',methods=['PUT'])
@jwt_required()
def return_A_Book():
    loggedInUser = Users.query.filter_by(emailID=get_jwt_identity()).first()
    if loggedInUser.role == 1:
        reqID = request.args['reqID']
        assignedBook = AssignedBooks.query.filter_by(requestID = reqID).first()
        if(assignedBook):
            existingBook = Books.query.filter_by(bookID = assignedBook.bookID).first()
            existingBook.status = 0
            existingBook.rack = 0
            existingBook.borrowerID = None
            existingReq = BookRequests.query.filter_by(requestID=reqID).first()
            if(existingReq):
                existingReq.requestStatus = 4
            availableBook = AvailableBooks.query.filter_by(bookID=existingBook.bookID).first()
            if(not availableBook):
                db.session.add(AvailableBooks(bookID=existingBook.bookID))
        
            db.session.delete(assignedBook)
            db.session.commit()
            return jsonify(message=f"The Book '{existingBook.bookName}' is returned"),200
        return jsonify(error=f"Invalid request ID"),404   
    return jsonify(error="You are not privileged to take book returns only Staff are previleged"),403