import unittest
from app import create_app, db
from app.models import Users, Roles, Games, Scores, Players


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        from app.models import Roles
        Roles.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_insert(self):
        user = Users.insert_user("one", "one", "one", 2)
        self.assertEquals(user.username, "one")

        user2 = Users.login("one")
        self.assertEquals(user2.username, "one")

    def test_user_edit(self):
        self.test_user_insert()
        user = Users.take_id(1)
        user.edit_user("two", "two", "two", 3)
        self.assertEquals(user.username, "two")
        self.assertEquals(user.name, "two")
        self.assertEquals(user.user_role.role, "superadmin")


    def test_user(self):
        self.test_user_edit()



        search = Users.search_users("two", False)
        for user in search:
            self.assertEquals(user.username, "two")

        new_user_check = Users.find_user("one")
        self.assertEquals(new_user_check, None)

        new_user_check = Users.find_user("two")
        self.assertEquals(new_user_check.username, "two")

        getby_id = Users.take_id(1)
        self.assertEquals(getby_id.username, "two")

        user4 = Users.insert_user("three", "three", "three", 1)
        self.assertEquals(user4.user_role.role, "user")

        user5 = Users.insert_user("four", "four", "four", 2)
        self.assertEquals(user5.user_role.role, "admin")

        count = Users.count()
        self.assertEquals(count, 1)

        list = Users.list(False)
        i = 0
        for l in list:
            i+=1
        self.assertEquals(i, 3)

        delete = Users.delete_user(1)
        self.assertEquals(delete.is_deleted, True)

        list = Users.list(True)
        i = 0
        for l in list:
            i+=1
        self.assertEquals(i, 1)

        search = Users.search_users("ne", True)
        for user in search:
            self.assertEquals(user.username, "one")

        restore = Users.restore_user(1)
        self.assertEquals(restore.is_deleted, False)


    def test_roles(self):
        roles = Roles.roles_all()
        list = []
        for role in roles:
            list.append(role.role)
        self.assertEquals(list[0], "user")
        self.assertEquals(list[1], "admin")
        self.assertEquals(list[2], "superadmin")


    def test_game(self):
        game = Games.insert_game("tr", "tomb raider", "1")
        self.assertEquals(game.short_name, "tr")

        game_edit = Games.edit_game(1, "tr", "tomb raider 2", "2")
        self.assertEquals(game_edit.short_name, "tr")
        self.assertEquals(game_edit.name, "tomb raider 2")
        self.assertEquals(game_edit.version, "2")

        game2 = Games.insert_game("bo", "burnout", "vv")
        self.assertEquals(game2.short_name, "bo")

        new_game_check = Games.find_name("tt")
        self.assertEquals(new_game_check, None)

        new_game_check = Games.find_name("burnout")
        self.assertEquals(new_game_check.version, "vv")

        getby_id = Games.take_id(1)
        self.assertEquals(getby_id.name, "tomb raider 2")

        list = Games.list(False)
        i = 0
        for l in list:
            i+=1
        self.assertEquals(i, 2)

        delete = Games.delete_game(1)
        self.assertEquals(delete.is_deleted, True)

        list = Games.list(True)
        i = 0
        for l in list:
            i+=1
        self.assertEquals(i, 1)

        search = Games.search_games("tomb", True)
        for game in search:
            self.assertEquals(game.name, "tomb raider 2")

        restore = Games.restore_game(1)
        self.assertEquals(restore.is_deleted, False)

        search = Games.search_games("burn", False)
        for game in search:
            self.assertEquals(game.name, "burnout")


    def test_players_scores(self):
        player = Players.insert_player("one", "one")
        self.assertEquals(player.username, "one")

        player2 = Players.insert_player("two", "two")
        self.assertEquals(player2.name, "two")

        find_player = Players.find_player("one")
        self.assertEquals(find_player.username, "one")

        list = Players.list()
        i = 0
        for l in list:
            i+=1
        self.assertEquals(i, 2)

        game = Games.insert_game("tr", "tomb raider", "1")
        self.assertEquals(game.short_name, "tr")

        game2 = Games.insert_game("bo", "burnout", "vv")
        self.assertEquals(game2.short_name, "bo")

        score = Scores.insert_score(1, 666, '{"dasfd":"asdf"}', 1, "time")
        self.assertEquals(score.score_player.username, "one")

        score2 = Scores.insert_score(2, 666, '{"dasfd":"asdf"}', 2, "time")
        self.assertEquals(score2.score_game.name, "burnout")

        scores = Scores.list_all()
        i = 0
        for s in scores:
            i+=1
        self.assertEquals(i, 2)

        delete = Games.delete_game(1)
        self.assertEquals(delete.is_deleted, True)

        scores = Scores.list()
        i = 0
        for s in scores:
            i+=1
        self.assertEquals(i, 1)

        restore = Games.restore_game(1)
        self.assertEquals(restore.is_deleted, False)

        search = Scores.search_scores("time")
        i = 0
        for s in search:
            i+=1
        self.assertEquals(i, 2)

        search = Scores.search_scores("burn")
        i = 0
        for s in search:
            i+=1
        self.assertEquals(i, 1)

        select = Scores.select("tomb raider")
        for s in select:
            self.assertEquals(s.game, 1)

        select = Scores.select("tomb")
        for s in select:
            self.assertEquals(s, None)

        names = Scores.names()
        list = []
        for name in names:
            list.append(name.name)
        self.assertEquals(list[0], "burnout")
        self.assertEquals(list[1], "tomb raider")


if __name__ == '__main__':
    unittest.main()
