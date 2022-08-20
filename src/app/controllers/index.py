from flask import Blueprint, render_template


home = Blueprint('home', __name__, url_prefix="/")

@home.route('/', methods = ["GET"])
def index():
    return render_template('index.html')

