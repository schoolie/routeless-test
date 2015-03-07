from flask import render_template, Blueprint
from routeless import db, apimanager

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/index')
def index():
    
    return render_template('index.html',
                           data='data')
