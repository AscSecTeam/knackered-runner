#DataAccess.py

#This class serves to connect to the MySQL database.

import mysql.connector
from mysql.connector import errorcode
from collections import OrderedDict
from Team import Team


#Configure database connection here
#_____________________________  #
DATABASE_USERNAME = "root"      #
DATABASE_PASSWORD = ""          #
DATABASE_ADDRESS = "localhost"  #
DATABASE_NAME = "scoring"       #
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  #

DATABASE_SCHEMA = OrderedDict()  # Order of table creation is important
                                 # Foreign keys will not function correctly unless tables are created in this order

DATABASE_SCHEMA['TEAMS'] = """
    CREATE TABLE teams (
      id INT PRIMARY KEY
    )
"""

#TYPE field denormalized for simplicity. (Could make serviceType table if desired.)
DATABASE_SCHEMA['SERVICES'] = """
    CREATE TABLE services (
      id INT PRIMARY KEY  AUTO_INCREMENT,
      teamId INT,
      address VARCHAR(50),
      type VARCHAR(5),
      FOREIGN KEY (teamId) REFERENCES teams(id)
    )
"""

DATABASE_SCHEMA['TEAMLOGINS'] = """
    CREATE TABLE teamlogins (
      id INT PRIMARY KEY AUTO_INCREMENT,
      teamId INT,
      username varchar(100),
      password varchar(100),
      FOREIGN KEY (teamId) REFERENCES teams(id)
    )
"""

DATABASE_SCHEMA['CHECKS'] = """
    CREATE TABLE checks (
      id INT PRIMARY KEY AUTO_INCREMENT,
      serviceId INT,
      round INT,
      result INT,
      FOREIGN KEY (serviceId) REFERENCES services(id)
    )
"""

DATABASE_SCHEMA['SERVICELOGINS'] = """
    CREATE TABLE servicelogins (
      id INT PRIMARY KEY AUTO_INCREMENT,
      serviceId INT,
      username varchar(100),
      password varchar(100),
      FOREIGN KEY (serviceId) REFERENCES services(id)
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
                                                  host=self.address)
        self.cursor = self.connection.cursor()

        #connect to the database
        #create the DB if it does not exist
        self.establishConnection()

    #Connects to DB and returns list of teams
    def getTeams(self):
        teamsList = []

        #ENSURE we're using the right database
        self.cursor.execute("USE " + self.dbname + ";")

        #Get teams and create teamslist entries
        self.cursor.execute("SELECT * FROM teams;")
        for (id) in self.cursor:
            teamsList.append(Team(int(id[0])))

        #we have the teams! Let's fill them with services.
        self.cursor.execute("SELECT * FROM services LEFT JOIN servicelogins ON services.id = servicelogins.serviceId")
        for (id, teamId, address, type, loginId, serviceId, username, password) in self.cursor:

            #Does the team have a login?
            if username is None:
                teamsList[teamId - 1].addService(id, type, address, "default9001", "default9001")
            else:
                teamsList[teamId - 1].addService(id, type, address, username, password)

        return teamsList

    #Connects to DB and inserts a round's check results
    def addCheckRound(self, teams, checkRound):

        #ENSURE we're using the right database
        self.cursor.execute("USE " + self.dbname + ";")

        query = "INSERT INTO checks (serviceId,round,result) VALUES"  # To be continued!

        #Loop through services and prepare query for insertion
        for team in teams:
            for service in team.getServices():
                addition = ' (' + str(service.getId()) + "," + str(checkRound) + "," + str(service.getCheck()) + '),'
                query += addition

        query = query[:-1] + ";"
        print query
        self.cursor.execute(query)
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    #connect to the database
    def establishConnection(self):
        try:
            self.connection.database = self.dbname
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.createDB()
                print "Created database."
                self.connection.database = self.dbname
            else:
                #if the connection is broken, rage-quit the program
                print """
                    Can't connect to the MySQL Database.
                    Ensure service is started on appropriate host. (service mysql start)
                    Ensure database user info is correct. (edit DataAccess.py)
                    Ensure connection is not being blocked by a firewall. MySQL uses port 3306 by default.
                """
                print(err)
                exit(1)

    #create the database
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

    def createTables(self):
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