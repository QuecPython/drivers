

# LIS2DH12 Accelerometer Sensor Driver User Manual

## Overview

This document describes how to use the LIS2DH12 accelerometer sensor driver code provided by Quectel. The LIS2DH12 is a low-power three-axis accelerometer suitable for various motion detection applications.

## Key Features

- Sensor initialization and reset
- Acceleration data reading
- Interrupt function configuration (single-click, double-click, motion detection, etc.)
- Operation mode settings

## Quick Start

### 1. Initialize the Sensor

python

```
def __init__(self, i2c_dev, int_pin, slave_address=0x19):
        self._address = slave_address
        self._i2c_dev = i2c_dev
        self._int_pin = int_pin
        self._extint = None
        self._sensor_init()
```

### 2. Read Acceleration Data

python

```
# Read three-axis acceleration data
 def read_acceleration(self):
        '''
        read acceleration
        :return: x,y,z-axis acceleration
        '''

        while 1:
            status = self._read_data(LIS2DH12_STATUS_REG,1)[0]
            xyzda = status & 0x08   # if xyz data exists, set 1
            xyzor = status & 0x80
            if not xyzda:
                continue
            else:
                x,y,z = self._acceleration
                return (x, y, z)
```

### 3. Configure Interrupt Function

text

```
# Define interrupt callback function
 def set_int_callback(self, cb):
        self._extint = ExtInt(self._int_pin, ExtInt.IRQ_FALLING, ExtInt.PULL_PU, cb)
```

## API Details

### 1. Constructor `__init__(self, i2c_dev, int_pin, slave_address=0x19):`

- Parameters:
  - `i2c_dev`: I2C device object
  - `int_pin`: GPIO number connected to the sensor interrupt pin
  - `slave_address`: Sensor I2C address (default 0x19)

### 2. Main Methods

#### `sensor_reset()`

Reset the sensor

#### `int_enable(int_type, int_ths=0x12, time_limit=0x18, time_latency=0x12, time_window=0x55, duration=0x03)`

Enable interrupt function

- Parameters:
  - `int_type`: Interrupt type (e.g., XYZ_SINGLE_CLICK_INT)
  - `int_ths`: Interrupt threshold
  - `time_limit`: Time limit (for click interrupt)
  - `time_latency`: Latency time (for double-click interrupt)
  - `time_window`: Time window (for double-click interrupt)
  - `duration`: Duration

#### `set_int_callback(cb)`

Set interrupt callback function

- Parameters:
  - `cb`: Callback function

#### `set_mode(mode)`

Set operation mode

- Parameters:
  - `mode`: 0-High resolution mode, 1-Normal mode, 2-Low power mode

### 3. Main Properties

#### `read_acceleration`

Read current three-axis acceleration values (unit: g)

#### `int_processing_data()`

Process interrupt and return current acceleration values

## Interrupt Type Constants

| Constant Name        | Description                     |
| :------------------- | :------------------------------ |
| XYZ_SINGLE_CLICK_INT | XYZ-axis single-click interrupt |
| X_SINGLE_CLICK_INT   | X-axis single-click interrupt   |
| Y_SINGLE_CLICK_INT   | Y-axis single-click interrupt   |
| Z_SINGLE_CLICK_INT   | Z-axis single-click interrupt   |
| XYZ_DOUBLE_CLICK_INT | XYZ-axis double-click interrupt |
| MOVE_RECOGNIZE       | Motion detection interrupt      |
| FF_RECOGNIZE         | Free-fall interrupt             |

## Notes

1. Ensure the I2C bus is properly initialized before use
2. The interrupt pin needs to be correctly configured
3. Check data ready status before reading acceleration data
4. Different operation modes affect power consumption and accuracy

## Technical Support

For further assistance, please contact Quectel technical support team.