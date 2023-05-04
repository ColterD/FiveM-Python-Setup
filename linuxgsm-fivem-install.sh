#!/bin/bash

set -e

function main() {
  check_sudo_privileges
  install_unattended_upgrades
  update_os_and_packages
  install_web_server
  install_required_packages
  secure_mariadb_installation
  configure_fail2ban
  create_fivem_user_and_set_sudo_privileges
  clone_linuxgsm_repository
  download_and_install_fivem
  configure_fivem
  display_database_and_fivem_user_passwords
}

function check_sudo_privileges() {
  if [[ $EUID -ne 0 ]]; then
     echo "This script must be run as sudo." 
     exit 1
  fi
}

function install_unattended_upgrades() {
  apt-get update
  apt-get install -y unattended-upgrades
}

function update_os_and_packages() {
  apt-get update
  apt-get -y upgrade
}

function install_web_server() {
  echo "Please select a web server to install:"
  echo "1. Apache"
  echo "2. Nginx"
  echo "3. Quit"

  read -p "Enter your choice [1-3]: " choice

  case $choice in
      1)
          apt-get update && apt-get install -y apache2
          systemctl enable apache2 && systemctl start apache2
          ;;
      2)
          apt-get update && apt-get install -y nginx
          systemctl enable nginx && systemctl start nginx
          ;;
      3)
          echo "Exiting script."
          exit 0
          ;;
      *)
          echo "Invalid input. You must choose 1 for Apache, 2 for Nginx, or 3 to quit."
          ;;
  esac
}

function install_required_packages() {
  apt-get install -y mariadb-server php php-fpm php-mysql phpmyadmin fail2ban screen nano unzip git
}

function secure_mariadb_installation() {
  mysql_secure_installation
}

function configure_fail2ban() {
  # Configure SSH Jail
  echo "[sshd]" >> /etc/fail2ban/jail.local
  echo "enabled = true" >> /etc/fail2ban/jail.local
  echo "port = ssh" >> /etc/fail2ban/jail.local
  echo "filter = sshd" >> /etc/fail2ban/jail.local
  echo "logpath = /var/log/auth.log" >> /etc/fail2ban/jail.local
  echo "maxretry = 3" >> /etc/fail2ban/jail.local

  # Configure FTP Jail
  echo "[vsftpd]" >> /etc/fail2ban/jail.local
  echo "enabled = true" >> /etc/fail2ban/jail.local
  echo "port = ftp,ftp-data,ftps,ftps-data" >> /etc/fail2ban/jail.local
  echo "filter = vsftpd" >> /etc/fail2ban/jail.local
  echo "logpath = /var/log/vsftpd.log" >> /etc/fail2ban/jail.local
  echo "maxretry = 3" >> /etc/fail2ban/jail.local

  # Configure FiveM Jail
  echo "[fivem]" >> /etc/fail2ban/jail.local
  echo "enabled = true" >> /etc/fail2ban/jail.local
  echo "port = 30120" >> /etc/fail2ban/jail.local
  echo "filter = fivem" >> /etc/fail2ban/jail.local
  echo "logpath = /home/fivem/server/server.log" >> /etc/fail2ban/jail.local
  echo "maxretry = 3" >> /etc/fail2ban/jail.local
}

function create_fivem_user_and_set_sudo_privileges() {
  read -p "Enter password for the new 'fivem' user: " fivem_password
  useradd -m -p $(openssl passwd -1 $fivem_password) fivem
  usermod -aG sudo fivem
}

function clone_linuxgsm_repository() {
  sudo -i -u fivem bash << EOF
  cd ~
  git clone https://github.com/GameServerManagers/LinuxGSM.git linuxgsm
  cd linuxgsm
  ./linuxgsm.sh fivem
EOF
}

function download_and_install_fivem() {
  sudo -i -u fivem bash << EOF
  cd ~
  mkdir -p fivemserver
  cd fivemserver
  wget $(curl -s https://runtime.fivem.net/artifacts/fivem/build_proot_linux/master/ | grep -o -m1 'https://[^"]*' | grep -m1 'fx\.tar\.xz')
  tar xf fx.tar.xz
  rm fx.tar.xz
EOF
}

function configure_fivem() {
  echo "Configuring FiveM server..."
  read -p "Enter server name: " server_name
  read -p "Enter server port (default 30120): " server_port
  server_port=${server_port:-30120}

  # Prompt for server license key
  echo "You can obtain a server license key by signing up for a FiveM license at https://fivem.net"
  read -p "Enter server license key: " license_key

  # Prompt for server tags
  echo "Server tags are used by the FiveM server browser to categorize servers. Separate tags with a comma (,)."
  read -p "Enter server tags: " server_tags

  # Prompt for maximum players allowed
  echo "Without subscribing to FiveM's patreon, the highest you can go is 32 players."
  read -p "Enter server max players (default 32): " max_players
  max_players=${max_players:-32}

  # Prompt for ESX Framework
  read -p "Do you want to enable the ESX Framework mod? (y/n): " enable_esx

  # Prompt to enable txAdmin
  read -p "Enable txAdmin FiveM mod? (y/n): " enable_txadmin

  # Create server.cfg file
  echo "Creating server.cfg file..."
  cat > server.cfg <<EOF
# This is the main configuration file for the FiveM server.

# Server name
sv_hostname "${server_name}"

# Server IP address and port to listen on
endpoint_add_tcp "0.0.0.0:${server_port}"
endpoint_add_udp "0.0.0.0:${server_port}"

# License key for server authentication
sv_licenseKey "${license_key}"

# Server tags used by the FiveM server browser
sets tags "${server_tags}"

# Maximum number of players allowed on the server
sv_maxclients ${max_players}
EOF

  if [ "${enable_esx}" = "y" ]; then
    # Add ESX Framework configuration to server.cfg
    cat >> server.cfg <<EOF

# ESX Framework configuration
set es_enableCustomData 1
set mysql_connection_string "server=localhost;database=es_extended;userid=root;password="
EOF

# Enable txAdmin FiveM mod
exec resources/[admin]/start_txadmin.cfg

EOF
  fi

  echo "Server configured successfully."
  echo "If you want to edit these values later, you can find the server.cfg file in the fivemserver directory."
}
