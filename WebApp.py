import os

from flask import Flask, render_template

from FaceIDoor import *

app = Flask(__name__)

TEMPLATE = os.path.join(WORKING_DIR, "Template/")

@app.route('/')
def auth():
    return render_template(os.path.join(TEMPLATE, "auth.html"))

@app.@app.route('/Auth')
def auth():
    open()

if __name__ == '__main__':
    app.run()