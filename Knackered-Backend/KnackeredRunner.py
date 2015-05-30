# Main orchestrating object

# Calls to run checks will be made here and passed back to here.
# This class connects the check-running scripts to the data-access class.


import threading

from DataAccess import DataAccess
from Runner import Runner
from ChartGenerator import ChartGenerator

class KnackeredRunner:

    def __init__(self, check_round, web_root):
        self.chart_gen = ChartGenerator(web_root)

        # Check runner object - runs checks for services with checkService() method
        # Returns integer 1/0 for check pass/fail
        # Default return is 9001 - if we see this in the database there is an issue with the checks
        self.runner = Runner(check_round)
        self.check()

    # We want the checks to run once per minute for each team.
    # Using a threaded timer to accomplish this
    def check(self):
        threading.Timer(60, self.check).start()

        # start the new round of checks
        self.runner.increment_round()

        # take note of the round now
        # if the current round does not finish before next one starts, we will enter the wrong round
        current_round = self.runner.round

        database = DataAccess()

        # Get teams from DB, loop through and check each service
        teams = database.get_teams()
        for team in teams:
            for service in team.services:
                self.runner.check_service(service)

        # after all teams are checked, deposit into DB (whole round at once)
        database.add_check_round(teams, current_round)

        # generate chart for web interface
        teams = database.get_scores()
        self.chart_gen.generate_chart(current_round, teams)
