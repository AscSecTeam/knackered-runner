
CREATE DATABASE scoring;

USE scoring;

CREATE TABLE teams (
    id INT PRIMARY KEY
);
  
CREATE TABLE services (
    id INT PRIMARY KEY AUTO_INCREMENT,
    teamId INT,
    address VARCHAR(50),
    type VARCHAR(5),
    FOREIGN KEY (teamId) REFERENCES teams(id)
);
    

CREATE TABLE teamlogins (
    teamId INT,
    user_id int(11) NOT NULL AUTO_INCREMENT,
    user_name varchar(64) COLLATE utf8_unicode_ci NOT NULL,
    user_password_hash varchar(255) COLLATE utf8_unicode_ci NOT NULL,
    PRIMARY KEY (user_id),
    UNIQUE KEY user_name (user_name),
    FOREIGN KEY (teamId) REFERENCES teams(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='user data';

CREATE TABLE checks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    serviceId INT,
    round INT,
    result INT,
    FOREIGN KEY (serviceId) REFERENCES services(id)
);

CREATE TABLE servicelogins (
    id INT PRIMARY KEY AUTO_INCREMENT,
    serviceId INT,
    username varchar(100),
    password varchar(100),
    FOREIGN KEY (serviceId) REFERENCES services(id)
);

INSERT INTO teams(id) VALUES (0),(1);

INSERT INTO teamlogins (teamId, user_name, user_password_hash) VALUES (0,'default','$2y$10$8pggvF7cqtrrmEM4rl8c0.joU3vcQBiN1vdZ2ILzQ8sBhIqjPd682');

INSERT INTO services (id, teamId, address, type) VALUES
  (21, 1, '10.10.10.10', 'http'),
  (22, 1, 'google.com', 'http'),
  (23, 1, '10.10.10.10', 'https'),
  (24, 1, 'google.com', 'https'),
  (25, 1, '10.10.10.10', 'ftp'),
  (26, 1, 'ftp.swfwmd.state.fl.us', 'ftp'),
  (27, 1, '10.10.10.10', 'ssh'),
  (28, 1, 'jeffandolora.com', 'ssh'),
  (29, 1, '10.10.10.10', 'icmp'),
  (30, 1, 'google.com', 'icmp'),
  (31, 1, '10.10.10.10', 'smtp'),
  (32, 1, 'test.smtp.org', 'smtp'),
  (33, 1, '10.10.10.10', 'dns'),
  (34, 1, '8.8.8.8', 'dns');