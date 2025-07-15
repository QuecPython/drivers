# BMA250 Accelerometer Sensor Driver Documentation

## Overview

This document provides usage instructions for the BMA250 accelerometer sensor driver developed by Quectel. The BMA250 is a low-power digital triaxial acceleration sensor with flexible configuration options.

## Key Features

- Sensor initialization and reset
- Configurable measurement range (±2g to ±16g)
- Adjustable output data rate (7.81Hz to 1000Hz)
- Multiple interrupt functions (tap, slope, orientation, etc.)
- Acceleration data reading

## Quick Start Guide

### 1. Initialization

```python
from machine import I2C
from bma250 import Bma250

# Initialize I2C interface
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)

# Create sensor instance
sensor = Bma250(i2c_dev)
```

### 2. Basic Configuration

```python
# Set measurement range (default ±2g)
sensor.set_range(Bma250.RANGE_SEL_2G)  # Options: RANGE_SEL_2G, RANGE_SEL_4G, RANGE_SEL_8G, RANGE_SEL_16G

# Set output data rate (default 7.81Hz)
sensor.set_hz(Bma250.BW_SEL_1000)  # Options from BW_SEL_7_81 to BW_SEL_1000
```

### 3. Reading Acceleration Data

```python
# Read acceleration values (x, y, z in g)
x, y, z = sensor.read_acceleration()
print(f"X: {x}g, Y: {y}g, Z: {z}g")
```

## Interrupt Configuration

### Available Interrupt Types

| Interrupt Constant | Description                  |
| :----------------- | :--------------------------- |
| `slope_en_x`       | X-axis slope detection       |
| `slope_en_y`       | Y-axis slope detection       |
| `slope_en_z`       | Z-axis slope detection       |
| `slope_en_xyx`     | Any-axis slope detection     |
| `d_tap_en`         | Double-tap detection         |
| `s_tap_en`         | Single-tap detection         |
| `orient_en`        | Orientation change detection |
| `flat_en`          | Flat position detection      |
| `low_g_en`         | Low-g detection (free fall)  |
| `high_g_en_x`      | X-axis high-g detection      |
| `high_g_en_y`      | Y-axis high-g detection      |
| `high_g_en_z`      | Z-axis high-g detection      |
| `high_g_en_xyx`    | Any-axis high-g detection    |

### Example: Configuring Tap Detection

```python
# Enable single-tap detection
sensor.int_enable(Bma250.s_tap_en)

# Wait for and process tap event
while True:
    if sensor.process_single_tap():
        print("Single tap detected!")
        x, y, z = sensor.read_acceleration()
        print(f"Current acceleration: X={x}g, Y={y}g, Z={z}g")
        break
    utime.sleep_ms(10)
```

### Example: Free Fall Detection

```python
# Enable low-g (free fall) detection
sensor.int2_enable(Bma250.low_g_en)

# Wait for free fall event
while True:
    if sensor.process_low_g():
        print("Free fall detected!")
        break
    utime.sleep_ms(10)
```

## Advanced Configuration

### Interrupt Parameters

The interrupt functions accept several configuration parameters:

```
# Example with all parameters (default values shown)
sensor.int_enable(
    int_code=Bma250.s_tap_en,
    tap_thr=0x03,     # Tap threshold
    tap_dur=0x04,     # Tap duration
    slop_thr=0x14,    # Slope threshold
    slop_dur=0x03,    # Slope duration
    flat_hold_time=0x10  # Flat position hold time
)

sensor.int2_enable(
    int_code=Bma250.low_g_en,
    low_mode=0x81,    # Low-g mode
    low_th=0x30,      # Low-g threshold
    low_dur=0x09,     # Low-g duration
    high_th=0xc0,     # High-g threshold
    high_dur=0x0f     # High-g duration
)
```

## Error Handling

The driver raises `CustomError` exceptions for various error conditions:

```python
try:
    sensor = Bma250(i2c_dev)
    sensor.set_range(Bma250.RANGE_SEL_4G)
except CustomError as e:
    print(f"Error: {e}")
```

## Example Application

```python
from machine import I2C
from bma250 import Bma250
import utime

# Initialize
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
sensor = Bma250(i2c_dev)

# Configure for high sensitivity
sensor.set_range(Bma250.RANGE_SEL_2G)
sensor.set_hz(Bma250.BW_SEL_1000)

# Enable orientation detection
sensor.int_enable(Bma250.orient_en)

# Main loop
while True:
    if sensor.process_orient():
        x, y, z = sensor.read_acceleration()
        print(f"Orientation changed! Current values: X={x}g, Y={y}g, Z={z}g")
    
    utime.sleep_ms(100)
```

## Notes

1. The sensor requires proper power supply and I2C pull-up resistors
2. Interrupt pins must be properly configured in hardware
3. Higher data rates consume more power
4. Lower measurement ranges provide better resolution but smaller maximum detectable acceleration

For technical support, please contact Quectel Wireless Solutions.