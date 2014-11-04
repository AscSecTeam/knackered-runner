#login.py

#this rather simple class is for storing login information


class Login():

    def __init__(self, aUsername, aPassword):
        self.username = aUsername
        self.password = aPassword

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password