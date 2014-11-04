#service.py

#Class for storing information about once service for one team.

from Login import Login
from Check import Check


class Service():
  
    def __init__(self, aId, aType, aAddress, aUsername, aPassword):
        self.id = aId
        self.type = aType                          # this is the type of check to run on the address
        self.address = aAddress                    # url/ip of the service
        self.login = Login(aUsername, aPassword)   # Some services may need login information
        self.checked = False                       # Has this already been checked?
        self.result = Check()

    def getId(self):
        return self.id

    def getType(self):
        return self.type

    def getAddress(self):
        return self.address

    def getUsername(self):
        return self.login.getUsername()

    def getPassword(self):
        return self.login.getPassword()

    def addCheck(self, result):
        if not self.checked:
            self.result.setPassed(result)
            self.checked = True
        else:
            print 'Warning: Service at' + self.address + 'has attempted to overwrite check'

    def getCheck(self):
        return self.result.isPassed()