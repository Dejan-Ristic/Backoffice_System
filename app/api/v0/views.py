from flask import render_template, Response, redirect, request
from . import v0
from app import db
from .forrms import Score, Player
from app.models import Scores, Games, Players
import json
from datetime import datetime

""" This page is only for API testing.
    Score() and Player() forms are used to simulate the requests (json format) sent to server to respective urls.

    'Games.list()' class method is used to obtain records on all active games from the database, to be diplayed in
    the 'score' form.
    'Players.list()' class method is used to obtain records on all players from the database, to be displayed in
    the 'score' form.
"""

@v0.route('/', methods=['GET', 'POST'])
def index():
    score = Score()
    player = Player()
    player_names = Players.list()
    game_names = Games.list(False)
    time_now = datetime.utcnow()
    if score.validate_on_submit():
        if score.player.data and score.score.data and score.details.data and score.game.data and score.time.data:
            return redirect("/scores-sent")
    if player.validate_on_submit():
        if player.username.data and player.name.data:
            return redirect("/player-sent")
    return render_template("api/scores.html", score=score, player=player, time_now=time_now, game_names=game_names,
                           player_names=player_names)


""" url to which post requests are sent containing the player data used for player registration.
    Requests are sent in json format and are entered into Players database table.
    'Players.insert_player()' class method is called to insert the data on new player in the database.
"""
@v0.route('/player-sent', methods=['POST'])
def player_sent():
    result = request.json
    Players.insert_player(result['username'], result['name'])
    return Response(response='{"status":"ok"}', status=201, mimetype='application/json')


""" url to which post requests are sent containing the score data for respective game and respective player.
    Requests are sent in json format and are entered into Scores database table.
    'Games.find_name()' and 'Players.find_player()' class method are used to obtain the game name and player username
    by their respective ids.
    'Scores.insert_score()' class method enters the data on new score into the 'scores' database table.
"""
@v0.route('/scores-sent', methods=['POST'])
def scores_sent():
    result = request.json
    game = Games.find_name(result['game'])
    player = Players.find_player(result['player'])
    Scores.insert_score(player.id, result['score'], json.dumps(result['details']), game.id, result['time'])
    return Response(response='{"status":"ok"}', status=201, mimetype='application/json')


""" url to which get requests for high scores are sent.
    All scores are taken from Scores database table and sent in a response in json format.
    Data in 'details' column in Scores table are stored in json format.
    'Scores.list_all()' class method is used to obtain all the scores for all the games from the database.
"""

@v0.route('/get-high-scores', methods=['GET'])
def get_high_scores():
    json_list = []
    scores = Scores.list_all()
    for score in scores:
        record = {
            "id": score.id,
            "player": score.score_player.username,
            "score": score.score,
            "details": json.loads(score.details),
            "game": score.score_game.name,
            "time": score.time
        }
        json_list.append(record)
    response = json.dumps(json_list)
    return Response(response=response, status=200, mimetype='application/json')