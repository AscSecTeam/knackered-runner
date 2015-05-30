# This file intended to run and test knackered-runner standalone.

import sys

from DataAccess import DataAccess
from KnackeredRunner import KnackeredRunner
from Conf import Conf

config = Conf()

check_round = 0
if len(sys.argv) > 1 and sys.argv[1].isdigit():
    check_round = sys.argv[1]
    print "Starting from round #" + str(check_round)

# Data access object - connects to MySQL database
# Selects service information, inserts check results
# Program will exit here if we can't connect to MySQL
testDatabase = DataAccess()
testDatabase.create_tables()

knackered = KnackeredRunner(check_round, config.WEB_ROOT)
