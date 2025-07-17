# ESP8266 WiFi Module Driver Documentation
## Overview 

This document explains how to use the ESP8266 WiFi module driver to enable the wireless connection function of IoT devices. This driver communicates with the ESP8266 module through the SLIP protocol and TLV data format, and supports the creation of WiFi access points (AP) and connection to mobile data networks. 

## Main Features
- WiFi Access Point Configuration: Supports custom SSID and password
- Automatic Routing Configuration: Enables seamless communication between networks
- Modular Management: Simple AP configuration and control of working modes
- Error Handling Mechanism: Comprehensive anomaly detection and handling

## Quick Start
### 1. Import Required Modules 

```python
from machine import UART
from esp8266_ap import Esp8266_ap
import utime
```


### 2. Initialize the ESP8266 module 
```python
# Initialize the ESP8266 module using the UART2 interface 
esp = Esp8266_ap(UART.UART2)
```
### 3. Set up a WiFi access point 
```python
# Configure WiFi access point (SSID: MyAP, password: 12345678) 
esp.set_ap(name='MyAP', pwd='12345678')
```


### 4. Enable WiFi function 

```python
# Enable the WiFi module and complete the network configuration 
if esp.wifi_on() == 0:
    print('WiFi module has started successfully')
    # Here, you can add the business logic after the device is connected to the network 
    while True:
        utime.sleep(10)
else:
print('WiFi module startup failed') 
```

## API Interface Description 

**`Esp8266_ap(uart)`**


Constructor, initializing the ESP8266 module. 

**Parameter Description:**


- uart: UART interface instance 

**`set_ap(name=None, pwd=None, project_name='wifi_setap', project_version='1.0.0')`**


Configure the parameters of the WiFi access point. 

**Parameter Description:**


- name: WiFi access point name (SSID)
- pwd: WiFi access point password
- project_name: Project name (used for network detection)
- project_version: Project version (used for network detection) 

**Return Value:** 

- 0: Success
- -1: Failure 

**`wifi_on()`**


Enable the WiFi function and configure the network. 

**Return Value:** 

- 0: Success
- -1: Failure 

**`wifi_off()`**


Turn off the WiFi function to free up resources.

## Application Example
Basic WiFi Access Point Configuration 
```python
# Set custom SSID and password 
esp.set_ap(name='Quectel_WiFi', pwd='SecurePass123')
```
Open AP without password 
```python
# Create an open access point without a password 
esp.set_ap(name='Free_WiFi_Access')
```
Password-protected AP 
```python
# Create an access point that is password-protected but hides the SSID 
esp.set_ap(pwd='HiddenNetworkPass')
```
Multi-network collaboration applications 
```python
esp = Esp8266_ap(UART.UART2)
esp.set_ap(name='IoT_Gateway', pwd='iot12345')


if esp.wifi_on() == 0:
    print('The device has connected to both mobile network and WiFi network') 
    while True:
    # Here, business logic for simultaneous access to dual networks can be added
    # For example: Report data via mobile network, manage devices via local WiFi utime.
    sleep(60)
```
Network Health Monitoring 
```python
import ujson


def network_health_check():
    # Check network status 
    esp_info = esp._wait_datacall_success()
    return ujson.dumps(esp_info)

esp.set_ap(name='Network_Monitor')
esp.wifi_on()

# Regularly report network status 
while True:
    status = network_health_check()
    print("Current network status: {}".format(status)) 
    utime.sleep(300)
```

## Technical Description
### 1. Usage of the SLIP Protocol 

- Serial Line Interface Protocol (Serial Line IP)
- Operates based on UART communication
- Protocol type: SLIP_INNER (Internal Network) 

### 2. TLV Data Format
| Field | Length | Description | 
|----|----|----|
| Head | 2 bytes | Identifier for data type (F1/F2/F3) |
| Length | 4 bytes | Length of data content (0000-9999) |
| Content | Variable length | Actual configuration data | 

**Headline:**


- F1: Password mode only
- F2: SSID mode only
- F3: Complete SSID + Password mode 

### 3. Routing Configuration 

- Default Gateway: 172.16.1.2
- AP Address Range: 192.168.4.0/24
- Subnet Mask: 255.255.255.0 

## Network Configuration Parameters
### 1. Default Server 

- IP address: 172.16.1.5

- Port number: 100 

### 2. Device Binding Address 

- IP address: 172.16.1.2

- Port number: 10001 

### 3. Mobile Network Priority
| Network Type | Priority | 
|----|----|
|LTE/5G| High |
|WiFi| Medium |
|Wired Network| Low |
## Network Configuration Parameters
### 1. Default Server 

- IP address: 172.16.1.5
- Port number: 100 

2. Device Binding Address 

- IP address: 172.16.1.2
- Port number: 10001 

### 3. Mobile Network Priority
| Network Type | Priority | 
|----|----|
|LTE/5G| High |
|WiFi| Medium |
|Wired Network| Low | 

## Common Issues Troubleshooting
### 1. Initialization Failure 

- Phenomenon: "slip netif construct fail" error
- Solution:
    - Check if the UART wiring is correct (TX/RX cross connection)
    - Confirm that the UART baud rate settings are consistent (usually 115200)
    - Verify if the power supply of the ESP8266 module is stable 

### 2. AP configuration failed 

- Phenomenon: Failure to set AP error
- Solution:
    - Check the network connection status: checkNet.wait_network_connected()
    - Confirm that the server address is reachable (172.16.1.5)
    - Verify the length of the SSID and password (SSID: 1-32 characters, password: 8-64 characters) 

### 3. Network Routing Error 

- Phenomenon: Unable to access both networks simultaneously
- Solution:
    - Confirm that the return value after calling wifi_on() is 0
    - Check if the routing table contains the 192.168.4.0/24 network segment
    - Verify if the default gateway settings are correct

### 4. Connection Stability Issues 

- Phenomenon: Frequent disconnections of connection
- Solution:
    - Shorten the distance between the device and the AP
    - Avoid interference from 2.4GHz frequency band (such as microwave ovens, Bluetooth devices)
    - Update the ESP8266 firmware to the latest version 

**Connection status monitoring:**
```python
def check_connection():
    try:
        # Attempt to access the server to verify the connection 
        sock = usocket.socket()
        sock.connect(('172.16.1.5', 1000)) return True
    except:
        return False
```
**Automatic Reconnection Mechanism:**
```python
while True:
    if not check_connection():
        print("Connection lost. Attempting to reconnect..." )
        esp.wifi_off()
        esp.set_ap(name='MyAP', pwd='password')
        esp.wifi_on()
    utime.sleep(60)
```
This driver provides a complete WiFi configuration and management solution for the ESP8266 module.