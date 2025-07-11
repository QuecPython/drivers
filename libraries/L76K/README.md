GNSS 定位模块驱动

**Class reference:**

```python
from gnss_driver import Gnss
```

**Instance parameters:**
| Name | Required | Type | Description | |----|----|----|----|
| uartn | is | int | UART port number |
| baudrate | is | int | Baud rate |
| databits | is | int | Data bits |
| parity | is | int | Parity bit |
| stopbits | is | int | Stop bits |
| flowctl | is | int | Flow control |

```python
    gnss = Gnss(1, 9600, 8, 0, 1, 0)
```
**Interface function:**

l read_gnss(retry=1, debug=0)

Read the raw data of GNSS.

Parameters: 

| Name | Type | Default Value | Description | 
|----|----|----|----|
| retry | int | 1 | Number of retries |
| debug | int | 0 | Debug mode |

Return value: 

-1: Failure 

(data_valid, data): Success 

data_valid: Data Valid Bit (0x01 - 0x07) 

data: Raw GNSS data

l isFix()

Check if the positioning was successful. 

Return value: 

1: Successful positioning

0: Failed positioning

l getUtcTime()

Obtain the UTC time for positioning. 

Return value: 

Success: UTC time string 

Failure: -1

l getLocationMode()

Obtain the positioning mode. 

Return value: 

-1: Failure in acquisition 

0: Positioning is unavailable 

GPS/SPS mode 

2: DGPS/DSPS Mode 

6: Estimation Mode

l getUsedSateCnt()

Obtain the number of satellites used for positioning. 

Return value: 

Success: Number of satellites 

Failure: -1

l getLocation()

Obtain the latitude and longitude information. 

Return value: 

Success: (Longitude, Longitude direction, Latitude, Latitude direction) 

Failure: -1

l getViewedSateCnt()

Obtain the number of visible satellites. 

Return value: 

Success: Number of satellites 

Failure: -1

l getGeodeticHeight()

Obtain the altitude. 

Return value: 

Success: Altitude (in meters) 

Failure: -1

l getCourse()

Obtain the satellite azimuth angle. 

Return value: 

Dictionary: {Satellite Number: Azimuth}

l getSpeed()

Obtain the ground speed. 

Return value: 

Success: Speed (KM/h) 

Failure: -1