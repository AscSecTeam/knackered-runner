# Class for storing info about each team and the location of its services.

from Service import Service


class Team:

    def __init__(self, team_id):
        self.id = team_id
        self.services = []
        self.score = 0

    def add_service(self, service_id, service_type, url, username, password):
        self.services.append(Service(service_id, service_type, url, username, password))

    def add_to_score(self, score):
        self.score += score
