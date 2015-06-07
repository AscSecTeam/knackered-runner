from flask.ext.login import UserMixin

class User(UserMixin):

    # proxy for a database of users
    # Username, Password, Team Number
    user_database = {"JohnDoe": ("JohnDoe", "John", 0),
                     "JaneDoe": ("JaneDoe", "Jane", 1)}

    def __init__(self, username, password):
        self.id = 4
        self.username = username
        self.password = password

    # def save(self):
    @classmethod
    def get_by_id(cls, id):
        return User(cls.user_database.get(id)[0], cls.user_database.get(id)[1])

    @classmethod
    def get_by_name(cls, username):
        for user in cls.user_database:
            if cls.user_database.get(user)[0] == username:
                return User(cls.user_database.get(user)[0], cls.user_database.get(user)[1])
        return None

    @classmethod
    def is_valid(cls, username, password):
        user = cls.get_by_name(username)
        if user is not None:
            return username == user.username and password == user.password
        return False
