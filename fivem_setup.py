import os
import random
import string
import subprocess
import logging

config = {
    'mariadb': {
        'root_password': '',
        'db_name': 'fivem',
        'db_user': 'fivem',
        'db_user_password': ''
    },
    'fivem': {
        'server_name': '',
        'server_description': '',
        'game_mode': 'roleplay',
        'port': '30120',
        'max_players': '32',
        'license_key': ''
    }
}

def install_packages(packages):
    """Install required packages"""
    logging.info("Installing required packages...")
    subprocess.run(["apt-get", "update"])
    subprocess.run(["apt-get", "install", "-y"] + packages, check=True)
    logging.info("Packages installed successfully.")

def configure_mariadb():
    """Configure MariaDB"""
    logging.info("Configuring MariaDB...")
    config['mariadb']['root_password'] = generate_password()
    print(f"Generated MariaDB root password: {config['mariadb']['root_password']}")
    db_root_password = get_password_input("Enter the password for the MariaDB root user: ")
    db_root_password_confirm = get_password_input("Enter the password again: ")
    if db_root_password != db_root_password_confirm:
        print("Passwords do not match. Please try again.")
        configure_mariadb()
        return
    try:
        subprocess.run(["mysqladmin", "-u", "root", "-p" + db_root_password, "password", config['mariadb']['root_password']], check=True)
        subprocess.run(["mysql", "-u", "root", f"-p{config['mariadb']['root_password']}", "-e", f"CREATE DATABASE {config['mariadb']['db_name']}"], check=True)
        subprocess.run(["mysql", "-u", "root", f"-p{config['mariadb']['root_password']}", "-e", f"CREATE USER '{config['mariadb']['db_user']}'@'localhost' IDENTIFIED BY '{config['mariadb']['db_user_password']}'"], check=True)
        subprocess.run(["mysql", "-u", "root", f"-p{config['mariadb']['root_password']}", "-e", f"GRANT ALL PRIVILEGES ON {config['mariadb']['db_name']}.* TO '{config['mariadb']['db_user']}'@'localhost'"], check=True)
        logging.info("MariaDB configured successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to configure MariaDB. Please check your input and try again.")
        logging.error(f"Failed to configure MariaDB: {e}")
        configure_mariadb()

def configure_web_server():
    """Configure the web server"""
    logging.info("Configuring the web server...")
    try:
        subprocess.run(["a2enmod", "rewrite"], check=True)
        subprocess.run(["systemctl", "restart", "apache2"], check=True)
        logging.info("Web server configured successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to configure the web server. Please check your input and try again.")
        logging.error(f"Failed to configure the web server: {e}")
        configure_web_server()

def configure_fivem():
    """Configure the FiveM server"""
    logging.info("Configuring the FiveM server...")
    config['fivem']['server_name'] = input("Enter the server name: ")
    config['fivem']['server_description'] = input("Enter the server description: ")
    config['fivem']['game_mode'] = input("Enter the game mode (default: roleplay): ") or "roleplay"
    config['fivem']['port'] = input("Enter the server port (default: 30120): ") or "30120"
    config['fivem']['max_players'] = input("Enter the maximum number of players (default: 32): ") or "32"
    config['fivem']['license_key'] = input("Enter the FiveM license key: ")
    # Validate the FiveM license key
    if config['fivem']['license_key']:
        response = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", f"https://keymaster.fivem.net/api/validate/{config['fivem']['license_key']}"], capture_output=True)
        if response.returncode != 0:
            print("Failed to validate the FiveM license key. Please check your input and try again.")
            config['fivem']['license_key'] = ''
    # Replace placeholders in the default configuration files with user input
    with open("/home/fivem/server-data/server.cfg", "r+") as f:
        content = f.read()
        # Do something with the file contents
    try:
        subprocess.run(["/home/fivem/run.sh", "+exec", "server.cfg"], check=True)
        logging.info("FiveM server started successfully.")
        print("\nFiveM server started successfully.")
        print(f"Server name: {config['fivem']['server_name']}")
        print(f"Server description: {config['fivem']['server_description']}")
        print(f"Game mode: {config['fivem']['game_mode']}")
        print(f"Server port: {config['fivem']['port']}")
        print(f"Maximum players: {config['fivem']['max_players']}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start the FiveM server. Error message: {e}")
        logging.error(f"Failed to start the FiveM server: {e}")
        configure_fivem()

def generate_password(length=16):
    """Generate a random password"""
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def get_password_input(prompt):
    """Prompt the user for a password"""
    password = ''
    while not password:
        password = input(prompt)
        if not password:
            print("Password cannot be empty. Please try again.")
    return password

if __name__ == "__main__":
    logging.basicConfig(filename="fivem_setup.log", level=logging.INFO)
    packages = ["apache2", "mysql-server", "curl"]
    install_packages(packages)
    print()
    configure_mariadb()
    print()
    configure_web_server()
    print()
    configure_fivem()

print("\033[32m\nFiveM server configuration complete!\033[0m")
