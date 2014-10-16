#check.py

#this rather simple class is for storing check results and sending them to the data access class.


class Check():
  
    def __init__(self):
        self.result = None

    def isPassed(self):
        return self.result

    def setPassed(self, aResult):
        result = aResult