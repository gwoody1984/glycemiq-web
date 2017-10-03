from flask import render_template

from . import account

@account.route('/')
def index():
    return render_template('index.html')


@account.route('/register')
def register():
    return render_template('register.html')


@account.route('/login')
def login():
    return render_template('login.html')