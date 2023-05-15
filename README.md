# FiveM Server Setup

This repository contains a Python script that can be used to setup and configure a FiveM server.

## Requirements

* A Linux machine (tested on Ubuntu 20.04)
* Python 3.9 or higher

## Installation

1. Clone the repository to your computer.
2. Open the `config.py` file in a text editor.
3. Edit the configuration variables to match your settings.
4. Run the `config.py` file.

## Usage

Once the configuration is complete, you will be able to start a FiveM server.

`python3 /path/to/config.py`

## Configuration Variables

The following configuration variables can be edited in the `config.py` file:

* `mariadb_root_password`: The password for the MariaDB root user.
* `db_name`: The name of the FiveM database.
* `db_user`: The name of the FiveM database user.
* `db_user_password`: The password for the FiveM database user.
* `server_name`: The name of the FiveM server.
* `server_description`: The description of the FiveM server.
* `game_mode`: The game mode of the FiveM server.
* `port`: The port of the FiveM server.
* `max_players`: The maximum number of players on the FiveM server.
* `license_key`: The license key for the FiveM server.

## Troubleshooting

If you have any problems with the configuration, please open an issue on the GitHub repository.
