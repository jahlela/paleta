

""" Models and database functions for paleta db. """

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


##############################################################################


class User(db.Model):
    """ User details """

    __tablename__ = "users"
    
    user_id = db.Column(db.Integer, primary_key=True, nullable = False,
                                    autoincrement = True)
    firstname = db.Column(db.String(30), nullable = False)
    lastname = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(50), nullable = False, unique=True)
    password = db.Column(db.String(50), nullable = False)

    # There is a relationship defined between User and UserImage in UserImage.
    # Backref to UserImage is "userimages"


class Image(db.Model):
    """ Image details """

    __tablename__ = "images"
    
    image_id = db.Column(db.Integer, primary_key=True, nullable = False,
                                     autoincrement = True)
    file_name = db.Column(db.String(30), nullable = False)
    # colors has a format of: "#aa7c60 | #e9cf7a | #c0411a | #fdf1e4 | #ede3b3"
    # table will accommodate up to 10 colors in this format
    colors = db.Column(db.String(100), nullable = False)


    # There is a relationship defined between Image and UserImage in UserImage.
    # Backref to UserImage is "userimages"

    
class UserImage(db.Model):
    """ All records of a user favoriting an image """

    __tablename__ = "userimages"
    
    user_image_id = db.Column(db.Integer, primary_key=True, nullable = False,
                                          autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    fav_image = db.Column(db.Integer, db.ForeignKey('images.image_id'), nullable=False)


    # Define relationship to user
    user = db.relationship("User", backref=db.backref("userimages", order_by=user_image_id))

    # Define relationship to image
    image = db.relationship("Image", backref=db.backref("userimages", order_by=user_image_id))



##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///paleta'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from app import app
    connect_to_db(app)
    print "Connected to DB."

    db.create_all()