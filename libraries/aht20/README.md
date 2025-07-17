# AHT20 Temperature and Humidity Sensor Example Code Documentation

## Overview

This document describes how to use the QuecPython-based AHT20 temperature and humidity sensor for environmental monitoring. The AHT20 is a high-precision digital sensor featuring ±2%RH humidity accuracy and ±0.2°C temperature accuracy, making it ideal for smart home, weather monitoring, and industrial control applications requiring high precision.

## Hardware Connection

Ensure proper hardware connections before using the AHT20 module:

- I2C interface (SCL/SDA)
- VCC connected to 3.3V power supply
- GND grounded
- Address selection pin (ADDR) left floating for default address **0x38**

## Quick Start

### 1. Initialize AHT20 Module

```python
from machine import I2C
from drivers.aht20 import Aht20

# Initialize I2C interface (use actual I2C bus)
i2c_obj = I2C(I2C.I2C1, I2C.FAST_MODE)
# Initialize AHT20 sensor (default address 0x38)
aht = Aht20(i2c_obj)
print("AHT20 module initialized")
```

### 2. Basic Function Usage

#### Single Measurement Mode

```python
# Read temperature and humidity data
humidity, temperature = aht.read()
print(f'Current humidity: {humidity}%RH, temperature: {temperature}°C')
```

#### Continuous Measurement Mode (with timing loop)

```python
import utime

while True:
    humidity, temperature = aht.read()
    print(f'Current humidity: {humidity}%RH, temperature: {temperature}°C')
    utime.sleep(2)  # Read every 2 seconds
```

## Precautions

1. Ensure correct I2C wiring (avoid SCL/SDA reversal)
2. Operating voltage: **3.3V ±0.1V**
3. Allow ≥15ms stabilization time before measurement
4. Avoid exposure to extreme temperatures (**-40~85°C**) or humidity (**>95%RH**)

## Troubleshooting

### 1. **Data Read Failure**

- Verify I2C connections
- Check 3.3V power supply
- Confirm I2C address (**default 0x38**)
- Ensure `read()` method is called (initial measurement trigger required)

### 2. **Abnormal Readings**

- Shield from direct sunlight/heat sources
- Ensure proper ventilation
- Restart device to reset sensor state
- Check against maximum range (**100%RH @ 85°C**)

## API Reference

### Class Initialization

```python
class Aht20:
    def __init__(self, i2c, address=0x38):
        """
        Initialize AHT20 sensor
        :param i2c: I2C object
        :param address: I2C slave address (default 0x38)
        """
```

### Core Methods

|       Method Name        | Parameters |             Return Value              |              Description               |
| :----------------------: | :--------: | :-----------------------------------: | :------------------------------------: |
|         `read()`         |    None    | `(humidity:float, temperature:float)` |     Get temperature/humidity data      |
| `get_calibration_data()` |    None    |                `dict`                 | Retrieve sensor calibration parameters |

## Supplementary Information

- **Datasheet**: `drivers/libraries/aht20/AHT20-datasheet.pdf`
- **Example Code**: `drivers/libraries/aht20/aht20_demo.py`
- [I2C Interface Reference]()
