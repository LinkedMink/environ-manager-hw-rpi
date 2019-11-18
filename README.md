# Environ Manager for Raspberry Pi

## Introduction
I wanted to create a simple, networked system that I could customize as needed 
to monitor environmental factors for enclosed environments (terrariums, grow 
chambers, etc.). Essentially, I wanted a custom IoT solution I could understand
at a low level and manage myself without abstraction layers (Alexa Skills, Automation 
Hubs, and the like). It should be able to save info to a server for further analysis. 
Secondarily, it should be able to react to changes in the environment and correct them.

This is meant to be used in a client/server system with remote sensor/control 
hardware. See:
- https://github.com/LinkedMink/environ-manager-hw-rpi
- https://github.com/LinkedMink/environ-manager-server
- https://github.com/LinkedMink/environ-manager-client

Disclaimer: This project was mainly intended as a learning aid and for private use.

## Getting Started

### Required Packages
Install packages not included in Raspbian.

```bash
pip3 install --upgrade pip setuptools wheel  
pip3 install psycopg2 # (or any DB engine compatible with SQL alchemy)  
pip3 install pyodbc   # (or any DB engine compatible with SQL alchemy)  
pip3 install sqlalchemy  
pip3 install Adafruit_Python_DHT  
```

### Edit config.py
ConnectionString: https://docs.sqlalchemy.org/en/13/core/engines.html

You can leave the value empty then nothing will be logged. This project has been tested on
SQL Server. The latest version of PostgreSql caused problems with the .NET server application.

HttpHost: The host name of this device

This should match the seed value that's inserted within the .NET application. It's used to
uniquely identity a hardware device.

### Create Schema
This can be ran alone without the API server. You can create the database schema:

```bash
python3 create_schema.py  
```

However, it's probably best to create the entire schema for the API server.

See: https://github.com/LinkedMink/environ-manager-server

### Wire Hardware
See the schematic. It's pretty general, and the components can be swapped out as needed.

![Wiring Schematic](https://github.com/LinkedMink/environ-manager-hw-rpi/raw/master/schematic/SchematicExport.png "Wiring Schematic")

#### Component List
- Raspberry Pi
- DHT22
- 1 x 10k Resistor
- 1 x 1k Resitor
- 1 x NPN Transistor
- 1 x LED
- Control Hardware (As needed)
    - 4 x 1k Resitor
    - 3 x NPN Power Transistors
    - Lighting LEDs
    - Humidifier Element
    - Heating Element
    - Power Supply

### Run Software
```bash
python3 environ_manager.py  
```

## Autostart
If everything is working correctly, you can have the process start on boot.

```bash
sudo vi /etc/systemd/system/environ-manager.service  
```

Point the service to the python script.

> [Unit]  
> Description=Environ Manager  
> After=multi-user.target  
>   
> [Service]  
> Type=simple  
> ExecStart=/usr/bin/python3 /path/to/source/environ_manager.py  
> StandardInput=tty-force  
>   
> [Install]  
> WantedBy=multi-user.target  

Enable the server.

```bash
sudo systemctl daemon-reload  
sudo systemctl enable environ-manager.service  
sudo systemctl start environ-manager.service  
```

Check that it started correctly.

```bash
sudo systemctl status environ-manager.service
```
