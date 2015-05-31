# Backend configuration options are stored here

from collections import OrderedDict


class Conf:
    def __init__(self):
        self.WEB_ROOT = "/var/www/html/"
        self.PLUGIN_DIRECTORY = "/usr/lib/nagios/plugins/"

        self.DATABASE_USERNAME = "root"
        self.DATABASE_PASSWORD = ""
        self.DATABASE_ADDRESS = "localhost"
        self.DATABASE_NAME = "scoring"

        # You shouldn't need to modify the schema for production use.
        self.DATABASE_SCHEMA = OrderedDict()  # Order of table creation is important. Foreign keys will break!
        self.DATABASE_SCHEMA['TEAMS'] = """
            CREATE TABLE teams (
                id INT PRIMARY KEY
            )
        """
        # TYPE field de-normalized for simplicity. (Could make serviceType table if desired.)
        self.DATABASE_SCHEMA['SERVICES'] = """
            CREATE TABLE services (
                id INT PRIMARY KEY  AUTO_INCREMENT,
                teamId INT,
                address VARCHAR(50),
                type VARCHAR(5),
                FOREIGN KEY (teamId) REFERENCES teams(id)
            )
        """
        self.DATABASE_SCHEMA['TEAMLOGINS'] = """
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
        self.DATABASE_SCHEMA['CHECKS'] = """
            CREATE TABLE checks (
                id INT PRIMARY KEY AUTO_INCREMENT,
                serviceId INT,
                round INT,
                result INT,
                FOREIGN KEY (serviceId) REFERENCES services(id)
            )
        """
        self.DATABASE_SCHEMA['SERVICELOGINS'] = """
            CREATE TABLE servicelogins (
                id INT PRIMARY KEY AUTO_INCREMENT,
                serviceId INT,
                username varchar(100),
                password varchar(100),
                FOREIGN KEY (serviceId) REFERENCES services(id)
            )
        """