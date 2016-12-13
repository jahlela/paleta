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

    @classmethod
    def add_user_to_db(cls, firstname, lastname, email, password):
        
        new_user = User(firstname=firstname, lastname=lastname, email=email, 
                password=bcrypt.hashpw(password.encode("UTF_8"), bcrypt.gensalt()))
        db.session.add(new_user)
        db.session.commit()

        return "Added new user"

class Role(db.Model):
    """ Role details """

    __tablename__ = "roles"
    
    role_id = db.Column(db.Integer, primary_key=True, autoincrement = True,
                                        nullable = False)
    role = db.Column(db.String(30), nullable = False)


class Image(db.Model):
    """ Image details """

    __tablename__ = "images"
    
    image_id = db.Column(db.Integer, primary_key=True, autoincrement = True,
                                                       nullable = False)
    file_name = db.Column(db.String(300), nullable = False)


    users = db.relationship("User", backref="images", 
                                    secondary="userimages") #Access Image directly

    # There is a relationship defined between Image and ImageColor in ImageColor.
    # Backref to ImageColor is "imagecolors"

    @classmethod
    def add_image_to_db(cls, file_name):
        # Check if the image is already in the db 
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

    @classmethod
    def remove_image_from_db(cls, image_id):

        # Query the database for record of this photo
        image_in_db = Image.query.get(image_id)

        # If prior record, delete it
        if image_in_db:
            db.session.delete(image_in_db)
            db.session.commit()


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



class UserRole(db.Model):
    """ All records of a user's roles """

    __tablename__ = "userroles"
    
    user_role_id = db.Column(db.Integer, primary_key=True, autoincrement = True,
                                                    nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), 
                                                    nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), 
                                                    nullable=False)

    # Define relationship to user
    user = db.relationship("User", backref=db.backref("userroles", order_by=user_role_id))

    # Define relationship to role
    role = db.relationship("Role", backref=db.backref("userroles", order_by=user_role_id))


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


    @classmethod
    def add_user_image_to_db(cls, user_id, image_id):

        # Query the database for a previous record of this photo and user
        user_image_in_db = UserImage.query.filter(UserImage.user_id==user_id, 
                                                 UserImage.image_id==image_id).first()

        # If no prior record, create one
        if not user_image_in_db:
            new_user_image = UserImage(user_id=user_id, image_id=image_id)
            db.session.add(new_user_image)
            db.session.commit()

    @classmethod
    def remove_user_image_from_db(cls, user_id, image_id):

        # Query the database for record of this photo associated with any user
        user_image_in_db = UserImage.query.filter(UserImage.user_id==user_id, 
                                                 UserImage.image_id==image_id).all()

        # If prior records, delete them
        if user_image_in_db:
            for user_image in user_image_in_db:
                db.session.delete(user_image)
                db.session.commit()
        


class GalleryImage(db.Model):
    """ All records of images in the gallery """

    __tablename__ = "galleryimages"
    
    gallery_image_id = db.Column(db.Integer, primary_key=True, autoincrement = True,
                                                    nullable = False)
    image_id = db.Column(db.Integer, db.ForeignKey('images.image_id'), 
                                                    nullable=False)

    # Define relationship to image
    image = db.relationship("Image", backref=db.backref("galleryimages", 
                                     order_by=gallery_image_id))

    @classmethod
    def add_gallery_image_to_db(cls, image_id):

        # Query the database for a previous record of this photo in the gallery
        gallery_image_in_db = GalleryImage.query.filter(GalleryImage.image_id==image_id).first()

        # If no prior record, create one
        if not gallery_image_in_db:
            new_gallery_image = GalleryImage(image_id=image_id)
            db.session.add(new_gallery_image)
            db.session.commit()

    @classmethod
    def remove_gallery_image_from_db(cls, image_id):

        # Query the database for record of this photo in the gallery
        gallery_image_in_db = GalleryImage.query.filter(GalleryImage.image_id==image_id).first()

        # If prior record, delete it
        if gallery_image_in_db:
            db.session.delete(gallery_image_in_db)
            db.session.commit()


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

        return "Added image colors to db"

    @classmethod
    def remove_image_colors_from_db(cls, image_id):

        imagecolor_in_db = ImageColor.query.filter(ImageColor.image_id==image_id).all()

        if imagecolor_in_db:
            for imagecolor in imagecolor_in_db:
                db.session.delete(imagecolor)
                db.session.commit()

        return "Removed image colors from db"




################### Helper Functions ####################

def add_gallery_images():

    photos = Image.query.order_by(Image.image_id).all()

    for photo in photos:
        GalleryImage.add_gallery_image_to_db(photo.image_id)
        print "added ", photo.image_id





def connect_to_db(app, URI='postgresql:///paleta'):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = URI
    db.app = app
    db.init_app(app)

    # Change default URI, db.uri


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
    # add_gallery_images()

    db.create_all()


