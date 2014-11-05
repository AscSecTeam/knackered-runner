#runner.py

#This class intended to receive check requests
#and use the ./scripts directory to make the checks and then return results of these checks.

#Specify plugin directory path here
PLUGIN_DIRECTORY = "/usr/lib/nagios/plugins/"

from subprocess import call

class Runner():

    def __init__(self):
        self.round = 0
        self.plugindir = PLUGIN_DIRECTORY
        print "Runner initialized."

    def checkService(self, aService):
        result = 9001  # default return value. if we see this in the checks table,
                       # there is a service that is not accounted for by a check
                       # Or a reason that result is not being reassigned. Panic regardless.

        # Checks should be called from below.
        # the result variables below are binary representations of the check's score.
        # The database supports integer results though,
        # so if we need to pass things such as http status codes as a result, we can do that.

        if aService.getType() == 'dns':
            result = 0  # RUN CHECK HERE

        elif aService.getType() == 'smtp':
            result = 0  # RUN CHECK HERE

        elif aService.getType() == 'icmp':
            result = 0  # RUN CHECK HERE

        elif aService.getType() == 'imap':
            result = 0  # RUN CHECK HERE

        elif aService.getType() == 'pop3':
            result = 0  # RUN CHECK HERE

        elif aService.getType() == 'ssh':
            result = 0  # RUN CHECK HERE

        elif aService.getType() == 'ftp':
            result = 0  # RUN CHECK HERE

        elif aService.getType() == 'http':
            #Welp i just realized i need to add in what to look for in the http check TODO
            command = self.plugindir + 'check_http -H ' + aService.getAddress()
            print call(command)
            result = 0  # RUN CHECK HERE

        elif aService.getType() == 'https':
            result = 0  # RUN CHECK HERE

        if result == 9001:
            print "Service with id " + str(aService.getId()) + " has failed to find an appropriate check type"

        aService.addCheck(result)

    def getRound(self):
        return self.round

    def incrementRound(self):
        self.round += 1