# This class serves to connect to the MySQL database.

import mysql.connector
from mysql.connector import errorcode
from collections import OrderedDict
from Team import Team

# Configure database connection here
DATABASE_USERNAME = "root"
DATABASE_PASSWORD = ""
DATABASE_ADDRESS = "localhost"
DATABASE_NAME = "scoring"

DATABASE_SCHEMA = OrderedDict()  # Order of table creation is important
# Foreign keys will not function correctly unless tables are created in this order

DATABASE_SCHEMA['TEAMS'] = """
    CREATE TABLE teams (
        id INT PRIMARY KEY
    )
"""

# TYPE field de-normalized for simplicity. (Could make serviceType table if desired.)
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
        teamId INT,
        user_id int(11) NOT NULL AUTO_INCREMENT,
        user_name varchar(64) COLLATE utf8_unicode_ci NOT NULL,
        user_password_hash varchar(255) COLLATE utf8_unicode_ci NOT NULL,
        PRIMARY KEY (user_id),
        UNIQUE KEY user_name (user_name),
        FOREIGN KEY (teamId) REFERENCES teams(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='user data';
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
        # Store configured settings
        self.username = DATABASE_USERNAME
        self.password = DATABASE_PASSWORD
        self.address = DATABASE_ADDRESS
        self.dbname = DATABASE_NAME
        self.schema = DATABASE_SCHEMA

        # init database connection using settings above
        self.connection = mysql.connector.connect(user=self.username,
                                                  password=self.password,
                                                  host=self.address)
        self.cursor = self.connection.cursor()

        # connect to the database
        # create the DB if it does not exist
        self.establish_connection()

    # Connects to DB and returns list of teams
    def get_teams(self):
        teams_list = []

        # ensure we're using the right database
        self.cursor.execute("USE " + self.dbname + ";")

        # Get teams and create teamslist entries
        self.cursor.execute("SELECT * FROM teams;")
        for team_id in self.cursor:
            teams_list.append(Team(int(team_id[0])))

        # we have the teams! Let's fill them with services.
        self.cursor.execute("SELECT * FROM services LEFT JOIN servicelogins ON services.id = servicelogins.serviceId")
        for (service_id, team_id, address, service_type, loginId, serviceId, username, password) in self.cursor:

            # find the right team to insert into
            for team in teams_list:
                if team.id == team_id:

                    # Does the team have a login?
                    if username is None:
                        team.addService(service_id, service_type, address, "default9001", "default9001")
                    else:
                        team.addService(service_id, service_type, address, username, password)

        return teams_list

    # Connects to DB and inserts a round's check results
    def add_check_round(self, teams, check_round):

        # ensure we're using the right database
        self.cursor.execute("USE " + self.dbname + ";")

        query = "INSERT INTO checks (serviceId,round,result) VALUES"  # To be continued!

        query_addition = ""
        # Loop through services and prepare query for insertion
        for team in teams:
            for service in team.services:
                query_addition += ' (' + str(service.getId()) + "," + str(check_round) + "," + str(service.result) + '),'

        # If there's no teams, an invalid query will be generated
        if query_addition != "":
            query += query_addition
            query = query[:-1] + ";"
            print query
            self.cursor.execute(query)
            self.connection.commit()

    # connect to the database
    def establish_connection(self):
        try:
            self.connection.database = self.dbname
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_db()
                print "Created database."
                self.connection.database = self.dbname
            else:
                # if the connection is broken, rage-quit the program
                print """
                    Can't connect to the MySQL Database.
                    Ensure service is started on appropriate host. (service mysql start)
                    Ensure database user info is correct. (edit DataAccess.py)
                    Ensure connection is not being blocked by a firewall. MySQL uses port 3306 by default.
                """
                print(err)
                exit(1)

    # create the database
    def create_db(self):
        try:
            self.cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.dbname))
            self.connection.commit()

        except mysql.connector.Error as err:
            # if the connection is broken, rage-quit the program
            print """
                Can't connect to the MySQL Database.
                Ensure service is started. (service mysql start)
                Ensure database user info is correct (EDIT DataAccess.py)
            """
            print("Failed creating database: {}".format(err))
            exit(1)

    def create_tables(self):
        for table_name, table in self.schema.items():
            try:
                self.cursor.execute(table)
                self.connection.commit()
                print "Created table " + table_name
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print "Table " + table_name + " already exists, woohoo"
                else:
                    print err.msg

    def get_scores(self):
        teams = []

        # ensure we're using the right database
        self.cursor.execute("USE " + self.dbname + ";")

        # Execute query
        query = """SELECT services.teamId, checks.serviceId, COUNT(checks.id)
                   FROM checks INNER JOIN services ON checks.serviceId = services.id
                   WHERE result = 1 GROUP BY serviceId;"""
        self.cursor.execute(query)

        for (team_id, service_id, count) in self.cursor:
            team_exists = False
            for team in teams:
                if team.id == team_id:
                    team.add_to_score(count)
                    team_exists = True

            if not team_exists:
                new_team = Team(team_id)
                new_team.add_to_score(count)
                teams.append(new_team)

        self.cursor.close()
        self.connection.close()

        return teams
