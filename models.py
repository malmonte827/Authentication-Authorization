from sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Models):
    """ Site User """

    __tablename__ = 'users'

    # id = db.Column(db.Integer,
    #                primary_key=True,
    #                autoincrement=True)
    
    username = db.Column(db.String(20),
                         primary_key=True)
    
    password = db.Column(db.Text,
                         nullable=False)
    
    email = db.Column(db.String(50),
                      nullable=False,
                      unique=True)
    
    first_name = db.Column(db.String(30),
                           nullable=False)
    
    last_name =db.Column(db.String(30),
                         nullable=False)