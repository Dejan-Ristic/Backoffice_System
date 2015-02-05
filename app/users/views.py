from flask import render_template, redirect, flash, request
from . import allusers
from .forrms import GameInsertEdit, UserInsertEdit, Search, Confirm, SelectGame
from ..models import Users, Games, Roles, Permissions, Scores
from flask_login import login_required, current_user, logout_user
from app.decorators import permission_required

""" The permissions to all routes and functions are separated in three groups: USER, ADMIN and SUPERADMIN.
    These permissions are defined in Models.Permissions class.
    User of USER type has permission to list the data on games and scores.
    User of ADMIN type can additionally edit and delete games. Also, deleted games can be restored.
    User of SUPERADMIN type can access data on all users who are using the application. Data on users and their
    permissions can be edited by Superadmin.
"""

@allusers.route('/secret')
@login_required
def secret():
    return redirect('/')


""" Logout function redirects the user to index page at logout
"""
@allusers.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


""" Active games are displayed on Games page via 'Games.list()' class method. The (False) argument in this function
    filters the data from 'games' table so that only games which are not deleted are displayed.

    'new_game' is the form used to insert new game data. 'find_game' class method is called to check if the
    game with the same name already exists and redirects the user to the same page if it does. If it doesn't,
    'insert_game' class method is used to insert the new game in the database.

    'search' is the form used to enter data which the user searches for in displayed games.
    'search_games' class method is called to compare every field of every active (non-deleted) game and search for all
    similarities with the data entered in 'search' form.
"""
@allusers.route('/games', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.USER)
def games():
    new_game = GameInsertEdit()
    search = Search()
    if search.validate_on_submit():
        if search.search_item.data:
            games = Games.search_games(search.search_item.data, False)
            return render_template("views/games.html", user=current_user, games=games, search=search,
                                   new_game=new_game)
    if new_game.validate_on_submit():
        if new_game.short_name.data and new_game.name.data and new_game.version.data:
            a_game = Games.find_name(new_game.name.data)
            if a_game:
                flash('There already is a game with this name')
                return redirect('/allusers/games')
            Games.insert_game(new_game.short_name.data, new_game.name.data, new_game.version.data)
            return redirect('/allusers/games')
    games = Games.list(False)
    return render_template("views/games.html", user=current_user, games=games, search=search,
                           new_game=new_game)


""" All scores for all active games are displayed on Scores page via 'Scores.list()' class method.

    'Scores.names()' class method is used to create the object containing all the games which are not deleted and
    for which at least one score entry in the 'scores' table exists. This object is used in the 'views/scores.html'
    template to display the game names in the drop-down menu. 'Scores.select()' class method is used to display the
    scores for a game selected in the drop-down menu.

    'search' is the form used to enter data which the user searches for in displayed scores.
    'search_scores' class method is called to compare every field of every score for active games and search for all
    similarities with the data entered in 'search' form.
"""
@allusers.route('/scores', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.USER)
def scores():
    sel_game = SelectGame()
    names = Scores.names()
    search = Search()
    if search.validate_on_submit():
        if search.search_item.data:
            scores = Scores.search_scores(search.search_item.data)
            return render_template("views/scores.html", user=current_user, scores=scores, search=search,
                                   sel_game=sel_game, names=names)
    if sel_game.validate_on_submit():
        if sel_game.select_game.data == "All games":
            scores = Scores.list()
        else:
            scores = Scores.select(sel_game.select_game.data)
        return render_template("views/scores.html", user=current_user, scores=scores, search=search,
                                       sel_game=sel_game, names=names)
    scores = Scores.list()
    return render_template("views/scores.html", user=current_user, scores=scores, search=search,
                           sel_game=sel_game, names=names)


""" 'Games.take_id()' class method id used to obtain the data on the game to be edited from the database.
    If 'id' is not received from the Games page, the user is redirected to '/allusers/games' route.

    The instance of 'GameInsertEdit()' class is the form used to edit the data on existing game by calling the
    'Games.edit_game()' class method.

    'Games.delete_game()' is called to delete the game.
"""
@allusers.route('/edit-game', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.ADMIN)
def edit_game():
    edit_id = request.args.get('id')
    if not edit_id:
        return redirect('/allusers/games')
    game = Games.take_id(edit_id)
    delete = Confirm()
    edit_game = GameInsertEdit()
    if edit_game.validate_on_submit():
        if edit_game.short_name.data and edit_game.name.data and edit_game.version.data:
            Games.edit_game(edit_id, edit_game.short_name.data, edit_game.name.data, edit_game.version.data)
            return redirect('/allusers/games')
    if delete.validate_on_submit():
        Games.delete_game(edit_id)
        return redirect('/allusers/games')
    return render_template("views/edit_game.html", game=game, edit_game=edit_game, delete=delete)


""" '/deleted-games' is the page on which all deleted games are displayed by calling the 'Games.list(True)' class
    method.
    'Games.search_games()' class method is used to search through all deleted games (is_deleted = True)
"""
@allusers.route('/deleted-games', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.ADMIN)
def deleted_games():
    search = Search()
    if search.validate_on_submit():
        if search.search_item.data:
            games = Games.search_games(search.search_item.data, True)
            return render_template("views/deleted_games.html", user=current_user, games=games, search=search)
    games = Games.list(True)
    return render_template("views/deleted_games.html", user=current_user, games=games, search=search)


""" A game selected on '/deleted-games' can be restored and returned to active games by calling the
    'Games.restore_game()' class method.
"""
@allusers.route('/restore-game', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.ADMIN)
def restore_game():
    restore_id = request.args.get('id')
    if not restore_id:
        return redirect('/allusers/games')
    game = Games.take_id(restore_id)
    restore = Confirm()
    if restore.validate_on_submit():
        Games.restore_game(restore_id)
        return redirect('/allusers/games')
    return render_template("views/restore_game.html", game=game, restore=restore)


""" Active users are displayed on Users page via 'Users.list()' class method. The (False) argument in this function
    filters the data from 'games' table so that only games which are not deleted are displayed.

    'new_user' is the form used to insert new user data. 'find_user' class method is called to check if the
    user with the same username already exists and redirects the user to the same page if it does. If it doesn't,
    'insert_user' class method is used to insert the new user in the database.

    'search' is the form used to enter data which the user searches for in displayed users.
    'search_users' class method is called to compare every field of every active (non-deleted) user and search for all
    similarities with the data entered in 'search' form.
"""
@allusers.route('/users', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.SUPERADMIN)
def users():
    new_user = UserInsertEdit()
    search = Search()
    role_names = Roles.roles_all()
    if search.validate_on_submit():
        if search.search_item.data:
            users = Users.search_users(search.search_item.data, False)
            return render_template("views/users.html", user=current_user, users=users, search=search,
                                   new_user=new_user, role_names=role_names)
    if new_user.validate_on_submit():
        if new_user.username.data and new_user.password.data and new_user.name.data and new_user.role.data:
            a_user = Users.find_user(new_user.username.data)
            if a_user:
                flash('There already is a user with this username')
                return redirect('/allusers/users')
            Users.insert_user(new_user.username.data, new_user.password.data, new_user.name.data, new_user.role.data)
            return redirect('/allusers/users')
    users = Users.list(False)
    return render_template("views/users.html", user=current_user, users=users, search=search,
                           new_user=new_user, role_names=role_names)


""" 'Users.take_id()' class method id used to obtain the data on the user to be edited from the database.
    If 'id' is not received from the Users page, the user is redirected to '/allusers/users' route.

    The instance of 'UserInsertEdit()' class is the form used to edit the data on existing user by calling the
    'Users.edit_user()' class method.

    'Users.delete_user()' is called to delete the game.
"""
@allusers.route('/edit-user', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.SUPERADMIN)
def edit_user():
    edit_id = request.args.get('id')
    if not edit_id:
        return redirect('/allusers/users')
    user = Users.take_id(edit_id)
    edit_user = UserInsertEdit()
    role_names = Roles.roles_all()
    superadmin_id = []
    for name in role_names:
        if name.role == user.user_role.role:
            superadmin_id = name.id
    delete = Confirm()
    count = Users.count()
    if edit_user.validate_on_submit():
        if edit_user.username.data and edit_user.name.data and edit_user.role.data:
            if count == 1 and user.user_role.role == "superadmin" and edit_user.role.data != superadmin_id:
                flash("There has to be at least one superadmin")
                return redirect('/allusers/users')
            user.edit_user(edit_user.username.data, edit_user.password.data, edit_user.name.data, edit_user.role.data)
            return redirect('/allusers/users')
    if delete.validate_on_submit():
        if count == 1 and user.user_role.role == "superadmin":
            flash("There has to be at least one superadmin")
            return redirect('/allusers/users')
        Users.delete_user(edit_id)
        return redirect('/allusers/users')
    return render_template("views/edit_user.html", user=user, edit_user=edit_user, delete=delete, role_names=role_names)


""" '/deleted-users' is the page on which all deleted users are displayed by calling the 'Users.list(True)' class
    method.
    'Users.search_users()' class method is used to search through all deleted users (is_deleted = True)
"""
@allusers.route('/deleted-users', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.SUPERADMIN)
def deleted_users():
    search = Search()
    if search.validate_on_submit():
        if search.search_item.data:
            users = Users.search_users(search.search_item.data, True)
            return render_template("views/deleted_users.html", user=current_user, users=users, search=search)
    users = Users.list(True)
    return render_template("views/deleted_users.html", user=current_user, users=users, search=search)



@allusers.route('/restore-user', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.SUPERADMIN)
def restore_user():
    """ A user selected on '/deleted-users' can be restored and returned to active users by calling the
    'Users.restore_user()' class method.
    """
    restore_id = request.args.get('id')
    if not restore_id:
        return redirect('/allusers/users')
    user = Users.take_id(restore_id)
    restore = Confirm()
    if restore.validate_on_submit():
        Users.restore_user(restore_id)
        return redirect('/allusers/users')
    return render_template("views/restore_user.html", user=user, restore=restore)