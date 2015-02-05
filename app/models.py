from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    pasword = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('roles.id'), default=1)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, username, password, name, role, is_deleted=False):
        self.username = username
        self.password = password
        self.name = name
        self.role = role
        self.is_deleted = is_deleted

    @staticmethod
    def superadmin():
        superadmin = Users.query.join(Roles).filter(Roles.role == "superadmin").first()
        if not superadmin:
            role = Roles.query.filter(Roles.role == "superadmin").first()
            insert = Users(username="super", password="super", name="super", role=role.id)
            db.session.add(insert)
            db.session.commit()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.pasword = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pasword, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return "{}".format(self.id)

    def can(self, permission):
        return self.role and (int(self.user_role.permission, base=16) & permission) == permission

    @classmethod
    def login(cls, username):
        return cls.query.filter(cls.username == username).first()

    @classmethod
    def take_id(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def list(cls, deleted):
        return cls.query.order_by(cls.username).filter(cls.is_deleted == deleted).all()

    @classmethod
    def count(cls):
        return cls.query.join(Roles).filter(Roles.role == "superadmin").filter(cls.is_deleted==False).count()

    @classmethod
    def find_user(cls, username):
        return cls.query.filter(cls.username == username).first()

    @classmethod
    def search_users(cls, search_string, deleted):
        return cls.query.join(Roles).filter(cls.username.like("%" + search_string + "%")|
                                                       cls.name.like("%" + search_string + "%")|
                                                       Roles.role.like("%" + search_string + "%")).\
                order_by(cls.username).filter(cls.is_deleted == deleted).all()

    @classmethod
    def insert_user(cls, username, password, name, role):
        user = cls(username=username, password=password, name=name, role=role)
        db.session.add(user)
        db.session.commit()
        return user

    def edit_user(self, username, password, name, role):
        self.username = username
        self.name = name
        self.role = role
        if password:
            self.password = password
        db.session.commit()
        return self

    @classmethod
    def delete_user(cls, user_id):
        user = cls.query.get(user_id)
        user.is_deleted = True
        db.session.commit()
        return user

    @classmethod
    def restore_user(cls, user_id):
        user = cls.query.get(user_id)
        user.is_deleted = False
        db.session.commit()
        return user


class Games(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    short_name = db.Column(db.String(6), nullable=False)
    name = db.Column(db.String(30), nullable=False, unique=True)
    version = db.Column(db.String(10), nullable=False)
    last_date = db.Column(db.String(30))
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    scores = db.relationship('Scores', backref='score_game')

    @classmethod
    def take_id(cls, game_id):
        return cls.query.get(game_id)

    @classmethod
    def list(cls, deleted):
        return cls.query.order_by(cls.name).filter(cls.is_deleted == deleted).all()

    @classmethod
    def find_name(cls, name):
        return cls.query.filter(cls.name == name).first()

    @classmethod
    def search_games(cls, search_string, deleted):
        return cls.query.filter(cls.short_name.like("%" + search_string + "%") |
                                cls.name.like("%" + search_string + "%") |
                                cls.version.like("%" + search_string + "%") |
                                cls.last_date.like("%" + search_string + "%")). \
            order_by(cls.short_name).filter(cls.is_deleted == deleted).all()

    @classmethod
    def insert_game(cls, short_name, name, version):
        game = cls(short_name=short_name, name=name, version=version, last_date=datetime.utcnow())
        db.session.add(game)
        db.session.commit()
        return game

    @classmethod
    def edit_game(cls, game_id, short_name, name, version):
        game = cls.query.get(game_id)
        game.short_name = short_name
        game.name = name
        game.version = version
        game.last_date = datetime.utcnow()
        db.session.commit()
        return game

    @classmethod
    def delete_game(cls, game_id):
        game = cls.query.get(game_id)
        game.is_deleted = True
        db.session.commit()
        return game


    @classmethod
    def restore_game(cls, game_id):
        game = cls.query.get(game_id)
        game.is_deleted = False
        db.session.commit()
        return game


class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.String(20), nullable=False, unique=True)
    permission = db.Column(db.String(8), nullable=False)
    users = db.relationship('Users', backref='user_role')
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    @staticmethod
    def insert_roles():
        roles = [
            {"role": "user", "permission": "0x01"},
            {"role": "admin", "permission": "0x03"},
            {"role": "superadmin", "permission": "0x0f"}
        ]
        for role in roles:
            r = Roles.query.filter(Roles.role == role['role']).first()
            if not r:
                insert = Roles(role=role['role'], permission=role['permission'])
                db.session.add(insert)
                db.session.commit()

    @classmethod
    def roles_all(cls):
        return cls.query.all()


class Permissions:
    USER = 0x01
    ADMIN = 0x03
    SUPERADMIN = 0x0f


class Scores(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    details = db.Column(db.Text)
    game = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    time = db.Column(db.String(30))
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    @classmethod
    def select(cls, select_string):
        return cls.query.join(Games).filter(Games.name == select_string).all()

    @classmethod
    def list(cls):
        return cls.query.join(Games).order_by(Games.name).filter(Games.is_deleted == False).all()

    @classmethod
    def list_all(cls):
        return cls.query.all()

    @classmethod
    def names(cls):
        return db.engine.execute("select distinct name from games as g inner join scores as s on g.id = s.game "
                              "where not g.is_deleted order by g.name")

    @classmethod
    def search_scores(cls, search_string):
        return cls.query.join(Games).filter(cls.player.like("%" + search_string + "%")|
                                           cls.score.like("%" + search_string + "%")|
                                           Games.name.like("%" + search_string + "%")|
                                           cls.time.like("%" + search_string + "%")).\
                order_by(Games.name).filter(cls.is_deleted == False).filter(Games.is_deleted == False).all()

    @classmethod
    def insert_score(cls, player, score, details, game, time):
        score = cls(player=player, score=score, details=details, game=game, time=time)
        db.session.add(score)
        db.session.commit()
        return score


class Players(db.Model):
    """
    Class represents model about players
    """
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    scores = db.relationship('Scores', backref='score_player')

    @classmethod
    def list(cls):
        """
        This methods list all users that are not deleted (is_deleted=False)
        :return:
        :rtype: list[Players]
        """
        return cls.query.filter(cls.is_deleted == False).all()

    @classmethod
    def insert_player(cls, username, name):
        """
        Inserts new player into database
        :param username: username of player
        :type username: str
        :param name: name of player
        :type name: str
        :return: player that has been inserted into database
        ":rtype: Players
        """
        player = cls(username=username, name=name)
        db.session.add(player)
        db.session.commit()
        return player

    @classmethod
    def find_player(cls, username):
        return cls.query.filter(cls.username == username).first()




















