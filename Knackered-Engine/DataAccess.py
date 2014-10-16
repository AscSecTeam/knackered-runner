#DataAccess.py

#This class serves to connect to the MySQL database.

import mysql.connector
from mysql.connector import errorcode
from collections import OrderedDict

##############################################
######CONFIGURE DATABASE CONNECTION HERE######
##############################################
DATABASE_USERNAME = "root"
DATABASE_PASSWORD = ""
DATABASE_ADDRESS = "localhost"
DATABASE_NAME = "Scoring"
DATABASE_SCHEMA = OrderedDict()

DATABASE_SCHEMA['TEAMS'] = """
    CREATE TABLE Teams (
      id INT PRIMARY KEY
    )
"""

DATABASE_SCHEMA['SERVICES'] = """
    CREATE TABLE Services (
      id INT PRIMARY KEY,
      teamId INT,
      address VARCHAR(50),
      FOREIGN KEY (teamId) REFERENCES Teams(id)
    )
"""

DATABASE_SCHEMA['TEAMLOGINS'] = """
    CREATE TABLE TeamLogins (
      id INT PRIMARY KEY AUTO_INCREMENT,
      teamId INT,
      username varchar(100),
      password varchar(100),
      FOREIGN KEY (teamId) REFERENCES Teams(id)
    )
"""

DATABASE_SCHEMA['CHECKS'] = """
    CREATE TABLE Checks (
      id INT PRIMARY KEY AUTO_INCREMENT,
      serviceId INT,
      round INT,
      result INT,
      FOREIGN KEY (serviceId) REFERENCES Services(id)
    )
"""

DATABASE_SCHEMA['SERVICELOGINS'] = """
    CREATE TABLE ServiceLogins (
      id INT PRIMARY KEY AUTO_INCREMENT,
      serviceId INT,
      username varchar(100),
      password varchar(100),
      FOREIGN KEY (serviceId) REFERENCES Services(id)
    )
"""


class DataAccess():

    def __init__(self):
        #Store configured settings
        self.username = DATABASE_USERNAME
        self.password = DATABASE_PASSWORD
        self.address = DATABASE_ADDRESS
        self.dbname = DATABASE_NAME
        self.schema = DATABASE_SCHEMA

        #init database connection using settings above
        self.connection = mysql.connector.connect(user=self.username,
                                                  password=self.password,
                                                  host=self.address,)
        self.cursor = self.connection.cursor()

        #connect to the database
        #create the DB if it does not exist
        try:
            self.connection.database = self.dbname
            print "Database already created, woohoo"
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.createDB()
                print "Created database."
                self.connection.database = self.dbname
            else:
                #if the connection is broken, rage-quit the program
                print """
                    Can't connect to the MySQL Database.
                    Ensure service is started. (service mysql start)
                    Ensure database user info is correct (EDIT DataAccess.spy)
                """
                print(err)
                exit(1)

        #Now that we have the connection, let's make sure the necessary tables are here
        for tablename, table in self.schema.items():
            try:
                self.cursor.execute(table)
                self.connection.commit()
                print "Created table " + tablename
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print "Table " + tablename + " already exists, woohoo"
                else:
                    print err.msg

    #Connects to DB and returns list of teams
    def getTeams(self):  # TODO
        teamsList = []
        return teamsList

    #Connects to DB and inserts a round's check results
    def addCheckRound(self, teams):  # TODO
        for team in teams:
            print team

    def createDB(self):
        try:
            self.cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.dbname))
            self.connection.commit()

        except mysql.connector.Error as err:
            #if the connection is broken, rage-quit the program
            print """
                Can't connect to the MySQL Database.
                Ensure service is started. (service mysql start)
                Ensure database user info is correct (EDIT DataAccess.py)
            """
            print("Failed creating database: {}".format(err))
            exit(1)
