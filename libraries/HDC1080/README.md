# HDC1080 Temperature and Humidity Sensor Driver Documentation
## Overview 

This document explains how to use the HDC1080 temperature and humidity sensor driver module to measure the ambient temperature and humidity. This sensor provides high-precision temperature and humidity data via the I2C interface and is suitable for various environmental monitoring applications.
## Key Features 

- Measure both temperature and humidity simultaneously
- High-precision measurement (temperature ± 0.2°C, humidity ± 2%)
- Ultra-low power consumption design (typical 1.2 μA)
- I2C digital interface
- Fast response time

## Quick Start
### 1. Import Required Modules 
```python
from machine import I2C
from hdc1080 import Hdc1080
import utime
```
2. Initialize the sensors 
```python
# Initialize the HDC1080 sensor on the I2C1 bus 
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
sensor = Hdc1080(i2c_dev)
```
3. Read temperature and humidity data 
```python
# Read temperature and humidity data 
humidity, temperature = sensor.read()
print("Temperature: {:.2f}°C, Humidity: {:.2f}%".format(temperature, humidity)) 
```

## API Interface Description 

**`Hdc1080(i2c_obj, dev_addr=0x40)`**


Construct the constructor and initialize the HDC1080 sensor. 

**Parameter Explanation:**


- i2c_obj: I2C device instance
- dev_addr: Sensor I2C address (default 0x40) 

**`read()`**


Read and return the current temperature and humidity values. 

**Return Value: ** 

- (humidity, temperature): Humidity percentage value and temperature value
- humidity: Relative humidity (unit: %)
- temperature: Temperature (unit: °C) 

**`reset()`**


Reset the sensor and restore factory settings. After the operation, the sensor needs to be reinitialized.

## Application Examples 

Basic environmental monitoring 
```python
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
sensor = Hdc1080(i2c_dev)


while True:
    humidity, temperature = sensor.read()
    print("Temperature: {:.2f}°C, Humidity: {:.2f}%".format(temperature, humidity)) 
    utime.sleep(10)
```


Temperature anomaly alarm system 
```python
def check_temperature_alert(temp, hum):
    critical_alerts = []
    warnings = []

    if temp > 35:
        critical_alerts.append("High temperature alert!") 
    elif temp < 0:
        critical_alerts.append("Low temperature alert!") 
    elif temp > 30:
        warnings.append("High temperature") 
    elif temp < 5:
        warnings.append("Low temperature") 
    if hum > 85:
        warnings.append("Excessive humidity") 
    elif hum < 20:
        warnings.append("Low humidity") 
    return critical_alerts, warnings

sensor = Hdc1080(i2c_dev)
while True:
    humidity, temperature = sensor.read()
    critical, warnings = check_temperature_alert(temperature, humidity)

    if critical:
        # Emergency Alert Processing Logic
        print("⚠️ Emergency Alert:", ", ".join(critical)) 
    if warnings:
        print("Warning:", ", ".join(warnings)) 
    utime.sleep(60)
```

## Common Issues Troubleshooting 

- I2C address error (correct address 0x40)
- I2C bus not initialized
- Sensor power supply abnormal
- There is a heat source interference near the sensor
- Humidity sensor exposed to condensation environment