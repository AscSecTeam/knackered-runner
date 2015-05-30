# Class for storing information about once service for one team.

from Login import Login

class Service:
  
    def __init__(self, service_id, service_type, address, username, password):
        self.id = service_id
        self.type = service_type                 # this is the type of check to run on the address
        self.address = address                   # url/ip of the service
        self.login = Login(username, password)   # Some services may need login information
        self.result = None

    def add_check(self, result):
        if result is None:
            self.result = result
        else:
            print 'Warning: Service at' + self.address + 'has attempted to overwrite check'

    def get_check(self):
        return self.result
