# Flask app for Flask + Firebase + Arduino

from flask import Flask, render_template, url_for, request, jsonify
from datetime import datetime
import pyrebase

app = Flask(__name__)

config = {}
key = 0 # If recording data over time, keys should be seconds or milliseconds from 0

# Notes:
# 1.    The @app.route parameter (in parantheses) should match the name of the page to
#       which it routes, without the ".html"
#       Ex. If routing to signIn.html: @app.route("/signIn") You need to add the 
#       forward slash before the parameter
#       The only exception is the @app.route for the index page: @app.route("/")
# 2.    When linking to index.html from other html pages when using Flask,
#       use {{url_for('index')}}. The name of the python function (_name) is used as
#       the endpoint, unless you specify the endpoint argument explicitly.
#       Ex. {{url_for('index')}} will redirect the user to index.html because
#       "index" is the name of the defined route function

@app.route("/")                             # Landing Page
def index():
    return render_template("index.html")


@app.route("/register")                     # Account Registration Page
def register():
    return render_template("register.html")

@app.route("/signIn")                       # Sign In Page
def signIn():
    return render_template("signIn.html")

@app.route("/home")                         # Account Home Page
def home():
    return render_template("home.html")

@app.route("/test", methods=['GET', 'POST'])
def test():

    global config, userID, db, timeStamp, key

    # POST request (FB configuration sent from login.js, request.method)
    if request.method == 'POST':

        # Each data set will be stored under its own child node identified the timestamp
        # Get time stamp to be used as firebase node
        timeStamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        # Receive Firebase configuration credentials, pop uid and assign to userID
        config = request.get_json()         # parse as JSON
        userID = config.pop('userID')       # userID used for updating data in FRD

        # Output to a console (or file) is normally buffered (stored) until it is
        # forced out by the printing of a newline. Flush will force the information
        # in the buffer to be printed immediately.

        print('User ID: ' + userID, flush = True)   # Debug only
        print(config, flush = True)                 # Debug only
    
        # Initialize firebase connection
        firebase = pyrebase.initialize_app(config)

        # Create database object ("db" represents the root node in the database)
        db = firebase.database()

        # Write sample data to FB to to test connection
        db.child('users/' + userID + '/data/' + '/' + timeStamp).update({'testKey':'testValue'})

        return 'Success', 200

    # If a GET request is made, check to see if the FB configuration has been provided. If not,
    # do nothing. If so, update the firesbase with the sensor data.
    #else:
        #if(bool(config) is false):      # If config is empty, bool(config) returns false
        #    print('FB config is empty')
    
        # Code to get data from Arduino will go here

    #    return "Success"

# Run server on local IP address on port 5000
if __name__ == "__main__":
    app.run(debug=False, host='10.133.132.212', port=5000)