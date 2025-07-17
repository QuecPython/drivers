# PL5NF001 Sensor Driver Documentation
## Overview 

This document explains how to use the PL5NF001 sensor driver module to achieve communication functionality based on GPIO and the I2C protocol. This driver provides complete control over I2C communication timing, and supports basic operations such as start signal, stop signal, and data reading and writing. 

## Main Features 

- GPIO-based analog I2C communication protocol
- Supports standard I2C timing control
- Complete implementation of start/stop signals
- ACK/NACK response mechanism
- Byte read/write function
- Flexible delay control

## Quick Start
### 1. Initialize the Sensor 
```python
from pl5nf001 import PL5NF001

# Initialize the PL5NF001 sensor 
sensor = PL5NF001()
```


2. Basic Communication Operations 
```python
# Send start signal 
sensor.start_signal()

# Write data bytes 
sensor.write_data(0x55)


# Waiting for ACK response 
if sensor.wait_ack() == 0:
    print("Received ACK response") 
else:
    print("No ACK response received") 

# Read data bytes
data = sensor.read_byte(ack=1)  
# Send ACK after reading
print("Read data: 0x{:02X}".format(data)) 

# Send stop signal 
sensor.stop_signal()
```
## API Interface Description 

**`PL5NF001()`**


Construct the constructor and initialize the PL5NF001 sensor. 

**`start_signal()`**


Send the I2C start signal. 

**`stop_signal()`**


Send the I2C stop signal. 

**`ack()`**


Send the ACK response signal. 

**`nack()`**


Send the NACK response signal. 

**`wait_ack()`**


Wait for the device to send an ACK response. 

**Return Value:** 

- 0: Received ACK
- 1: Timeout - No ACK received 

**`write_data(data)`**


Write a single byte of data to the device. 

**Parameter Description:**


- data: The data bytes to be written (0 - 255) 

**`read_byte(ack)`**


Read a byte of data from the device. 

**Parameter Description:**


- ack: Whether to send an ACK after reading
    - 1: Send ACK
    - 0: Send NACK 

- Return value: 

    - The read-in data bytes

## Application Examples
Basic Reading and Writing Operations 
```python
sensor = PL5NF001()

# Initiate Communication 
sensor.start_signal()

# Write device address 
sensor.write_data(0x48)
if sensor.wait_ack() ! = 0:
    print("Device is unresponsive") 
    return

# Write to register address 
sensor.write_data(0x01)
sensor.wait_ack()

# Read data
data = sensor.read_byte(ack=0)  
# The last byte is sent as NACK 

# End Communication 
sensor.stop_signal()

print("Read register value: 0x{:02X}".format(data)) 
```

Multibyte reading 
```python
def read_multiple_bytes(sensor, address, reg, count):
    sensor.start_signal()

    # Write device address + Write mode 
    sensor.write_data(address << 1)
    if sensor.wait_ack() ! = 0: 
        return None

    # Write to register address 
    sensor.write_data(reg)
    sensor.wait_ack()

    # Start Over 
    sensor.start_signal()

    # Write device address + Read mode 
    sensor.write_data((address << 1) | 1)
    sensor.wait_ack()

    # Read data data = []
    for i in range(count):
        ack = 1 if i < count - 1 else 0  # The last byte sends NACK 
        data.append(sensor.read_byte(ack))

    sensor.stop_signal()
    return data


# Read 3 bytes of data 
sensor = PL5NF001()
result = read_multiple_bytes(sensor, 0x48, 0x00, 3)
print("Read data: {}".format(result)) 
```


## Common Issues Troubleshooting
| Problem Phenomenon | Possible Causes | 
|----|----|
Unable to receive ACK | Device address error
All data read are 0 | Device not initialized
Unstable communication | Timing parameters do not match
Data error | Timing disorder
Unable to generate start/stop signals | GPIO configuration error