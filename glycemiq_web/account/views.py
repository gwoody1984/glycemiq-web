from flask import render_template

from . import account
from .register_form import RegisterForm

@account.route('/')
def index():
    return render_template('index.html')


@account.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return render_template('index.html')
    return render_template('register.html', form=form)


@account.route('/login')
def login():
    return render_template('login.html')