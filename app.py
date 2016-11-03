from jinja2 import StrictUndefined
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import func

from flask import Flask, jsonify, render_template, request, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension


# app is now your new Flask object
app = Flask(__name__)

# May not need this
app.secret_key = ''

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





# Render the homepage
@app.route('/')
def index():
    """Render homepage and send the user there."""

    return render_template('homepage.html')




################## Run Server ##################


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = False
    app.jinja_env.auto_reload = app.debug

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(host='0.0.0.0')
