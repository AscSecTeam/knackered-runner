#Main.py

#This file intended to be the main orchestrating controller for service checks.

#Calls to run checks will be made here and passed back to here.
#This class connects the check-running scripts to the data-access class.

import threading

from DataAccess import DataAccess
from Runner import Runner


#Data access object - connects to MySQL database
#SELECTs service information, INSERTs check results
#Program will exit here if we can't connect to MySQL
database = DataAccess()

#Check runner object - runs checks for services with checkService() method
#Returns integer 1/0 for check pass/fail
#Default return is 9001 - if we see this in the database there is an issue with the checks
runner = Runner()


# We want the checks to run once per minute for each team.
# Using a threaded timer to accomplish this
def work():
    threading.Timer(3, work).start()

    #start the new round of checks
    runner.incrementRound()
    print "Running check round #" + str(runner.getRound())

    #Get teams from DB, loop through and check each service
    teams = database.getTeams()
    for team in teams:
        for service in team.getServices():
            runner.checkService(service)

    #after all teams are checked, deposit into DB (whole round at once)
    database.addCheckRound(teams)

work()