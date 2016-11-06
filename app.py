
from jinja2 import StrictUndefined
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import func

from flask import Flask, jsonify, render_template, request, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

# Don't import session from db -- it may be confused with Flask session
from model import connect_to_db, db, User, Image, UserImage

import os.path
import requests

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


@app.route('/')
def index():
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

    return render_template('homepage.html',
                            user=user)

@app.route('/register')
def register():
    """ Render registration page """ 

    return render_template("/register.html")


@app.route('/users/<user_id>', methods=["GET"])
def user_details(user_id):
    """User details."""

    # get user object from database with their user_id
    user = User.query.get(user_id)

    return render_template('/user_profile.html',
                            user=user)



################## Redirects ##################


@app.route("/register", methods=["POST"])
def register_new_user():
    """Add new users."""
    
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']

    print 'email', email

    # user_in_db = db.session.query(User).filter(User.email==email).all()
    user_in_db = False
    # if username (email) is in not in database, add them 
    if not user_in_db:
        # add to db
        new_user = User(firstname=firstname, lastname=lastname, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

    # redirect to homepage
    return redirect("/")



@app.route("/login", methods=['POST'])
def user_login():
    """User login"""

    email = request.form['email']
    password = request.form['password']

    if "user_id" not in session:
        session["user_id"] = {}

    current_user = User.query.filter_by(email=email).first()

    # check login credentials against database, and route user accordingly
    if not current_user:
        # redirect to /register
        flash("No record found. Please register!")
        return redirect("/register")

    elif current_user and current_user.password == password:
        # store username in Flask session
        session["user_id"] = current_user.user_id
        session["logged_in"] = True
        flash("Successfully logged in!")
        return redirect("/")

    # if username in db and password belongs to same user, redirect to homepage 
    elif current_user.password != password:
        flash("Password does not match. Please try again.")
        return redirect("/")


@app.route('/logout', methods=['POST'])
def logout():
    """User logout."""
    # remove the username from the session if it's there
    session['user_id'] = None
    session['logged_in'] = False

    flash("Successfully logged out!")
    return redirect("/")


@app.route('/analyze_photo', methods=['POST'])
def analyze_photo():
    """  """
    # Grab URL from form
    URL = request.form['URL']

    # Grab the image from a URL
    image_response = requests.get(URL)

    os_path = os.path.dirname(os.path.abspath(__file__))
    

    # Create a hexidecimal hash of the image data string for a unique filename
    file_hash = hex(hash(image_response.content))
    print 'file_hash', file_hash

    # Sometimes there is a dash at the beginning -- not great for a file name
    # Replace the '-' with a 1 to maintain uniqueness
    if file_hash[0] == '-':
        file_hash_name = os_path +'/static/img/photos/1' +  hex(hash(image_response.content))[2:] + '.png'
        print 'os_path', os_path
        print 'file_hash_name', file_hash_name
        
    # Create a filename as is
    else:
        file_hash_name = os_path + '/static/img/photos/' + hex(hash(image_response.content))[1:] + '.png'
        print 'os_path', os_path
        print 'file_hash_name', file_hash_name
        print 'file_hash_name', file_hash_name



    with open(file_hash_name,'wb') as new_image_file:
        new_image_file.write(image_response.content)

    message = "Successfully submitted this URL: " + URL

    flash(message)
    return redirect("/")


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
