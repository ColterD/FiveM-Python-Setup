# FiveM Server Setup Script

This script will install the required packages, configure MariaDB, configure the web server, and prompt the user to edit the server.cfg file. Finally, the script creates a fivemserver.sh file that can be used to start, stop, restart, and update the FiveM server.

If there isn't a Release listed, then this is completely unstable.

## Prerequisites

* Ubuntu 20.04
* At least 4GB of RAM
* At least 5GB hard drive space

## Installation

1. Clone the repository:

```
git clone https://github.com/ColterD/FiveM-Python-Setup.git
```

2. Change to the directory:

```
cd FiveM-Python-Setup
```

3. Install the required packages:

```
pip3 install -r requirements.txt
```

4. Run the command:

```
python3 fivem_setup.py
```

## Server Management

1. Run the following command to start the FiveM server:

```
./fivemserver.sh start
```

2. Run the following command to stop the FiveM server:

```
./fivemserver.sh stop
```

3. Run the following command to restart the FiveM server:

```
./fivemserver.sh restart
```

4. Run the following command to update the FiveM server:

```
./fivemserver.sh update
```

## Configuration

The FiveM server can be configured by editing the server.cfg file. The server.cfg file is located in the FiveM-Python-Setup directory.

## License

This project is licensed under the Creative Commons Attribution-Share Alike 4.0 International (CC BY-SA 4.0) License.
