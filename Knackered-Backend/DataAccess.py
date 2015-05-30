# This class serves to connect to the MySQL database.

import mysql.connector
from mysql.connector import errorcode
from Team import Team
from Conf import Conf


class DataAccess():

    def __init__(self):
        # Store configured settings
        self.config = Conf()

        # init database connection using settings above
        self.connection = mysql.connector.connect(user=self.config.DATABASE_USERNAME,
                                                  password= self.config.DATABASE_PASSWORD,
                                                  host=self.config.DATABASE_ADDRESS)
        self.cursor = self.connection.cursor()

        # connect to the database
        # create the DB if it does not exist
        self.establish_connection()

    # Connects to DB and returns list of teams
    def get_teams(self):
        teams_list = []

        # ensure we're using the right database
        self.cursor.execute("USE " + self.config.DATABASE_NAME + ";")

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
        self.cursor.execute("USE " + self.config.DATABASE_NAME + ";")

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
            self.connection.database = self.config.DATABASE_NAME
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_db()
                print "Created database."
                self.connection.database = self.config.DATABASE_NAME
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
            self.cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.config.DATABASE_NAME))
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
        for table_name, table in self.config.DATABASE_SCHEMA.items():
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
        self.cursor.execute("USE " + self.config.DATABASE_NAME + ";")

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
