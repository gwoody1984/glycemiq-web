import bcrypt

from flask import render_template, url_for, abort, redirect, flash, request
from flask_login import login_user, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer

from . import account
from .register_form import RegisterForm
from .login_form import LoginForm
from ..emailer import send_mail
from ..config import config_as_dict
from glycemiq_db import db, User
from glycemiq_web import login_manager

config = config_as_dict('APP')
ts = URLSafeTimedSerializer(config['URL_SERIALIZER_KEY'])


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@account.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('portal.home'))

    form = RegisterForm()
    if form.validate_on_submit():

        # check for user existence
        if User.query.filter_by(email=form.email.data).scalar() is None:
            # new user save record
            salt = bcrypt.gensalt()
            user = User(
                email=form.email.data,
                password=salt + bcrypt.hashpw(form.password.data.encode('utf-8'), salt=salt)
            )
            db.session.add(user)
            db.session.commit()

            # send confirm email
            token = ts.dumps(user.email, salt=config['URL_SERIALIZER_SALT'])

            confirm_url = url_for(
                'account.confirm_email',
                token=token,
                _external=True)

            html = render_template(
                'email/activate.html',
                confirm_url=confirm_url)

            send_mail(user.email, "Confirm your email", html)

        else:
            # user exists
            # send user exists email
            html = render_template('email/reregistration.html')
            send_mail(form.email.data, "Your account already exists", html)

        return render_template('registration_success.html')
    return render_template('register.html', form=form)


@account.route('/', methods=['GET', 'POST'])
@account.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('portal.home'))

    form = LoginForm()
    if form.validate_on_submit():

        # make sure the user exists
        user = User.query.filter_by(email=form.email.data).first()
        if user:

            # check the password hash
            salt = user.password[:29]
            actual_password = user.password[29:]
            password_hash = bcrypt.hashpw(form.password.data.encode('utf-8'), salt=salt)

            if actual_password == password_hash:
                login_user(user)
                return redirect(request.args.get('next') or url_for('portal.home'))
            else:
                flash('Email or password are incorrect.', 'danger')
        else:
            flash('Email or password are incorrect.', 'danger')

    return render_template('login.html', form=form)


@account.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('account.login'))


@account.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt=config['URL_SERIALIZER_SALT'], max_age=86400)
    except:
        return abort(404)

    user = User.query.filter_by(email=email).first_or_404()

    user.verified = True

    db.session.add(user)
    db.session.commit()

    flash('Your email has been confirmed.', 'success')
    return redirect(url_for('account.login'))
