from flask import render_template, redirect, flash
from . import main
from .forrms import LoginForm
from ..models import Users
from flask_login import login_user


""" Starting page where user login is required, with basic login data inspection.
    After login, all users are redirected to 'games' page.
"""

@main.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data and form.password.data:
            registered_user = Users.login(form.username.data)
            if registered_user and registered_user.is_deleted == True:
                flash('You are no longer our user')
                return redirect('/')
            if registered_user is not None and registered_user.verify_password(form.password.data):
                login_user(registered_user)
                return redirect('/allusers/games')
            else:
                flash('You must enter the correct username and password')
        else:
            flash('You must enter the correct username and password')
    return render_template("views/index.html", form=form)