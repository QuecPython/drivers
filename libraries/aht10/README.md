# AHT10 Temperature and Humidity Sensor Example Code Documentation

## Overview

This document describes how to use the QuecPython-based AHT10 temperature and humidity sensor for environmental monitoring. The AHT10 is a high-precision digital sensor suitable for applications such as smart homes, weather monitoring, and industrial control systems.

## Hardware Connection

Ensure proper hardware connections before using the AHT10 module:

- I2C interface (SCL/SDA)
- VCC connected to 3.3V power supply
- GND grounded
- Address selection pin (ADDR) left floating for default address 0x38

## Quick Start

### 1. Initialize AHT10 Module

```python
from machine import I2C
from drivers.aht10 import Aht10

# Initialize I2C interface (use actual I2C bus)
i2c_obj = I2C(I2C.I2C1, I2C.FAST_MODE)
# Initialize AHT10 sensor (default address 0x38)
aht = Aht10(i2c_obj)
print("AHT10 module initialized")
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
2. Operating voltage: 3.3V ±0.1V
3. Allow ≥15ms stabilization time before measurement
4. Avoid extreme temperatures (-40~85°C) or humidity (>95%RH)

## Troubleshooting

1. **Data Read Failure**:
   - Verify I2C connections
   - Check 3.3V power supply
   - Confirm I2C address (default 0x38)
2. **Abnormal Readings**:
   - Shield from direct sunlight/heat sources
   - Ensure proper ventilation
   - Reset device to clear sensor state

## API Reference

### Class Initialization

```
class Aht10:
    def __init__(self, i2c, address=0x38):
        """
        Initialize AHT10 sensor
        :param i2c: I2C object
        :param address: I2C slave address (default 0x38)
        """
```

### Core Methods

|      Method Name       | Parameters |            Return Value             |              Description               |
| :--------------------: | :--------: | :---------------------------------: | :------------------------------------: |
|         read()         |    None    | (humidity:float, temperature:float) |     Get temperature/humidity data      |
| get_calibration_data() |    None    |                dict                 | Retrieve sensor calibration parameters |

## Supplementary Information

- Datasheet: `drivers/libraries/aht10/AHT10.pdf`
- Example code: `drivers/libraries/aht10/aht10_demo.py`
- [I2C Interface Reference](https://developer.quectel.com/doc/quecpython/API_reference/en/peripherals/machine.I2C.html)
