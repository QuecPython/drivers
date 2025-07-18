# BH1750(GY302) Environmental Light Sensor Driver Documentation
## Overview 

This document explains how to use the BH1750 (or GY302 module) ambient light sensor to detect light intensity. This sensor supports high-precision light intensity measurement (with a maximum resolution of 0.5 lx), and communicates via the I2C interface.
## Key Features 

- Measurement range: 1 - 65535 lx
- Accuracy range: 0.5 - 4 lx (optional)
- Low current (120 μA)
- I2C interface (address 0x23)
- 50Hz/60Hz light source noise suppression
- Digital output (no AD conversion required)
- Temperature-dependent low

## Quick Start Guide 

### Sample Code 
```python
from machine import I2C
from bh1750 import Bh1750

# Initialize I2C (taking EC600U as an example) 
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
# Initialize sensors 
sensor = Bh1750(i2c_dev)

# Activate the sensor 
sensor.on()

# Set measurement mode (highest accuracy) 
sensor.set_measure_mode(CONTI_H_MODE2)

# Read the ambient light value 
light_level = sensor.read()
print("Light intensity:", light_level, "lx") 

# Turn off the sensor when the device is not in use 
sensor.off()
```


## API Interface Description 
**`Bh1750(i2c, dev_addr=0x23)`**

Construct the constructor and initialize the sensor. 

**Parameter Explanation:** 

- i2c: I2C object (initialized I2C instance)
- dev_addr: I2C device address (default 0x23, optional 0x5C) 

**`on()`**


Activate the sensor and prepare for the measurement. **`off()`**


Turn off the sensor and enter a low-power state (consuming only 1 μA of current). **`reset()`**


Reset the sensor and clear the historical data. **`set_measure_mode(mode=CONTI_H_MODE2)`**


Set the measurement mode. 

**Mode Description:**


- CONTI_H_MODE: Continuous High Resolution Mode (1 lx precision)
- CONTI_H_MODE2: Continuous High Resolution Mode 2 (0.5 lx precision) ※ Recommended
- CONTI_L_MODE: Continuous Low Resolution Mode (4 lx precision)
- ONE_H_MODE: Single High Resolution Mode (1 lx precision)
- ONE_H_MODE2: Single High Resolution Mode 2 (0.5 lx precision)
- ONE_L_MODE: Single Low Resolution Mode (4 lx precision) 

**`read()`**


Read the current light intensity value. 

**Return Value:** 

- Light intensity value (unit: lux lx)

## Typical Application
Automatic Backlight Adjustment 
```python
sensor = Bh1750(i2c_dev)
sensor.on()
sensor.set_measure_mode(CONTI_H_MODE2)

# Backlight Level Mapping Table 
brightness_levels = [
    (0, 10, 1),  # Extremely dark environment
    (10, 50, 2),  # Low light environment
    (50, 200, 3),  # Ordinary indoor environment
    (200, 500, 4),  # Bright indoor environment
    (500, 1000, 5),  # Bright illumination
    (1000, 3000, 6),  # Outdoor on cloudy day
    (3000, 20000, 7)  # Direct sunlight 
]


while True:
    light = sensor.read()

    # Determine the backlight level level = 0
    for min_lux, max_lux, lvl in brightness_levels:
        if min_lux <= light < max_lux:
        level = lvl
    break

set_backlight(level)  # Set the backlight intensity
utime.sleep(5)       # Check every 5 seconds 
```

Light intensity recorder 
```python
def light_logger(interval=60, duration=86400):
    '''Continuous recording of light intensity''' 
    sensor.on()
    sensor.set_measure_mode(ONE_H_MODE2)  # Single high-precision mode 
    log = []
    start_time = utime.time()

    while utime.time() - start_time < duration:
    # Read and store data 
    timestamp = utime.localtime()
    light_level = sensor.read()
    log.append((timestamp, light_level))

    # Enter a dormant state until the next measurement
    utime.sleep(interval - 0.1)  # Take measurement time compensation into account 
    # Log Processing and Data Storage 
    save_to_file(log)
    sensor.off()

    # Record 24-hour data (record every 5 minutes) 
    light_logger(interval=300, duration=86400)
```


## Common Issues Troubleshooting
- Sensor Position: Ensure it is not obstructed and that it measures the true ambient light.
- Light Source Interference: Avoid direct light shining on the sensor to prevent reading errors.
- Power Consumption Optimization: Turn off the sensor when it is not needed for frequent detections.
- Light Range: Beyond the sensor's range (>65535 lx), the maximum measurement value will be reached.
- Calibration Adjustment: During the first use, calibrate the reading accuracy under different lighting conditions.