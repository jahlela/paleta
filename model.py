""" Models and database functions for paleta db. """

from flask_sqlalchemy import SQLAlchemy
from helpers import get_color_bin

db = SQLAlchemy()


###################### Database Tables ####################


class User(db.Model):
    """ User details """

    __tablename__ = "users"
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement = True,
                                        nullable = False)
    firstname = db.Column(db.String(30), nullable = False)
    lastname = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(50), nullable = False, unique=True)
    password = db.Column(db.String(500), nullable = False)

    # There is a relationship defined between User and UserImage in UserImage.
    # Backref to UserImage is "userimages"


class UserImage(db.Model):
    """ All records of a user favoriting an image """

    __tablename__ = "userimages"
    
    user_image_id = db.Column(db.Integer, primary_key=True, autoincrement = True,
                                                    nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), 
                                                    nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('images.image_id'), 
                                                    nullable=False)

    # Define relationship to user
    user = db.relationship("User", backref=db.backref("userimages", order_by=user_image_id))

    # Define relationship to image
    image = db.relationship("Image", backref=db.backref("userimages", order_by=user_image_id))


class Image(db.Model):
    """ Image details """

    __tablename__ = "images"
    
    image_id = db.Column(db.Integer, primary_key=True, autoincrement = True,
                                                       nullable = False)
    file_name = db.Column(db.String(300), nullable = False)

    # There is a relationship defined between Image and ImageColor in ImageColor.
    # Backref to ImageColor is "imagecolors"

    @classmethod
    def add_image_to_db(cls, file_name):
        # Next, check if the image is already in the db 
        image_in_db = cls.query.filter(cls.file_name==file_name).first()

        if image_in_db:
            # colors = image_in_db.colors
            image_id = image_in_db.image_id
        # If not, add the image to the db
        else:
            new_photo = cls(file_name=file_name)
            db.session.add(new_photo)
            db.session.commit()

            image_id = new_photo.image_id

        return image_id



class Color(db.Model):
    """ Color details """

    __tablename__ = "colors"
    
    color_id = db.Column(db.Integer, primary_key=True, autoincrement = True,
                                                    nullable = False)
    color = db.Column(db.String(30), nullable = False)

    # There is a relationship defined between Color and ImageColor in ImageColor.
    # Backref is "imagecolors"

    @classmethod
    def add_colors_to_db(cls, colors):
        """ Takes a list of comma-separated hex values, and makes a record in 
            Color if none existed previously """

        for color in colors:
            color_in_db = cls.query.filter(cls.color==color).first()
            # Color not already in the table
            if not color_in_db:
                new_color = cls(color=color)
                db.session.add(new_color)
                db.session.commit()
        return



    
    

class ImageColor(db.Model):
    """ Colors in a photo """

    __tablename__ = "imagecolors"

    image_color_id = db.Column(db.Integer, primary_key=True, autoincrement = True,
                                                    nullable = False)
    image_id = db.Column(db.Integer, db.ForeignKey('images.image_id'), index=True, 
                                                    nullable = False)
    color_id = db.Column(db.Integer, db.ForeignKey('colors.color_id'), 
                                                    nullable = False)
    color_bin = db.Column(db.String(10), index=True, nullable = False)

    # Define relationship to image
    image = db.relationship("Image", backref=db.backref("imagecolors"), order_by=image_color_id)

    # Define relationship to color
    color = db.relationship("Color", backref=db.backref("imagecolors"), order_by=image_color_id)
    

    @classmethod
    def add_image_colors_to_db(cls, image_id, colors):

        for color in colors:

            color_record = Color.query.filter(Color.color==color).first()
            color_id = color_record.color_id

            has_image_color = cls.query.filter(cls.image_id==image_id, 
                                               cls.color_id==color_id).first()

            if not has_image_color:

                color_bin = get_color_bin(color)

                new_image_color = cls(image_id=image_id, 
                                             color_id=color_id,
                                             color_bin=color_bin)
                print 'new_image_color', new_image_color
                db.session.add(new_image_color)
                db.session.commit()


        return


################### Helper Functions ####################


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

    # add_color_bins_to_db(75)


    db.create_all()


