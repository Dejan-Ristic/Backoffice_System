from flask_wtf import Form
from wtforms import StringField, FloatField, SubmitField, SelectField, DateTimeField


""" classes Score and Player are used only for API testing purposes.
    Two forms in 'api/v0/' are used to simulate request sending to the respective urls, with data on registered
    players and game scores
"""

class Score(Form):
    SECRET_KEY = 'score_submit'
    player = SelectField('Player:')
    score = FloatField('Score:')
    details = StringField("Details:")
    game = SelectField("Game: ")
    time = DateTimeField()
    submit = SubmitField('Submit scores')


class Player(Form):
    SECRET_KEY = 'player_submit'
    username = StringField('Username:')
    name = StringField('Full name:')
    submit = SubmitField('Submit')