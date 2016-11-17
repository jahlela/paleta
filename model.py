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

    # # colors has a format of: "#aa7c60,#e9cf7a,#c0411a,#fdf1e4,#ede3b3"
    # # table will accommodate up to 10 colors in this format, but default is 5
    # colors = db.Column(db.String(100), nullable = False)

    # There is a relationship defined between Image and ImageColorBin in ImageColorBin.
    # Backref to ImageColorBin is "imagecolorbins"

    

    def add_color_bins_to_db(self):
        """ Takes an image_id, calculates and adds its color bins to the db """

        bins = self.get_image_color_bins()

        for color_bin in bins:
            # bin_for_image = ImageColorBin.query.filter(image_id==self.image_id, 
                                                        # color_bin==color_bin)

            if not bin_for_image:
                new_image_color_bin = ImageColorBin(image_id=image_id, color_bin=color_bin)
                db.session.add(new_image_color_bin)
                db.session.commit()

        return

    # Add db image object as parameter
    def get_image_color_bins(self):
        """ takes an image_id, and loops through its colors, creating 
            a set of the base-4 codes for each bin represented by that image,
            then commits a record for each bin associated with the image to the db """
        
        # Grab colors from image 
        color_string = self.colors
        colors = color_string.split(",")

        # Will hold a list of bins to associate with this image
        bins = []

        # Calculate the bin for each 
        for color in colors:
            hex_color = color[1:]
            rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2 ,4))

            bin = ''
            # Grab values for red, green, blue channels and round down to the 
            # nearest 64 and divide by 64 to find bin 
            for channel in rgb_color:
                bin_partial = (channel - (channel % 64))/64
                bin += str(bin_partial)

            bins.append(bin)

        return bins



class Color(db.Model):
    """ Color details """

    __tablename__ = "colors"
    
    color_id = db.Column(db.Integer, primary_key=True, autoincrement = True,
                                                    nullable = False)
    color = db.Column(db.String(30), nullable = False)

    # There is a relationship defined between Color and ImageColor in ImageColor.
    # Backref is "imagecolors"
    

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


