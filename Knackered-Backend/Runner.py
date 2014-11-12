#runner.py

#This class intended to receive check requests
#and use the ./scripts directory to make the checks and then return results of these checks.

import subprocess

#Specify plugin directory path here
PLUGIN_DIRECTORY = "/usr/lib/nagios/plugins/"


class Runner():

    def __init__(self):
        self.round = 0
        self.plugindir = PLUGIN_DIRECTORY
        print "Runner initialized."

    def checkService(self, aService):
        result = 9001
        """ 9001 is the default return value. if we see this in the checks table,
        there is a service that is not accounted for by a check
        or a reason that result is not being reassigned. Panic regardless.
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        Checks should be called from below.
        the result variables below are binary representations of the check's score.
        The database supports integer results though,
        so if we need to pass things such as http status codes as a result, we can do that. """

        if aService.getType() == 'dns':
            #TODO Compare with expected result
            #Temp using google.com
            command = self.plugindir + 'check_dns'
            argone = 'google.com'
            argtwo = aService.getAddress()
            run = subprocess.Popen([command, argone, argtwo], stdout=subprocess.PIPE)
            status = run.stdout.read()
            if status.find('OK') != -1:  # Include expected result comparison
                result = 1
                print aService.getType() + ' OK ON ' + aService.getAddress()
            else:
                result = 0
                print aService.getType() + ' CRITICAL ON ' + aService.getAddress()

        elif aService.getType() == 'smtp':
            command = self.plugindir + 'check_smtp'
            args = aService.getAddress()
            run = subprocess.Popen([command, args], stdout=subprocess.PIPE)
            status = run.stdout.read()
            if status.find('SMTP OK') != -1:
                result = 1
                print aService.getType() + ' OK ON ' + aService.getAddress()
            else:
                result = 0
                print aService.getType() + ' CRITICAL ON ' + aService.getAddress()

        elif aService.getType() == 'icmp':
            command = self.plugindir + 'check_icmp'
            args = aService.getAddress()
            run = subprocess.Popen([command, args], stdout=subprocess.PIPE)
            status = run.stdout.read()
            if status.find('OK') != -1:
                result = 1
                print aService.getType() + ' OK ON ' + aService.getAddress()
            else:
                result = 0
                print aService.getType() + ' CRITICAL ON ' + aService.getAddress()

        elif aService.getType() == 'ssh':
            #TODO Compare with expected result
            command = self.plugindir + 'check_ssh'
            args = aService.getAddress()
            run = subprocess.Popen([command, args], stdout=subprocess.PIPE)
            status = run.stdout.read()
            if status.find('SSH OK') != -1:  # Include expected result comparison
                result = 1
                print aService.getType() + ' OK ON ' + aService.getAddress()
            else:
                result = 0
                print aService.getType() + ' CRITICAL ON ' + aService.getAddress()

        elif aService.getType() == 'ftp':
            #TODO Compare with expected result
            command = self.plugindir + 'check_ftp'
            argone = '-H'
            argtwo = aService.getAddress()
            run = subprocess.Popen([command, argone, argtwo], stdout=subprocess.PIPE)
            status = run.stdout.read()
            if status.find('FTP OK') != -1:
                result = 1
                print aService.getType() + ' OK ON ' + aService.getAddress()
            else:
                result = 0
                print aService.getType() + ' CRITICAL ON ' + aService.getAddress()

        elif aService.getType() == 'http':
            #TODO Compare with expected result
            command = self.plugindir + 'check_http'
            argone = '-I'
            argtwo = aService.getAddress()
            run = subprocess.Popen([command, argone, argtwo], stdout=subprocess.PIPE)
            status = run.stdout.read()
            if status.find('HTTP OK') != -1:
                result = 1
                print aService.getType() + ' OK ON ' + aService.getAddress()
            else:
                result = 0
                print aService.getType() + ' CRITICAL ON ' + aService.getAddress()

        elif aService.getType() == 'https':
            #TODO Compare with expected result
            command = self.plugindir + 'check_http'
            argone = '-S'
            argtwo = '-I'
            argthree = aService.getAddress()
            run = subprocess.Popen([command, argone, argtwo, argthree], stdout=subprocess.PIPE)
            status = run.stdout.read()
            if status.find('HTTP OK') != -1:
                result = 1
                print aService.getType() + ' OK ON ' + aService.getAddress()
            else:
                result = 0
                print aService.getType() + ' CRITICAL ON ' + aService.getAddress()

        if result == 9001:
            print "Service with id " + str(aService.getId()) + " has failed to find an appropriate check type"

        aService.addCheck(result)

    def getRound(self):
        return self.round

    def incrementRound(self):
        self.round += 1