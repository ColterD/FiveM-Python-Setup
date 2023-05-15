# FiveM Server Setup Script

This script will help you set up a FiveM server on Ubuntu 20.04. It will install the required packages, configure MariaDB, and configure the web server.

## Prerequisites

* A computer with at least 4GB of RAM
* A 64-bit operating system
* A 5GB hard drive space

## Instructions

1. Clone this repository to your computer.
2. Open a terminal window and navigate to the directory where you cloned the repository.
3. Run the following commands to install the required packages:

```
sudo apt-get install python3-pip
```

4. Run the following command:

```
python3 fivem_setup.py
```

5. To start the FiveM server, run the following command:

```
python3 start_fivem_server.py
```

6. To stop the FiveM server, run the following command:

```
python3 stop_fivem_server.py
```

7. To restart the FiveM server, run the following command:

```
python3 restart_fivem_server.py
```

8. To update the FiveM server, run the following command:

```
python3 update_fivem_server.py
```

## License

This script is licensed under the MIT License.
```
