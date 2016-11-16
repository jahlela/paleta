""" Models and database functions for paleta db. """

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


###################### Database Tables ####################


class User(db.Model):
    """ User details """

    __tablename__ = "users"
    
    user_id = db.Column(db.Integer, primary_key=True, nullable = False,
                                    autoincrement = True)
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

# =%=%=%=%=%=%=%= Old Format =%=%=%=%=%=%=%=%=%=
    # colors has a format of: "#aa7c60,#e9cf7a,#c0411a,#fdf1e4,#ede3b3"
    # table will accommodate up to 10 colors in this format, but default is 5
    colors = db.Column(db.String(100), nullable = False)
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=


# =%=%=%=%=%=%=%= New Format %=%=%=%=%=%=%=%=%=

#     # There is a relationship defined between Image and UserImage in UserImage.
#     # Backref is "userimages"

#     # There is a relationship defined between Image and ImageColor in ImageColor.
#     # Backref is "imagecolors"

# class ColorBin(db.Model):
#     """ Bins of colors """

#     color_bin_id = db.Column(db.Integer, primary_key=True, autoincrement = True,
#                                                         nullable = False)
#     color_bin_name = db.Column(db.String(50))
#     min_red = db.Column(db.Integer, nullable = False)
#     max_red = db.Column(db.Integer, nullable = False)
#     min_green = db.Column(db.Integer, nullable = False)    
#     max_green = db.Column(db.Integer, nullable = False)
#     min_blue = db.Column(db.Integer, nullable = False)
#     max_blue = db.Column(db.Integer, nullable = False)

#     # There is a relationship defined between ColorBin and Color in Color.
#     # Backref is "colors"


# class Color(db.Model):
#     """ Color details """

#     __tablename__ = "imagecolors"
    
#     color_id = db.Column(db.Integer, primary_key=True, autoincrement = True,
#                                                     nullable = False)
#     color_bin_id = db.Column(db.Integer, db.ForeignKey('color_bins.color_bin_id'),
#                                                     nullable = False)
#     red = db.Column(db.Integer)
#     green = db.Column(db.Integer)
#     blue = db.Column(db.Integer)

#     # Define relationship to colorbins
#     colorbins = db.relationship("ColorBin", backref=db.backref("colors"), order_by=color_id)

#     # There is a relationship defined between Color and ImageColor in ImageColor.
#     # Backref is "imagecolors"
    

# class ImageColor(db.Model):
#     """ Colors in a photo """

#     __tablename__ = "imagecolors"

#     image_color_id = db.Column(db.Integer, primary_key=True, autoincrement = True,
#                                                     nullable = False)
#     image_id = db.Column(db.Integer, db.ForeignKey('images.image_id'), index=True, 
#                                                     nullable = False)
#     color_id = db.Column(db.Integer, db.ForeignKey('colors.color_id'), index=True, 
#                                                     nullable = False)

#     # Define relationship to image
#     image = db.relationship("Image", backref=db.backref("imagecolors"), order_by=image_color_id)

#     # Define relationship to color
#     color = db.relationship("Color", backref=db.backref("imagecolors"), order_by=image_color_id)
    
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=

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

    db.create_all()