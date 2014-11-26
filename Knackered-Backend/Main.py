#Main.py

#This file intended to be the main orchestrating controller for service checks.

#Calls to run checks will be made here and passed back to here.
#This class connects the check-running scripts to the data-access class.

import threading
import sys

check_round = 0
if len(sys.argv) > 1 and sys.argv[1].isdigit():
    check_round = sys.argv[1]
    print check_round

from DataAccess import DataAccess
from Runner import Runner
from ChartGenerator import ChartGenerator



#Check runner object - runs checks for services with checkService() method
#Returns integer 1/0 for check pass/fail
#Default return is 9001 - if we see this in the database there is an issue with the checks
runner = Runner(check_round)

#Data access object - connects to MySQL database
#SELECTs service information, INSERTs check results
#Program will exit here if we can't connect to MySQL
testDatabase = DataAccess()
testDatabase.createTables()

chartGen = ChartGenerator()


# We want the checks to run once per minute for each team.
# Using a threaded timer to accomplish this
def check():
    threading.Timer(60, check).start()

    #start the new round of checks
    runner.incrementRound()

    #take note of the round now
    #if the current round does not finish before next one starts, we will enter the wrong round
    round = runner.getRound()

    database = DataAccess()

    #Get teams from DB, loop through and check each service
    teams = database.getTeams()
    for team in teams:
        for service in team.getServices():
            runner.checkService(service)

    #after all teams are checked, deposit into DB (whole round at once)
    database.addCheckRound(teams, round)

    teams = database.getScores()

    chartGen.generate_chart('/var/www/html/chart.svg', round, teams)

check()