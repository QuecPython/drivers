# TM1650 Digital Tube Driver Documentation
## Overview 

This document explains how to use the TM1650 digital tube driver module to control the display of a 4-digit 7-segment digital tube. This driver supports the display of numbers, letters, symbols, as well as advanced functions such as brightness control and loop display.
## Key Features 

- Supports independent control of 4-digit digital tubes
- Displays numbers, letters and common symbols
- Supports decimal point display
- Brightness control switch
- Loop display function
- Clear screen and full display function
- Simple and user-friendly API interface

## Quick Start
### 1. Initialize the Digital Tube 
```python
from machine import Pin
from tm1650 import Tm1650


# Initialize the digital display (DIO = GPIO13, CLK = GPIO12) 
tube = Tm1650(dio=Pin.GPIO13, clk=Pin.GPIO12)
```
2. Basic Display Operations 
```python
# Turn on the digital tube 
tube.on()

# Display numbers 
tube.show_num(1234)

# Display String 
tube.show_str("HELL")

# Display a number with decimal points
tube.show_num(56.78)  # Displays "56.78" 

# Turn off the digital display panel 
tube.off()
```

## API Interface Description 

**`Tm1650(dio=None, clk=None)`**


Constructor, initializes the digital tube. 

**Parameter Description:**


- dio: Data pin (default: GPIO10)
- clk: Clock pin (default: GPIO13) 

**`on()`**


Turn on the digital tube display. 

**`off()`**


Turn off the digital display. 

**`all_clear()`**


Clear all the digital tube displays. 

**`clear_bit(bit)`**


Clear the digital tube display at the specified position. 

**Parameter Description:**


- bit: Position of the digital tube (1-4) 

**`all_show()`**


All the digital tubes are lit up (for testing purposes). 

**`show_num(num)`**


Display the numbers. 

**Parameter Description:**


- num: The number to be displayed (-999 to 9999) 

**`show_str(st)`**


Display the string. 

**Parameter Description:**


- st: The string to be displayed (up to 4 characters) 

**`show_dp(bit=1)`**


Display the decimal point at the specified location. 

**Parameter Description:**


- bit: Decimal point position (1-4) 

**`circulate_show(st)`**


Display the string in a loop. 

**Parameter Description:**


- st: The string to be displayed in a loop (recommending a maximum length of 12 characters)

## Application Example
Temperature Display Application 
```python
def display_temperature(temp):
    # Display temperature value 
    if temp >= 0:
        tube.show_num(int(temp * 100))  # Display with two decimal places
        tube.show_dp(3)  # Display decimal point at the third position 
    else:
        tube.show_num(int(temp))  # Negative numbers display only the integer part 

# Example Usage 
tube = Tm1650(Pin.GPIO13, Pin.GPIO12)
tube.on()

while True:
    temperature = read_temperature_sensor()  # A hypothetical function for reading the temperature sensor 
    display_temperature(temperature)
    utime.sleep(1)
```
Countdown function 
```python
def countdown(seconds):
    tube.on()
    for i in range(seconds, -1, -1):
        tube.show_num(i)
        utime.sleep(1)
    tube.show_str("END")
    utime.sleep(2)
    tube.off()

# 10-second countdown 
countdown(10)
```


## Common Issues Troubleshooting 

- The digital tube is not lit up.
    - The power supply is not connected.
    - The function "on()" has not been called.
    - There is an error in initializing the pins.
- Some segments are not lit up.
    - The hardware is damaged.
    - The segment mapping is incorrect.
    - The driving current is insufficient.
- The display has garbled characters.
    - The characters are not in the mapping table.
    - There is an error in data transmission.
- The brightness cannot be adjusted.
    - The control command is incorrect.
    - The brightness register is not configured.