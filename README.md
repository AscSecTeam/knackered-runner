Knackered
================
The Knackered Engine is a security competition scoring engine.

Designed with quick setup in mind, all that is needed is a linux server with LAMP and Python. Tested primarily on Ubuntu 12.04 but should run on just about anything.

Knackered's backend uses checks from the nagios-plugins package. (sudo apt-get install nagios-plugins)

The system is also designed to be easily modifiable. All checks are made from Runner.py, calling scripts in the nagios-plugins directory. 


Installation and Setup
============
Ensure MySQL 5+, Apache2, PHP 5.3+, and nagios-plugins are installed (and, if necessary, running)

Configure the database information at the top of Knackered-Backend/DataAccess.py, and in the web interface's config/db.php file.

If nagios-plugins aren't in /usr/lib/nagios/plugins/, specify the directory at the top of Knackered-Backend/Runner.py

If your webroot isn't /var/www/html/, configure that in Knackered-Backend/Main.py.

scoring.sql contains the necessary MySQL database along with a test team.

From there, use the web interface to configure Knackered-Backend for your competition.


Checks
=============
The HTTP and HTTPS checks get the page and look for an expected string.

The DNS check queries the specified server for an expected result.

The FTP check does a banner-grab and looks for an expected string. In the future, this should probably modified to actually login and upload/download.

The SSH check returns the SSH server version. In the future, this should probably be modified to actually login and cat a file.

The ICMP check is pretty self explanatory. It pings the server.

The SMTP check establishes a connection, does a HELO and a QUIT. In the future, this should probably be modified to actually login and send mail.


Credits
============
Nagios-Plugins

A modified version of Panique's minimal php-login project: https://github.com/panique/php-login-minimal

Griffith Chaffee's cyberengine used at ISTS competitions https://github.com/RITSPARSA/cyberengine
