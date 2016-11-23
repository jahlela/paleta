from jinja2 import StrictUndefined
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import func, desc

from flask import Flask, jsonify, render_template, request, redirect, session, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension

# Don't import session from db -- it may be confused with Flask session
from model import connect_to_db, db, User, Image, UserImage, Color, ImageColor

from helpers import get_color_bin
# from image_analysis import hash_photo
from color_difference import get_image_and_palette

import os.path
import requests
import bcrypt

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "mypaleta"

# Make Jinja2 raise an error if there is an undefined variable
app.jinja_env.undefined = StrictUndefined


################## Setup ##################

# Make sure logged_in is initialized in the session so that everything in the 
# menu renders properly
@app.before_request
def before_request():
    """ Default session["logged_in"] to false if next endpoint is not /login"""

    if "logged_in" not in session and request.endpoint != 'login':
        session["logged_in"] = False


################## Render Templates ##################


@app.route('/', methods=['GET'])
def index(photos=None):
    """ Render homepage """

    if "user_id" not in session:
        session["user_id"] = {}
        user = None

    elif "user_id" in session and session["user_id"] == None:
        user = None
    else:
        user_id = session["user_id"]
        # get user object from database with their user_id
        user = User.query.get(user_id)

    if photos is None:
        photos = [Image.query.get(162)]

    return render_template('homepage.html',
                            user=user,
                            photos=photos)


@app.route('/', methods=['POST'])
def analyze_photo():
    """ For any image URL, analyze it, store it in the db, and display it 
        on the homepage """

    # Grab URL from form and use it to create an image file path and palette
    #  image is a hashed file name of the original image's content
    URL = request.form['URL']
    
    try:
        file_name, colors = get_image_and_palette(URL)
    except StandardError as error:
        print error 
        flash("Whoops! Looks like we can't access that image. \
               Please try a different one.")
        return redirect('/')

    # Add image to db and save resulting image_id
    image_id = Image.add_image_to_db(file_name)
    # make db entry for each color
    Color.add_colors_to_db(colors)
    # Add image colors to db
    ImageColor.add_image_colors_to_db(image_id, colors)
    # If user is logged in, add a user_image record if none already exists
    if session["logged_in"]:
        user_id = session["user_id"]
        UserImage.add_user_image_to_db(user_id, image_id)
    # This must be a list, even though there is only one element
    new_photo = [Image.query.filter(Image.file_name==file_name).first()]

    # Technically just calls the index function in the '/' GET route
    return index(new_photo)


@app.route('/gallery', methods=["GET"])
def gallery(photos=None):
    """ Display photo gallery """

    # get user object from database with their user_id
    if session["logged_in"]:
        user_id = session["user_id"]
        user = User.query.get(user_id)
    else:
        user = None

    photos = Image.query.order_by(Image.image_id.desc()).all()

    return render_template('/gallery.html',
                            photos=photos, 
                            user=user)


@app.route('/users/<user_id>', methods=["GET"])
def user_details(user_id, photos=None):
    """ User details """

    # get user object from database with their user_id
    user_id = session["user_id"]
    user = User.query.get(user_id)

    images_by_user = UserImage.query.filter(UserImage.user_id==user_id).\
                     order_by(UserImage.user_image_id.desc()).all()

    # If the user has images associated with them, grab the images by user_image
    if images_by_user:
        photos = []
        for userimage in images_by_user:
	       photos.append(userimage.image)
        return render_template('/user_profile.html',
                               user=user,
                               photos=photos)
    # If not, just show user information
    else:
        return render_template('/user_profile.html',
                               user=user)


@app.route('/image_filter', methods=["GET"])
def image_filter():
    """ Filter images by color_bin """

    hex_color = request.args.get("hex_color") or "#6f3f79"

    # get user object from database with their user_id
    if session["logged_in"]:
        user = User.query.get(session["user_id"])
    else:
        user = None

    color_bin = get_color_bin(hex_color)
    color_image_query = ImageColor.query.filter(ImageColor.color_bin==color_bin).distinct()

    # If there are photos represented in that bin, display them
    if color_image_query:
        photo_set = set()
        for color_image in color_image_query:
           photo_set.add(color_image.image)
        photos = list(photo_set)
        return render_template('/image_filter.html',
                                user=user,
                                hex_color=hex_color,
                                photos=photos)
    # If not, just show user information
    else:
        flash("Whoops! No similar images found.")
        return redirect('/gallery')


################## Redirects ##################


@app.route("/register", methods=["POST"])
def register_new_user():
    """ Add new user and log them in """
    
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']

    # Grab any record matching this email (will be None if no previous record)
    user_in_db = User.query.filter_by(email=email).first()

    # If there is a previous record with this email, prompt user to try again
    if user_in_db:
        flash("It looks like you are already registered. Try logging in again.")

        return redirect("/")

    # if username (email) is in not in database, add them and log them in
    else:
        # Add new user to db
        new_user = User(firstname=firstname, lastname=lastname, email=email, 
                password=bcrypt.hashpw(password.encode("UTF_8"), bcrypt.gensalt()))
        db.session.add(new_user)
        db.session.commit()

        # Get new User record for logging in
        current_user = User.query.filter_by(email=email).first()

        # Add user to browser session
        session["user_id"] = current_user.user_id
        session["logged_in"] = True
        flash("Successfully registered and logged in!")

        # Redirect to homepage
        return redirect("/")


@app.route("/login", methods=['POST'])
def user_login():
    """ User login """

    email = request.form['email']
    password = request.form['password']

    if "user_id" not in session:
        session["user_id"] = {}

    current_user = User.query.filter_by(email=email).first()
    input_password_hash = bcrypt.hashpw(password.encode("UTF_8"),
                          current_user.password.encode("UTF_8")).decode()

    # check login credentials against database, and route user accordingly
    if not current_user:
        # redirect to /register
        flash("No record found. Please register!")
        return redirect("/register")

    elif current_user and current_user.password == input_password_hash:
        # store username in Flask session
        session["user_id"] = current_user.user_id
        session["logged_in"] = True
        flash("Successfully logged in!")
        return redirect("/")

    # if username in db and password belongs to same user, redirect to homepage 
    elif current_user.password != input_password_hash:
        flash("Password does not match. Please try again.")
        return redirect("/")


@app.route('/logout')
def logout():
    """ User logout """

    # remove the username from the session if it's there
    session['user_id'] = None
    session['logged_in'] = False

    flash("Successfully logged out!")
    return redirect("/")






@app.route('/favorite_image', methods=["POST"])
def add_image_to_profile():
    """ The user should already be logged in. """

    # Grab user_id from the browser session     
    user_id = session["user_id"]
    image_id = int(request.form["image_id"])
    print
    print 'favoriting picture: ', image_id
    print 'user_id', user_id
    
    userimage_in_db = UserImage.query.filter(UserImage.user_id==user_id, 
                                        UserImage.image_id==image_id).first()

    if userimage_in_db:
        flash('Image already added to profile')
    else: 
        new_user_image = UserImage(user_id=user_id, image_id=image_id)
        db.session.add(new_user_image)
        db.session.commit()
        # flash('Image added!')

    return "Favorited image"


@app.route('/remove_image', methods=["POST"])
def remove_image_from_profile():
    """ The user should already be logged in. """

    # Grab user_id from the browser session and image_id from the request    
    user_id = session["user_id"]
    image_id = int(request.form["image_id"])
    
    userimage_in_db = UserImage.query.filter(UserImage.user_id==user_id, 
                                        UserImage.image_id==image_id).first()

    if userimage_in_db:
        db.session.delete(userimage_in_db)
        db.session.commit()
        # flash('Image removed from profile')
    else: 
        flash('This image could not be found.')

    return "Removed image"


################## Run Server ##################


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0')