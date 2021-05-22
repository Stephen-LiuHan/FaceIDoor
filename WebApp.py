import os

from flask import Flask, render_template

#from FaceIDoor import *

app = Flask(__name__)

#WORKING_DIR = os.path.dirname(__file__)
#print(__file__)
#TEMPLATE = os.path.join(WORKING_DIR, "templates")



@app.route('/')
def auth():
    return render_template("Auth.html")

@app.route('/Auth')
def auth_myself():
    #open()
    pass

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)
