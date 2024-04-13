from app import app
from models import *
from werkzeug.security import generate_password_hash


@app.cli.command('dbcreate')
def dbCreate():
    db.create_all()
    db.session.commit()
    print("DB created")

@app.cli.command('dbdrop')
def dbDrop():
    db.drop_all()
    db.session.commit()
    print("Db dropped")

@app.cli.command('dbseed')
def dbSeed():
    #write the seeding code here which loads the data to the data base tables
    roles_date = [
        {'roleId':1,'roleName':'Library Staff'},
        {'roleId':2,'roleName':'Student'}
    ]
    book_location_data = [
        {'rackID':0,'floorName':'ground Floor'},
        {'rackID':1,'floorName':'ground Floor'},
        {'rackID':2,'floorName':'First Floor'}
    ]

    book_category_data = [
        {'categoryID':1,'categoryName':'Programming','rackID':1},
        {'categoryID':2,'categoryName':'Self Help'},
        {'categoryID':3,'categoryName':'Project Management','rackID':1}
    ]

    books_data = [
        {'bookID':1,'bookName':'grooking Algorithms','bookCategory':1},
        {'bookID':2,'bookName':'Let us C','bookCategory':1},
        {'bookID':3,'bookName':'The magic of thinking big','bookCategory':2},
        {'bookID':4,'bookName':'Atomic Habits','bookCategory':2},
        {'bookID':5,'bookName':'GIT - The complete boot camp','bookCategory':3},
        {'bookID':6,'bookName':'AGILE - Project Management','bookCategory':3}
    ]

    user_data = [
        {'userID':1,'userName':'student1','emailID':'student1@clg.com','password':generate_password_hash('1234',method='pbkdf2:SHA256',salt_length=3),'role':2},
        {'userID':2,'userName':'student2','emailID':'student2@clg.com','password':generate_password_hash('1234',method='pbkdf2:SHA256',salt_length=3),'role':2},
        {'userID':3,'userName':'staff1','emailID':'staff1@clg.com','password':generate_password_hash('1234',method='pbkdf2:SHA256',salt_length=3),'role':1},
        {'userID':4,'userName':'staff2','emailID':'staff2@clg.com','password':generate_password_hash('1234',method='pbkdf2:SHA256',salt_length=3),'role':1}
    ]

    db.session.bulk_insert_mappings(Roles,roles_date)
    db.session.bulk_insert_mappings(BookLocation,book_location_data)
    db.session.bulk_insert_mappings(BookCategory,book_category_data)
    db.session.bulk_insert_mappings(Books,books_data)
    db.session.bulk_insert_mappings(Users,user_data)


    db.session.commit()
    print("DB seeded")