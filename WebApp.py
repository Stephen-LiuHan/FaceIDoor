import os

from flask import Flask, render_template
from flask_httpauth import HTTPDigestAuth

from FaceIDoor import *

app = Flask(__name__)

TEMPLATE = os.path.join(WORKING_DIR, "Template/")

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
    return render_template(os.path.join(TEMPLATE, "auth.html"))

@auth.login_required
@app.route('/Auth')
def auth():
    open()

if __name__ == '__main__':
    app.run()