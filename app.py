import requests

from jinja2 import StrictUndefined
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import func

from flask import Flask, jsonify, render_template, request, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from image_manipulation import get_palette


# app is now your new Flask object
app = Flask(__name__)

# Need this for debugging
app.secret_key = 'cantbeblank'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = StrictUndefined

# @app.before_request
# def before_request():
#     """ Default session["logged_in"] to false if next endpoint is not /login"""

#     if "logged_in" not in session and request.endpoint != 'login':
#         session["logged_in"] = False



################## Render Templates ##################




@app.route('/')
def index():
    """ Render homepage and send the user there. """

    return render_template('homepage.html')


@app.route('/analyze_photo')
def analyze_photo(URL, color_limit):
    """  """

    # Grab the image from a URL
    image_request = requests.get(URL)

    # Create a hexidecimal hash of the image data string for a unique filename
    file_hash = hex(hash(image_request.content))

    # Sometimes there is a dash at the beginning -- not great for a file name
    # Replace the '-' with a 1 to maintain uniqueness
    if file_hash[0] == '-':
        file_hash_name = '1' + hex(hash(r.content))[2:] + '.png'
    # Create a filename as is
    else:
        file_hash_name = hex(hash(r.content))[1:] + '.png'

    with open(file_hash_name,'w') as new_image_file:
        new_image_file.write(image_request.content)




################## Run Server ##################


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # In debug mode, prevents caching 
    app.jinja_env.auto_reload = app.debug

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0')
