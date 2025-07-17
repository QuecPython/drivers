# HDC2080 Temperature and Humidity Sensor Driver Documentation
## Overview 

This document explains how to use the HDC2080 temperature and humidity sensor driver module to accurately measure the ambient temperature and humidity. The sensor provides digital temperature and humidity data via the I2C interface, featuring low power consumption and high accuracy.
## Key Features 

- High-precision temperature and humidity measurement (temperature ± 0.2°C, humidity ± 2%)
- Ultra-wide range: temperature (-40°C ~ 85°C), humidity (0% ~ 100%)
- Dual 16-bit analog-to-digital converters
- I2C digital interface (default address 0x40)
- Low power consumption mode (typical standby current 0.1μA) 

## Quick Start
### 1. Import Required Modules 
```python
from machine import I2C
from hdc2080 import Hdc2080
import utime
```
2. Initialize the sensors 
```python
# Initialize the HDC2080 sensor on the I2C1 bus 
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
sensor = Hdc2080(i2c_dev)
```
3. Read temperature and humidity data 
```python
# Read temperature and humidity data 
humidity, temperature = sensor.read()
print("Temperature: {:.2f}°C, Humidity: {:.2f}%".format(temperature, humidity)) 
```
## API Interface Description 

**`Hdc2080(i2c, addr=0x40)`**


Construct the constructor and initialize the HDC2080 sensor. 

**Parameter Explanation:**


- i2c: I2C device instance
- addr: Sensor I2C address (default 0x40) 

**`reset()`**


Reset the sensor and restore to factory settings. 

**`read_temperature()`**


Read the current temperature value. 

**Return Value:** 

Temperature value (unit: °C) 

**`read_humidity()`**


Read the current humidity value. 

**Return Value:** 

Humidity value (unit: %) 

**`read()`**


Trigger the temperature and humidity measurement and read the results. 

**`Return Value:`** 

- (humidity, temperature): Humidity percentage value and temperature value

## Application Examples
Basic Environmental Monitoring 
```python
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
sensor = Hdc2080(i2c_dev)


while True:
    humidity, temperature = sensor.read()
    print("Temperature: {:.2f}°C, Humidity: {:.2f}%".format(temperature, humidity)) 
    utime.sleep(10)
```

## Common Issues Troubleshooting
- I2C address error (correct address: 0x40)
- I2C bus not initialized
- Sensor power supply abnormal
- Interference from heat source near the sensor
- Humidity sensor exposed in a condensation environment