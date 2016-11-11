
from jinja2 import StrictUndefined
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import func

from flask import Flask, jsonify, render_template, request, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

# Don't import session from db -- it may be confused with Flask session
from model import connect_to_db, db, User, Image, UserImage

from image_analysis import hash_photo

import os.path
import requests
import bcrypt

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Make Jinja2 raise an error if there is an undefined variable
app.jinja_env.undefined = StrictUndefined


################## Setup ##################


@app.before_request
def before_request():
    """ Default session["logged_in"] to false if next endpoint is not /login"""

    if "logged_in" not in session and request.endpoint != 'login':
        session["logged_in"] = False


################## Render Templates ##################


@app.route('/', methods=['GET'])
def index(file_name=None, colors=None):
    """ Render homepage """

    # Default to caterpillar image
    if file_name == None:
        file_name='/static/img/demo/caterpillar.png'

    # Default to caterpillar colors
    if colors == None:
        colors=['#aa7c60', '#e9cf7a', '#c0411a', '#fdf1e4', '#ede3b3']

    if "user_id" not in session:
        session["user_id"] = {}
        user = None

    elif "user_id" in session and session["user_id"] == None:
        user = None
    else:
        user_id = session["user_id"]
        # get user object from database with their user_id
        user = User.query.get(user_id)



    return render_template('homepage.html',
                            user=user, 
                            palette=colors,
                            image=file_name)




@app.route('/', methods=['POST'])
def analyze_photo():
    """  """

    # Grab URL from form and use it to create an image file path and palette
    #  image is a hashed file name of the original image's content
    URL = request.form['URL']
    file_name, colors = hash_photo(URL)
    print 'file_name', file_name
    print 'colors', colors



    # Next, check if the image is already in the db 
    image_in_db = Image.query.filter(Image.file_name==file_name).first()
    print 'image_in_db', image_in_db

    if image_in_db:
        print 'if image_in_db'
        # colors = image_in_db.colors
        print 'colors', colors
        image_id = image_in_db.image_id
        print 'image_id', image_id

    # If not, add the image to the db
    else:
        print "I got to the image_in_db else"
        new_photo = Image(file_name=file_name, colors=colors)
        db.session.add(new_photo)
        db.session.commit()

        image_id = new_photo.image_id

    

    # Grab user_id if a user is logged in
    if session["logged_in"]:
        user_id = session["user_id"]
        

    
        userimage_in_db = UserImage.query.filter(UserImage.user_id==user_id, 
                                            UserImage.image_id==image_id).first()

        if not userimage_in_db:
            print 'not userimage_in_db'
            print 'user_id', user_id
            print 'image_id', image_id
            new_user_image = UserImage(user_id=user_id, image_id=image_id)
            db.session.add(new_user_image)
            db.session.commit()


    print 'colors', colors

    return index(file_name, colors)


@app.route('/register')
def register():
    """ Render registration page """ 

    return render_template("/register.html")


@app.route('/users/<user_id>', methods=["GET"])
def user_details(user_id, photos=None):
    """User details."""

    # get user object from database with their user_id
    user = User.query.get(user_id)

    photo_query = UserImage.query.filter(user_id==user_id)
    print 'photo_query', photo_query

    # Default to caterpillar with colors
    if photos == None:
        photos = ['/static/img/demo/caterpillar.png', 
                    ['#aa7c60', '#e9cf7a', '#c0411a', '#fdf1e4', '#ede3b3']]

    return render_template('/user_profile.html',
                            user=user,
                            photos=photos)



################## Redirects ##################


@app.route("/register", methods=["POST"])
def register_new_user():
    """Add new users."""
    
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']

    print 'email', email

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
    """User login"""

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
    """User logout."""
    # remove the username from the session if it's there
    session['user_id'] = None
    session['logged_in'] = False

    flash("Successfully logged out!")
    return redirect("/")



################## Helper Function ##################

def clean_image_records():

    images_in_db = Image.query.all()
    print 'images_in_db', images_in_db


    for image in images_in_db:
        if image.colors[0] == "{":
            print image.colors
            image.colors = image.colors[1:-1]
        elif image.colors[0] == "\"":
            print image.colors
            image.colors = image.colors[1:-1]

    db.session.commit()




################## Run Server ##################


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    clean_image_records()

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0')
