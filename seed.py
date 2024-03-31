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


    db.session.commit()
    print("DB seeded")