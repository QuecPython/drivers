# GNSS Positioning Module Driver Documentation
## Overview 

This document explains how to use the GNSS positioning module driver to obtain satellite positioning data. This driver supports various functions for obtaining positioning data, including location, speed, altitude, key positioning information such as visible satellites.
## Main Features
- Obtain raw GNSS data (GGA/RMC/GSV format)
- Position status detection
- Obtain precise latitude and longitude coordinates
- Measure altitude and moving speed
- Statistics of visible satellites
- Positioning time acquisition
- Support for multiple positioning mode recognition

## Quick Start
### 1. Import Required Modules 
```python
from gnss import Gnss
import utime
```
### 2. Initialize the GNSS module 

```python
# UART1 initializes the GNSS module (with a baud rate of 9600) 
gnss = Gnss(
    uartn = 1  # UART port number
    baudrate = 9600  # Baud rate
    databits = 8  # Data bits
    parity = 0  # Parity
    stopbits = 1  # Stop bits
    flowctl = 0  # Flow control 
    )
```


### 3. Obtain positioning data 

```python
# Obtain location information 
if gnss.isFix():
    location = gnss.getLocation()
    print("Latitude and Longitude: {}{}, {}{}".format(location[0], location[1], location[2], location[3])) 
else:
    print("Failed to locate successfully. Please wait..." )
```

## API Interface Description 

**`Gnss(uartn, baudrate, databits, parity, stopbits, flowctl)`**


Construct the constructor and initialize the GNSS module. 

**Parameter Explanation:**


- uartn: UART port number (1, 2, etc.)
- baudrate: Communication baud rate (default 9600)
- databits: Data bits (usually 8)
- parity: Parity bit (0 - no parity check, 1 - odd parity check, 2 - even parity check)
- stopbits: Stop bits (1 or 2)
- flowctl: Flow control (0 - no flow control) 

**`read_gnss(retry=1, debug=0)`**


Read the original GNSS data. 

**Parameter Explanation:**


- retry: Number of retry attempts for reading
- debug: Switch for debug mode 

**Return Value:** 

- Success: (data_valid, data)
- Where data_valid is the valid bit identifier:
- 0x04: GGA is valid
- 0x02: RMC is valid
- 0x01: GSV is valid
- Failure: -1 

**`isFix()`**


Check if the positioning was successful. 

**Return value:**

- 1: Successfully located
- 0: Not yet located 

**`getUtcTime()`**


Obtain the UTC time for positioning. 

**Return Value:** 

- Success: UTC time string (formatted as "HHMMSS.SS")
- Failure: -1

**`getLocationMode()`**


Obtain the positioning mode. 

**Return Value:** 

- -1: Acquisition failed
- 0: Positioning is unavailable or invalid
- 1: GPS/SPS mode (standard positioning)
- 2: DGPS/DSPS mode (differential positioning)
- 6: Estimation mode (course position calculation) 

**`getUsedSateCnt()`**


Obtain the number of satellites used for positioning. 

**Return Value:** 

- Success: Number of satellites used
- Failure: -1 

**`getLocation()`**


Obtain precise latitude and longitude information. 

**Return Value:** 

- Success: (longitude, lon_direction, latitude, lat_direction)
  - longitude: Longitude value (floating point number)
  - lon_direction: Longitude direction ('E' or 'W')
  - latitude: Latitude value (floating point number)
  - lat_direction: Latitude direction ('N' or 'S')
- Failure: -1 

**`getViewedSateCnt()`**


Obtain the number of visible satellites. 

**Return Value:** 

- Success: Visible satellite count
- Failure: -1 

**`getGeodeticHeight()`**


Obtain the altitude. 

**Return Value:** 

- Success: Altitude (unit: meters)
- Failure: -1 

**`getCourse()`**


Obtain the azimuth angle of the visible satellite. 

**Return Value:** 

- Success: Satellite azimuth data in dictionary format, key is satellite number, value is azimuth
- Failure: -1 

**`getSpeed()`**


Obtain the ground speed. 

**Return Value:** 

- Success: Ground speed (unit: km/h)
- Failure: -1

## Application Examples
Basic Positioning Application 
```python
gnss = Gnss(1, 9600, 8, 0, 1, 0)

while True:
    if gnss.isFix():
        # Obtain location information 
        lon, lon_dir, lat, lat_dir = gnss.getLocation()
        height = gnss.getGeodeticHeight()
        speed = gnss.getSpeed()

        print("Location: {:.6f}{}, {:.6f}{}".format(lat, lat_dir, lon, lon_dir))
        print("Altitude: {} meters, Speed: {} km/h".format(height, speed)) 
    else:
        used_sats = gnss.getUsedSateCnt()
        visible_sats = gnss.getViewedSateCnt()
        print("Locating... Using satellites: {}, Visible satellites: {}".format(used_sats, visible_sats)) 
    utime.sleep(1)
```



Satellite information analysis 
```python
gnss = Gnss(1, 9600, 8, 0, 1, 0)

def analyze_satellites():
while not gnss.isFix():
    utime.sleep(1)

    # Obtain satellite azimuth information 
    satellite_data = gnss.getCourse()
    visible_sats = gnss.getViewedSateCnt()

    print("A total of {} satellites can be seen:".format(visible_sats)) 
    for sat_id, azimuth in satellite_data.items():
        print("Satellite {}: Azimuth {}°".format(sat_id, azimuth)) 

analyze_satellites()
```

## Common Issues Troubleshooting
### Long-term Failure to Locate 

- Possible causes:
- Poor or damaged antenna connection
- Positioning module not powered on
- Poor satellite signal in the current environment