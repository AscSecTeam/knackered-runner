# This class intended to receive check requests
# and use the ./scripts directory to make the checks and then return results of these checks.

import subprocess

# Specify plugin directory path here
PLUGIN_DIRECTORY = "/usr/lib/nagios/plugins/"


class Runner:

    def __init__(self, check_round):
        self.round = check_round
        self.plugin_dir = PLUGIN_DIRECTORY
        print "Runner initialized."

    def check_service(self, service):
        result = 9001
        """ 9001 is the default return value. if we see this in the checks table,
        there is a service that is not accounted for by a check
        or a reason that result is not being reassigned. Panic regardless.
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        Checks should be called from below.
        the result variables below are binary representations of the check's score.
        The database supports integer results though,
        so if we need to pass things such as http status codes as a result, we can do that. """

        if service.type == 'dns':
            command = self.plugin_dir + 'check_dns'
            arg_one = 'google.com'
            arg_two = service.address
            run = subprocess.Popen([command, arg_one, arg_two], stdout=subprocess.PIPE)
            status = run.stdout.read()
            if status.find('OK') != -1:  # Include expected result comparison
                result = 1
                print service.type + '   OK ON       ' + service.address
            else:
                result = 0
                print service.type + '   CRITICAL ON ' + service.address

        elif service.type == 'smtp':
            command = self.plugin_dir + 'check_smtp'
            args = service.address
            run = subprocess.Popen([command, args], stdout=subprocess.PIPE)
            status = run.stdout.read()
            if status.find('SMTP OK') != -1:
                result = 1
                print service.type + '  OK ON       ' + service.address
            else:
                result = 0
                print service.type + '  CRITICAL ON ' + service.address

        elif service.type == 'icmp':
            command = self.plugin_dir + 'check_icmp'
            args = service.address
            run = subprocess.Popen([command, args], stdout=subprocess.PIPE)
            status = run.stdout.read()
            if status.find('OK') != -1:
                result = 1
                print service.type + '  OK ON       ' + service.address
            else:
                result = 0
                print service.type + '  CRITICAL ON ' + service.address

        elif service.type == 'ssh':
            command = self.plugin_dir + 'check_ssh'
            args = service.address
            run = subprocess.Popen([command, args], stdout=subprocess.PIPE)
            status = run.stdout.read()
            if status.find('SSH OK') != -1:  # Include expected result comparison
                result = 1
                print service.type + '   OK ON       ' + service.address
            else:
                result = 0
                print service.type + '   CRITICAL ON ' + service.address

        elif service.type == 'ftp':
            command = self.plugin_dir + 'check_ftp'
            arg_one = '-H'
            arg_two = service.address
            run = subprocess.Popen([command, arg_one, arg_two], stdout=subprocess.PIPE)
            status = run.stdout.read()
            if status.find('FTP OK') != -1:
                result = 1
                print service.type + '   OK ON       ' + service.address
            else:
                result = 0
                print service.type + '   CRITICAL ON ' + service.address

        elif service.type == 'http':
            command = self.plugin_dir + 'check_http'
            arg_one = '-I'
            arg_two = service.address
            run = subprocess.Popen([command, arg_one, arg_two], stdout=subprocess.PIPE)
            status = run.stdout.read()
            if status.find('HTTP OK') != -1:
                result = 1
                print service.type + '  OK ON       ' + service.address
            else:
                result = 0
                print service.type + '  CRITICAL ON ' + service.address

        elif service.type == 'https':
            command = self.plugin_dir + 'check_http'
            arg_one = '-S'
            arg_two = '-I'
            arg_three = service.address
            run = subprocess.Popen([command, arg_one, arg_two, arg_three], stdout=subprocess.PIPE)
            status = run.stdout.read()
            if status.find('HTTP OK') != -1:
                result = 1
                print service.type + ' OK ON       ' + service.address
            else:
                result = 0
                print service.type + ' CRITICAL ON ' + service.address

        if result == 9001:
            print "Service with id " + str(service.id) + " has failed to find an appropriate check type"

        service.add_check(result)

    def increment_round(self):
        self.round += 1
