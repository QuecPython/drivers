# LTR303ALS Ambient Light Sensor Driver Documentation

## Overview

This document describes how to use the QuecPython-based LTR303ALS ambient light sensor for light intensity detection and interrupt control. The LTR303ALS is a dual-channel light sensor with I²C communication interface, suitable for applications requiring precise light sensing (e.g., automatic brightness adjustment, environmental monitoring).

------

## Hardware Connection

Before using the LTR303ALS module, ensure proper hardware connections:

- **I²C Interface**: Connect SCL/SDA pins to the development board’s corresponding interfaces.
- **VCC**: Connect to 3.3V power supply (operating voltage: 2.7–3.6V).
- **GND**: Ground.
- **INT Pin**: Connect to a development board GPIO interrupt pin (e.g., GPIO32).
- **ADDR Pin**: Ground to use default address `0x29` (leave unconnected for address `0x4D`).

------

## Quick Start

### 1. Initialize the LTR303ALS Module

```python
from machine import I2C, ExtInt
import itl_303als

# Initialize I²C interface (standard mode on I2C1)
i2c = I2C(I2C.I2C1, I2C.STANDARD_MODE)

# Initialize sensor (address 0x29, interrupt on GPIO32, falling edge trigger, threshold 100 lux)
als = itl_303als(i2c, 0x29, ExtInt.GPIO32, 100, itl_303als.IRQ_FALLING)
```

------

### 2. Basic Function Usage

```python
# Read current light intensity values (CH0/CH1)
ch0, ch1 = als.read()
print(f"CH0: {ch0}, CH1: {ch1}")

# Set a new interrupt threshold (200 lux)
als.set_threshold(200)
```

------

## Advanced Features

### 1. Interrupt Configuration

```python
# Configure interrupt trigger mode (rising/falling edge)
als.config_interrupt(itl_303als.IRQ_RISING)

# Set interrupt persistence condition (trigger after 10 consecutive detections)
als.set_persist(0x0A)
```

------

### 2. Auto Calibration

```python
# Start auto-calibration mode (duration: 10 seconds)
als.start_calibration(10000)

# Retrieve calibrated threshold value
calibrated = als.get_calibrated_threshold()
print(f"Calibrated Threshold: {calibrated}")
```

------

## Class and Method Reference

### `itl_303als` Class

#### Constructor

```python
itl_303als(i2c_bus, i2c_addr=0x29, int_pin=None, threshold=100, int_mode=IRQ_FALLING)
```

- `i2c_bus`: I²C bus object.
- `i2c_addr`: Device I²C address (default `0x29`).
- `int_pin`: Interrupt pin object (optional).
- `threshold`: Initial interrupt threshold (lux).
- `int_mode`: Trigger mode (`IRQ_RISING`/`IRQ_FALLING`).

#### Main Methods

|         Method Name          |    Parameters    |         Description         |
| :--------------------------: | :--------------: | :-------------------------: |
|           `read()`           |       None       |  Read CH0/CH1 light values  |
|      `set_threshold()`       | `threshold(int)` |   Set interrupt threshold   |
|     `config_interrupt()`     |   `mode(int)`    | Configure interrupt trigger |
|    `start_calibration()`     |  `duration(ms)`  |   Start auto-calibration    |
| `get_calibrated_threshold()` |       None       |  Get calibrated threshold   |

#### Properties

|    Property Name     | Type |         Description         |
| :------------------: | :--: | :-------------------------: |
| `interrupt_occurred` | bool |   Interrupt trigger flag    |
| `current_threshold`  | int  | Current interrupt threshold |

------

### Constants

|   Constant    | Value |     Description      |
| :-----------: | :---: | :------------------: |
| `IRQ_RISING`  |   0   | Rising-edge trigger  |
| `IRQ_FALLING` |   1   | Falling-edge trigger |

------

## Notes

1. Ensure correct I²C address configuration (determined by ADDR pin state).
2. Configure proper pull-up/pull-down resistors for the interrupt pin.
3. Avoid prolonged exposure to strong light environments (may damage the sensor).
4. Maintain stable lighting conditions during calibration.

------

## Troubleshooting

|     Symptom      |      Possible Cause       |           Solution           |
| :--------------: | :-----------------------: | :--------------------------: |
|   No data read   | I²C communication failure |   Check wiring and address   |
| Interrupt fails  | Invalid threshold setting | Adjust `threshold` parameter |
| Data fluctuation | Power noise interference  |    Add filter capacitors     |