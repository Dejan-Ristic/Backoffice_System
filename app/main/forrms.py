from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, SelectField


""" LoginForm class is used for login form at the start of application """

class LoginForm(Form):
    SECRET_KEY = 'login_form'
    username = StringField('Username:')
    password = PasswordField('Password:')
    submit = SubmitField('Log in')