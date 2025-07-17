# AW9523 GPIO Expansion Chip Driver Documentation
## Overview 

This document explains how to use the AW9523 driver module to achieve GPIO expansion functionality. This chip expands 16 bidirectional GPIO pins through the I2C interface, supports independent configuration of input/output modes, and has a level change interrupt detection function. 

## Main Features
- Supports 16 bidirectional GPIO pins expansion
- Allows independent configuration of each pin as input/output mode
- Supports high/low level control (output mode)
- Supports pin status reading (input mode)
- Built-in edge detection function (rising/falling edge)
- Real-time callback notification of interrupt status

## Quick Start

### 1. Import Required Modules 

```python
from machine import I2C, ExtInt
from aw9523 import AW9523
from usr.common import create_thread
import utime
```


### 2. Initialize the sensors 
```python
# Create an instance of the I2C device (I2C1, standard mode) 
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)

# Define the interrupt callback function 
def int_callback(pin_data):
    pin, level = pin_data
    print("Pin {} has a level change! Current level: {}".format(pin, 'High' if level else 'Low')) 

# Initialize the AW9523 chip on the I2C0 bus (address 0x58, using pin 1 as the interrupt pin) 
expander = AW9523(
    i2c_bus=i2c_dev,
    int_pin = 1,                 # Interrupt pin number
    int_callback = int_callback  # Interrupt callback function 
    )
```


### 3. Configure GPIO pins 
```python
# Set pin 0 to output mode and set it to high level 
expander.pin(0, mode=0, value=1)

# Set pin 8 to input mode and enable interrupts 
expander.pin(8, mode=1, interrupt_enable=1)

# Set pin 9 to input mode and disable interrupts 
expander.pin(9, mode=1, interrupt_enable=0)
```


### 4. Read the pin status 
```python
# Read the current level state of pin 8 
level = expander.read(8)
print("Pin 8 current level: ".format('High' if level else 'Low')) 

# Read the status of all pins in batches 
all_pins_state = expander.gpio
print("All pin states: {}".format(bin(all_pins_state))) 
```

## API Interface Description 

### **`AW9523(i2c_bus, int_pin=1, int_mode=0, int_callback=None, address=0x58)`**


Constructor, initializing the AW9523 chip 

**Parameter Description:**


- i2c_bus: I2C bus instance
- int_pin: Interrupt detection pin number
- int_mode: Interrupt triggering mode
- int_callback: Interrupt callback function
- address: Device I2C address (0x58 or 0x5B) 

**`pin(pin, mode=None, value=None, interrupt_enable=None)`**


Configure the specified pin parameters 

**Parameter Explanation:**


- pin: Pin number (0-15)
- mode: Pin mode
    - 0: Output mode
    - 1: Input mode
- value: Output level value (valid in output mode)
    - 0: Low level
    - 1: High level
- interrupt_enable: Interrupt enable
    - 0: Disable interrupt
    - 1: Enable interrupt 

**`read(pin)`**


Read the level status of the specified pin 

**Parameter Explanation:**


- pin: Pin number (0-15) 

- Return value: 

    - 0: Low level
    - 1: High level 

Attribute accessor 

- mode: All pin mode status (16 bits)
- interrupt_enable: All pin interrupt enable status (16 bits)
- gpio: All pin level status (16 bits)

## Application Example
Basic GPIO Expansion Application 
```python
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
expander = AW9523(i2c_dev)

# Set pins 0 to 3 to output mode 
for i in range(4):
    expander.pin(i, mode=0, value=0)

# Set pins 8 to 11 to input mode 
for i in range(8, 12):
    expander.pin(i, mode=1, interrupt_enable=0)

while True:
    # Read the status of pins 8 to 1 
    for i in range(8, 12):
        state = expander.read(i)
        print("Pin {i} state: {state}".format(i, state))

    utime.sleep(1)
```
Interrupt detection application 
```python
def int_handler(pin_data):
    pin, level = pin_data
    print("Pin {} changed to {}".format(pin, level))

i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
expander = AW9523(i2c_dev, int_callback=int_handler)


# Set pins 4 to 7 as inputs and enable interrupts 
for i in range(4, 8):
    expander.pin(i, mode=1, interrupt_enable=1)

# Continuously perform other tasks 
while True:
    # Main Program Logic 
    utime.sleep(10)
```
LED Control Application 

```python
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
expander = AW9523(i2c_dev)

# Set pins 12 to 15 to output mode to control the 
LED led_pins = [12, 13, 14, 15]
for pin in led_pins:
    expander.pin(pin, mode=0, value=0)

# LED Waterfall Light Effect while True:
for pin in led_pins:
    expander.pin(pin, value=1)  # Turn on the LED 
    utime.sleep_ms(200)
    expander.pin(pin, value=0)  # Turn off the LED 
```

## Technical Description
### 1. Pin Mapping 

|Port|Pin Range|Register| 
|----|----|----|
|PORTA|0-7|0x00|
|PORTB|8-15|0x01|


### 2. Interruption Handling Mechanism 

- Interrupt triggered by using the hardware INT pin
- Interrupt triggered when the level changes
- Interrupt callback function format: callback([pin, level])
    - pin: Pin number that has changed (0-15)
    - level: Changed level (0: low/1: high) 

### 3. Configuration Options
| Configuration Type | Value Range | Description | 
|----|----|----|
| Pin Mode | 0/1 | 0 = Output, 1 = Input |
| Output Level | 0/1 | 0 = Low Level, 1 = High Level |
| Interrupt Enable | 0/1 | 0 = Disable, 1 = Enable |
| Interrupt Trigger Mode | 0/1 | 0 = Bi-directional Edge, 1 = Unidirectional Edge (Reserved) | 

### 4. I2C Address Explanation
| Device Type | I2C Address |
 |----|----|
|Button Driver|0x58|
|IO Expander|0x5B| 

Common Issues Troubleshooting 
- Check if the I2C connections are correct.
- Confirm if the I2C address is correct (0x58 or 0x5B).
- Ensure that the interrupt_enable is set to 1.
- Verify if the INT pin configuration is correct.
- Make sure there are no blocking operations on the interrupt line within the loop. 



This driver provides a complete control interface for the AW9523 GPIO expansion chip, and is suitable for various scenarios that require IO expansion.