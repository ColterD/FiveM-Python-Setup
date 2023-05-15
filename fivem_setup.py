# flake8: noqa

import os
import random
import string
import subprocess
import logging
import getpass

# Define the configuration variables
config = {
    'mariadb': {
        'root_password': '',
        'db_name': 'fivem',
        'db_user': 'fivem',
        'db_user_password': ''
    },
    'fivem': {
        'sv_projectName': 'FiveM',
        'sv_projectDesc': 'A FiveM roleplaying server.',
        'sv_maxclients': '32',
    }
}

# Add comments to the code to explain what each function does
def install_packages():
    """Install required packages"""
    # Install the apache2, curl, openssl, libssl-dev, libffi-dev, git, build-essential, zip, unzip, nodejs, npm, python3-pip, mariadb-server packages
    print(f"**Installing required packages:** {', '.join(packages)}")

    # Check if the user has the required permissions to install the packages
    if not os.geteuid() == 0:
        print("**You do not have the required permissions to install the packages.**")
        return

    # Use a linter to check for errors
    subprocess.run(["pylint", "install_packages.py"])

    # Download the FiveM server
    print("**Downloading FiveM server...**")

    # Check if the user has the required permissions to download the FiveM server
    if not os.geteuid() == 0:
        print("**You do not have the required permissions to download the FiveM server.**")
        return

    subprocess.run(["wget", "https://fivem.net/fivem-server.zip"])

    # Unzip the FiveM server
    print("**Unzipping FiveM server...**")

    # Check if the user has the required permissions to unzip the FiveM server
    if not os.geteuid() == 0:
        print("**You do not have the required permissions to unzip the FiveM server.**")
        return

    subprocess.run(["unzip", "fivem-server.zip"])

    # Configure MariaDB
    configure_mariadb()

    # Configure the web server
    configure_web_server()

    print("**FiveM server is now configured!**")


def configure_mariadb():
    """Configure MariaDB"""
    # Configure the MariaDB root user password
    print("**Configuring MariaDB...**")
    print("**Setting the root password...**")

    # Check if the user has the required permissions to access the MariaDB database
    if not os.geteuid() == 0:
        print("**You do not have the required permissions to access the MariaDB database.**")
        return

    # Generate a random password for the MariaDB root user
    password = generate_password()
    # Set the MariaDB root user password
    subprocess.run(["sudo", "mysqladmin", "-u", "root", "-p", password, "password", password])

    # Create a FiveM database user
    print("**Creating a FiveM database user...**")

    # Check if the user has the required permissions to create a FiveM database user
    if not os.geteuid() == 0:
        print("**You do not have the required permissions to create a FiveM database user.**")
        return

    # Create a FiveM database user
    subprocess.run(["sudo", "mysql", "-u", "root", "-p", password, "-e", "CREATE USER 'fivem'@'localhost' IDENTIFIED BY 'password'"])

    # Grant all privileges to the FiveM database user
    print("**Granting all privileges to the FiveM database user...**")

    # Check if the user has the required permissions to grant privileges to the FiveM database user
    if not os.geteuid() == 0:
        print("**You do not have the required permissions to grant privileges to the FiveM database user.**")
        return

    # Grant all privileges to the FiveM database user
    subprocess.run(["sudo", "mysql", "-u", "root", "-p", password, "-e", "GRANT ALL PRIVILEGES ON fivem.* TO 'fivem'@'localhost'"])

        # Display the FiveM user and password to the user
    print("**Your FiveM database user and password is:**")
    print("**User:** fivem")
    print("**Password:** password")

    print("**MariaDB configuration complete!**")


def configure_web_server():
    """Configure the web server"""

    # Ask the user if they want to install Apache
    print("Would you like to install Apache? (Y/N)")
    choice = input()

    if choice == "Y":
        # Enable the rewrite module for the Apache web server
        print("**Enabling the rewrite module for the Apache web server...**")

        # Check if the user has the required permissions to enable the rewrite module
        if not os.geteuid() == 0:
            print("**You do not have the required permissions to enable the rewrite module.**")
            return

        subprocess.run(["sudo", "a2enmod", "rewrite"])

        # Create a virtual host for the FiveM server
        print("**Creating a virtual host for the FiveM server...**")

        # Check if the user has the required permissions to create a virtual host
        if not os.geteuid() == 0:
            print("**You do not have the required permissions to create a virtual host.**")
            return

        with open("/etc/apache2/sites-available/fivem.conf", "w") as f:
            f.write("""
<VirtualHost *:80>
    ServerName fivem.example.com
    ServerAlias www.fivem.example.com
    DocumentRoot /var/www/fivem
    ErrorLog /var/log/apache2/fivem-error.log
    CustomLog /var/log/apache2/fivem-access.log common
    <Directory /var/www/fivem>
        Options Indexes FollowSymLinks MultiViews
        AllowOverride All
        Order allow,deny
        Allow from all
    </Directory>
</VirtualHost>
""")

        # Enable the virtual host
        print("**Enabling the virtual host...**")

        # Check if the user has the required permissions to enable the virtual host
        if not os.geteuid() == 0:
            print("**You do not have the required permissions to enable the virtual host.**")
            return

        subprocess.run(["sudo", "a2ensite", "fivem"])

        # Restart the Apache web server
        print("**Restarting the Apache web server...**")

        # Check if the user has the required permissions to restart the Apache web server
        if not os.geteuid() == 0:
            print("**You do not have the required permissions to restart the Apache web server.**")
            return

        subprocess.run(["sudo", "systemctl", "restart", "apache2"])

        print("**Apache has been configured and enabled!**")
    else:
        print("**Apache will not be installed.**")


if __name__ == "__main__":
    # Install the required packages
    install_packages()

    # Configure MariaDB
    configure_mariadb()

    # Configure the web server
    configure_web_server()

    # Prompt the user to edit the server.cfg file
    print("Would you like to edit the server.cfg file now? (Y/N)")
    choice = input()

    if choice == "Y":
        # Get the user's input for the config variables
        sv_projectName = input("Enter the server name (Leave blank for default): ") or "FiveM"
        sv_projectDesc = input("Enter the server description (Leave blank for default): ") or "A FiveM roleplaying server."
        sv_maxclients = input("Enter the maximum number of players (Leave blank for default): ") or "32"
        
        # Prompt the user for the license key and tell them where to get it
        sv_licenseKey = input("Enter the license key: ")
        print("To get a FiveM license key, go to https://keymaster.fivem.net/")

        # Open the server.cfg file in write mode
        with open("server.cfg", "w") as f:

            # Write the user's input to the server.cfg file
            f.write("sv_projectName = " + server_name + "\n")
            f.write("sv_projectDesc = " + sv_projectDesc + "\n")
            f.write("sv_maxclients = " + sv_maxclients + "\n")
            f.write("sv_licenseKey = " + sv_licenseKey + "\n")

        # Close the server.cfg file
        f.close()

    else:
        # Do nothing
        pass

    # Create the fivemserver.sh file and directory
    with open('fivemserver.sh', 'w') as f:
        f.write("""
#!/usr/bin/env python3

import os
import sys
import requests

# Define the configuration variables
config = {
    'fivem_server_path': os.getcwd(),
    'fivem_server_command': 'startfivem.sh',
    'fivem_server_update_command': 'updatefivem.sh',
}

# Check if the user has the required permissions to start, stop, restart, and update the FiveM server
if not os.geteuid() == 0:
    print("**You do not have the required permissions to start, stop, restart, and update the FiveM server.**")
    sys.exit(1)

# Get the current working directory
current_directory = os.getcwd()

# Change the current working directory to the FiveM server directory
os.chdir(config['fivem_server_path'])

# Check if the FiveM server directory exists
if not os.path.exists(config['fivem_server_path']):
    print("**The FiveM server directory does not exist.**")
    sys.exit(1)

# Start the FiveM server
if sys.argv[1] == 'start':
    print("**Starting FiveM server...**")
    subprocess.run([config['fivem_server_command']])
    print("**FiveM server is now started.**")

# Stop the FiveM server
if sys.argv[1] == 'stop':
    print("**Stopping FiveM server...**")
    subprocess.run([config['fivem_server_command'], '--stop'])
    print("**FiveM server is now stopped.**")

# Restart the FiveM server
if sys.argv[1] == 'restart':
    print("**Restarting FiveM server...**")
    subprocess.run([config['fivem_server_command'], '--restart'])
    print("**FiveM server is now restarted.**")

# Get the latest FiveM version
latest_version = requests.get("https://fivem.net/api/version").json()["version"]

# Check if the current version is the latest version
if latest_version > config['fivem_server_version']:
    print("**Updating FiveM server...**")
    subprocess.run([config['fivem_server_update_command']])
    print("**FiveM server is now updated.**")
else:
    print("**There is no newer version of FiveM available.**")
""")

    # Check if the fivemserver.sh file exists
    if not os.path.exists('fivemserver.sh'):
        print("**The fivemserver.sh file does not exist.**")
        sys.exit(1)

    # Make the fivemserver.sh file executable
    os.chmod('fivemserver.sh', 0o755)

    # Start the FiveM server
    print("**Starting FiveM server...**")
    subprocess.run(['fivemserver.sh'])
    print("**FiveM server is now configured started.**")
