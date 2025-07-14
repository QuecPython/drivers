# GNSS Positioning Module Driver 

"Class Reference" 
```python
from gnss_driver import Gnss
```


**Instantiation Parameters:** 

| Name | Required | Type | Description | 
|----|----|----|----|
| uartn | is | int | UART port number |
| baudrate | is | int | Baud rate |
| databits | is | int | Data bits |
| parity | is | int | Parity |
| stopbits | is | int | Stop bits |
| flowctl | is | int | Flow control | 

**Interface Function:** 

l read_gnss(retry=1, debug=0)


Read the raw data of GNSS. 

**Parameters:** 

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


Check if the positioning was successful 

Return value: 

1: Successful positioning 

0: Positioning failed 

l getUtcTime()


Obtain the UTC time of the location 

Return value: 

Success: UTC time string 

Failure: -1 

l getLocationMode()


Obtain positioning mode 

Return value: 

-1: Failure in acquisition 

0: Positioning is unavailable 

GPS/SPS mode 

2: DGPS/DSPS Mode 

6: Estimation Mode 

l getUsedSateCnt()


Obtain the number of satellites used for positioning 

Return value: 



Success: Number of Satellites 

Failure: -1 

l getLocation()


Obtain latitude and longitude information 

Return value: 

Success: (Longitude, Longitude direction, Latitude, Latitude direction) 

Failure: -1 

getViewedSateCnt()


Obtain the number of visible satellites 

Return value: 



Success: Number of Satellites 

Failure: -1 

l getGeodeticHeight()


Obtain the altitude 

Return value: 

Success: Altitude (meters)
Failure: -1 getCourse()
Obtain the satellite azimuth angle 

Return value: 

Dictionary: {Satellite Number: Azimuth} getSpeed()
Obtain the ground speed 

Return value: 

Success: Speed (KM/h)
Failure: -1