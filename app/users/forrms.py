from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, IntegerField


""" GameInsertEdit form is used to edit the existing games and to insert new games into the database """

class GameInsertEdit(Form):
    SECRET_KEY = "game_insert_edit"
    short_name = StringField('Short name:')
    name = StringField('Full name:')
    version = StringField('Version:')
    submit = SubmitField('Confirm')


""" UserInsertEdit form is used to edit the existing users and to insert new users into the database """

class UserInsertEdit(Form):
    SECRET_KEY = "user_insert_edit"
    username = StringField('Enter username:')
    password = PasswordField('Enter password:')
    name = StringField('Enter name:')
    role = IntegerField('Status:')
    submit = SubmitField('Confirm')


""" Search form is used to search data on the page the user is currently at """

class Search(Form):
    SECRET_KEY = 'search_form'
    search_item = StringField('Enter query:')
    submit = SubmitField('Search')


""" Confirm form is used to confirm the deletion and restoration of users and games """

class Confirm(Form):
    submit = SubmitField('Confirm')


""" SelectGame form is used to select a game to display in Scores function """

class SelectGame(Form):
    select_game = StringField()
    submit = SubmitField('Submit')