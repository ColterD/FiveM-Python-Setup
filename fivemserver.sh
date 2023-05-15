#!/usr/bin/env python3

import os
import sys

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

# Update the FiveM server
if sys.argv[1] == 'update':
    print("**Updating FiveM server...**")
    subprocess.run([config['fivem_server_update_command']])
    print("**FiveM server is now updated.**")

