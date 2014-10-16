#team.py

#Class for storing info about each team and the location of its services.

from Service import Service


class Team():

    def __init__(self, aId):
        self.id = aId
        self.services = []

    def addService(self, type, url, username, password):
        aService = Service(type, url, username, password)
        self.services.append(aService)

    def getServices(self):
        return self.services

    def getId(self):
        return self.id