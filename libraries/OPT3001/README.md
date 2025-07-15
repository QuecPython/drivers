# OPT3001 Ambient Light Sensor Example Code Documentation

## Overview

This document describes how to use the OPT3001 ambient light sensor based on QuecPython for light intensity measurement. The OPT3001 is a high-precision digital light sensor suitable for applications such as ambient light monitoring and display backlight control.

## Hardware Connection

Before using the OPT3001 module, ensure the hardware is properly connected:

- I2C interface connection (SCL/SDA)
- VCC connected to 3.3V power supply
- GND connected to ground

## Quick Start

### 1. Initialize the OPT3001 Module

```python
from machine import I2C
from usr.opt3001 import Opt3001

# Initialize I2C interface
i2c_obj = I2C(I2C.I2C1, I2C.FAST_MODE)
# Initialize OPT3001 sensor
opt = Opt3001(i2c_obj)
print("OPT3001 module initialized")
```

### 2. Basic Functionality

#### Single Measurement Mode

```python
# Set to single measurement mode
opt.set_measure_mode(1)
# Wait for measurement to complete (at least 800ms)
utime.sleep_ms(1000)
# Read light intensity
lux = opt.read()
print('Current light intensity: {0} lux'.format(lux))
```

#### Continuous Measurement Mode

```python
# Set to continuous measurement mode
opt.set_measure_mode(2)

while True:
    # Read light intensity
    lux = opt.read()
    print('Current light intensity: {0} lux'.format(lux))
    utime.sleep(1)  # Read once per second
```

## Advanced Features

### 1. Automatic Measurement and Recording

```python
# Initialize sensor
i2c_obj = I2C(I2C.I2C1, I2C.FAST_MODE)
opt = Opt3001(i2c_obj)

# Set to single measurement mode
opt.set_measure_mode(1)

for i in range(20):
    utime.sleep_ms(1000)  # 1-second interval between measurements
    print("Measurement count: {}------------".format(i+1))
    lux = opt.read()
    print("Light intensity: {0} lux".format(lux))
    # Trigger next measurement
    opt.set_measure_mode(1)
```

### 2. Low Power Mode

```python
# Set to shutdown mode to save power
opt.set_measure_mode(0)
print("Sensor entered low power mode")

# Wake up when measurement is needed
opt.set_measure_mode(1)  # Single measurement mode
utime.sleep_ms(1000)
lux = opt.read()
print("Current light intensity: {0} lux".format(lux))
```

## Notes

1. Ensure the I2C interface is correctly connected; do not reverse SCL and SDA lines.
2. In single measurement mode, each read requires re-triggering the measurement.
3. The interval between two reads must be greater than 800ms (sensor conversion time).
4. The default I2C address of the sensor is 0x44; adjust accordingly if modified.
5. Avoid direct strong light exposure to the sensor, as it may affect measurement accuracy.

## Troubleshooting

1. **Unable to read data**:
   - Check if the I2C connection is correct.
   - Confirm the sensor is powered properly (3.3V).
   - Verify the I2C address is correct.
2. **Inaccurate measurements**:
   - Ensure the sensor surface is clean and unobstructed.
   - Avoid exposing the sensor to extreme temperatures.
   - Check for direct strong light sources.
3. **Communication errors**:
   - Verify the I2C bus is functioning properly.
   - Confirm pull-up resistors are correctly connected.
   - Try reducing the I2C communication rate.

## API Reference

### Main Methods

- `set_measure_mode(mode)`: Sets the measurement mode.
  - Parameters:
    - mode: 0=shutdown, 1=single measurement, 2=continuous measurement.
  - Returns: 0=success, -1=failure.
- `read()`: Reads the light intensity value.
  - Returns: Current light intensity value (unit: lux).

I2C [Reference](https://developer.quectel.com/doc/quecpython/API_reference/en/peripherals/machine.I2C.html)