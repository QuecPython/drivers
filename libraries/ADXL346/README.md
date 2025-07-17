# ADXL346 Three-Axis Acceleration Sensor Driver Documentation
## Overview 

This document explains how to use the ADXL346 three-axis acceleration sensor driver module to read the motion data of the device via the I2C interface, including the values of the three-axis acceleration and the ability to configure various motion detection interrupts. 

## Main Features 

- Read the acceleration values of X/Y/Z axes
- Set the measurement range (2g/4g/8g/16g)
- Configure 5 types of motion detection interrupts:
  - Single click (Single tap)
  - Double click (Double tap)
  - Activity detection (Activity)
  - Inactivity detection (Inactivity)
  - Free-fall (Free-fall)
- Real-time interrupt status detection

## Quick Start
### 1. Import Required Modules 
```python
from machine import I2C
from adxl346 import Adxl346
import utime
```
### 2. Initialize the sensors 

```python
# Initialize the ADXL346 sensor on the I2C1 bus, with the device address set to 0x53 
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
accel_sensor = Adxl346(i2c_dev)
```


### 3. Set the measurement range 

```python
# Set the range (optional: 2g/4g/8g/16g)
accel_sensor.set_range(Adxl346.range_8g)  # Set to 8g range 
```


### 4. Read sensor data
#### Read the values of the three-axis acceleration 

```python
x, y, z = accel_sensor.read_acceleration()
print("Acceleration values: X={}g, Y={}g, Z={}g".format(x, y, z)) 
```


Configure and use interrupts (taking double-click detection as an example) 

```python
# Enable Double-click Detection Interruption 
accel_sensor.int_enable(Adxl346.DOUB_TAP_INT)

# Wait for and handle interrupt events 
accel_sensor.process_double_tap()
print("Detecting double-click event!" )

# Read the current acceleration value 
x, y, z = accel_sensor.read_acceleration()
```

## API Interface Description 

### **`Adxl346(i2c, dev_addr=0x53)`**


Construct the constructor and initialize the ADXL346 sensor. 

**Parameter Description:**


- i2c: I2C device instance
- dev_addr: Sensor I2C address (default 0x53) 

### **`set_range(range=range_2g)`**


Set the acceleration measurement range. 

**Parameter Explanation:** 

- range: Range selection (range_2g, range_4g, range_8g, range_16g) 

### **`read_acceleration()`**


Read the values of the three-axis acceleration. 

**Return Value: ** 

- (x, y, z) Three-axis acceleration values, with units of g 

### **`int_enable(int_code, **kwargs)`**


Enable the specific interrupt function. 

**Parameter Explanation:** 

- int_code: Interrupt Type Selection:
    - SING_TAP_INT: Single Click
    - DOUB_TAP_INT: Double Click
    - ACT_INT: Activity Detection
    - INACT_INT: Inactivity Detection
    - FF_INT: Free Fall
- kwargs: Interrupt Parameters (refer to the technical description) 

### Interrupt handling function. 

Wait for a specific interrupt to occur: 

- process_single_tap(): Single click
- process_double_tap(): Double click
- process_act(): Activity detection
- process_inact(): Inactivity detection
- process_ff(): Free fall

## Application Examples 

Basic data reading 

```python
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
adxl = Adxl346(i2c_dev)
adxl.set_range(Adxl346.range_8g)


while True:
    x, y, z = adxl.read_acceleration()
    print("X={:.3f}g, Y={:.3f}g, Z={:.3f}g".format(x, y, z))
    utime.sleep(1)
```


Double-click detection application 
```python
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
adxl = Adxl346(i2c_dev)
adxl.int_enable(Adxl346.DOUB_TAP_INT)


while True:
    # Waiting for double-click event 
    adxl.process_double_tap()

    # After the incident occurred, data was 
    read. x, y, z = adxl.read_acceleration()
    print("Double-click event! Current acceleration: X={}g, Y={}g, Z={}g".format(x, y, z)) 
```


Free fall detection 
```python
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
adxl = Adxl346(i2c_dev)
adxl.int_enable(Adxl346.FF_INT, ff_thr=0x06, ff_time=0x15)


while True:
    if adxl.process_ff():
    printf("Detecting free fall event!" )
```

## Technical Description
### 1. Range and Resolution 

| Range | Resolution | Maximum Measurement Value | |----|----|----|
|2g |0.004g| ±2g|
|4g |0.008g| ±4g|
|8g |0.016g|  ±8g|
|16g |0.032g| ±16g|
### 2. Interruption Parameter Configuration 

Each interrupt type supports the following parameters:
- Single click/double click:
  - tap_thr: Trigger threshold (default 0x30)
  - dur: Duration (default 0x20)
  - tap_axis: Detection axis (default 0x07 for all axes) 

- Free fall: 

    - ff_thr: Trigger threshold (default: 0x06)
    - ff_time: Time window (default: 0x15) 

- Activity Detection: 

    - act_thr: Trigger threshold (default: 0x03)
    - act_axis: Detection axis (default: 0xF0) 

- Static detection: 

    - inact_thr: Trigger threshold (default: 0x03)
    - inact_axis: Detection axis (default: 0x0F)
    - inact_time: Duration of inactivity (default: 3) 

### 3. Interruption Response Characteristics 

- All interruption detection response times are at the millisecond level.
- It is recommended to retain a delay of at least 20ms in the main loop (utime.sleep_ms(20)).
- In actual applications, the detection threshold parameters should be adjusted according to the requirements. 

Common Issues Troubleshooting 

- Check the I2C wiring and address (default 0x53)
- Ensure the sensor is properly powered (3.3V)
- Confirm that the interrupt pin is correctly connected and configured
- Confirm that there is no address conflict on the I2C bus 

This driver provides a complete interface for motion detection applications using the ADXL346 acceleration sensor, and is applicable to scenarios such as posture detection, impact detection, and free fall detection.