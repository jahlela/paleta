

"""Models and database functions for paleta db."""

from flask_sqlalchemy import SQLAlchemy

# Here's where we create the idea of our database. We're getting this through
# the Flask-SQLAlchemy library. On db, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################


class User(db.User):
    """User details."""

    __tablename__ = "users"
    
    user_id = db.Column(db.Integer, primary_key=True, nullable = False,
                               autoincrement = True)
    first_name = db.Column(db.String(30), nullable = False))
    last_name = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(50), nullable = False, unique=True)
    password = sa.Column(PasswordType(schemes=['pbkdf2_sha512','md5_crypt'],
                                      deprecated=['md5_crypt']))

class Image(db.Image):
    """Image details."""

    __tablename__ = "images"
    
    image_id = db.Column(db.Integer, primary_key=True, nullable = False,
                               autoincrement = True)


    
class UserImage(db.UserImage):
    """Details about a user's favorite images."""

    __tablename__ = "userImages"
    
    user_image_id = db.Column(db.Integer, primary_key=True, nullable = False,
                               autoincrement = True)




##############################################################################
# Helper functions

def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///paleta'
    app.config['SQLALCHEMY_ECHO'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."
