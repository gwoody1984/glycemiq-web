from flask import render_template

from . import portal


@portal.route('/home')
def home():
    return render_template('home.html')