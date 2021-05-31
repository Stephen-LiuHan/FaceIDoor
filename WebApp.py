import os

from flask import Flask, render_template
from flask_httpauth import HTTPDigestAuth

#from FaceIDoor import *

app = Flask(__name__)

#WORKING_DIR = os.path.dirname(__file__)
#print(__file__)
#TEMPLATE = os.path.join(WORKING_DIR, "templates")



users = {
    "User" : "FaceIDoor",
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/')
@auth.login_required
def auth():
    return render_template("Top.html")

@app.route('/Auth')
def auth_myself():
    #open_the_door()
    return render_template("Authorized.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)
