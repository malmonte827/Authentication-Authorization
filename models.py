from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
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
    
    @classmethod
    def register(cls, username, password):
        """ Register user with hashed password & return user """

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into unicode utf8 string
        hashed_utf8 = hashed.decode('utf8')

        #retrun instance of user
        return cls(username=username, password=hashed_utf8)