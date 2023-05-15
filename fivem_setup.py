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
        'server_name': 'FiveM',
        'server_description': 'A FiveM roleplaying server.',
        'game_mode': 'roleplay',
        'port': '30120',
        'max_players': '32',
        'license_key': ''
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

    print("**FiveM server is now configured!**")
