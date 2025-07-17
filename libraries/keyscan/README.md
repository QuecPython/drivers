# Keyboard Driver Module Documentation
## Overview 

This document explains how to use the key driver module to implement various key detection functions, including single-key press, continuous key detection, short press/long press recognition, etc. The driver achieves efficient key detection through the interrupt mechanism and supports the management of multiple keys simultaneously and the handling of complex events.
## Key Features 

- Supports single-key press detection and continuous-key press detection modes
- Supports independent handling of key press/release events
- Supports long-key recognition (with customizable long-press duration)
- Built-in hardware debouncing mechanism
- Efficient event handling through interrupt-driven approach
- Parallel management of multiple keys
- Thread-safe callback mechanism

## Quick Start
### 1. Import Required Modules 
```python
from machine import Pin
from key_driver import Key
```
### 2. Define the key event handling function 
```python
def key_event_handler(key, event):
    if event == Key.Event.PRESSED:
        print("The button with pin number {} has been pressed".format(key.pin)) 
    elif event == Key.Event.RELEASED:
        print("The button with pin {} was released for a duration of {} seconds.".format(key.pin, key.sec)) 
    elif event == Key.Event.LONG_PRESSED:
        print("Press key {} for {} seconds".format(key.pin, key.sec)) 
```
### 3. Initialize the key object 
```python
# Configure K1 button (GPIO4)
# Working mode: Continuous detection
# Decoupling time: 20ms
# Pressing level: Low level (0)
# Attention event: Press and release 
k1 = Key(
    pin=Pin.GPIO4,
    work_mode=Key.WorkMode.CONTINUOUS,
    debounse_ms=20,
    level_on_pressed=0,
    cared_event=Key.Event.PRESSED | Key.Event.RELEASED,
    event_cb=key_event_handler
)
```
### 4. Run the main program 
```python
while True:
    # Main Program Logic 
    sleep_ms(100)
```

## API Interface Description 

**`Key(pin, work_mode, debounse_ms, level_on_pressed, cared_event, event_cb, long_press_event=[])`**


Construct the constructor to initialize the key object. 

**Parameter Description:**

- pin: GPIO pin number
- work_mode: Working mode
    - Key.WorkMode.ONE_SHOT: Single-shot key mode
    - Key.WorkMode.CONTINUOUS: Continuous detection mode
- debounce_ms: Debouncing time (milliseconds)
- level_on_pressed: Voltage level when the key is pressed
    - 0: Pressed state is low voltage
    - 1: Pressed state is high voltage
- cared_event: Combinations of events to be monitored
    - Key.Event.PRESSED: Key pressed event
    - Key.Event.RELEASED: Key released event
    - Key.Event.LONG_PRESSED: Long press event
- event_cb: Key event callback function
- long_press_event: Long press time settings (list of seconds) 

**`disable()`**


Disable key detection. 

**`enable()`**


Enable key detection.

## Application Example
Basic Key Press Detection 
```python
def key_handler(key, event):
    if event == Key.Event.PRESSED:
        print("Button pressed") 
    elif event == Key.Event.RELEASED:
        print("Button released") 

# Initialize key K1 
Key(
    pin=Pin.GPIO4,
    work_mode=Key.WorkMode.CONTINUOUS,
    debounse_ms=20,
    level_on_pressed=0,
    cared_event=Key.Event.PRESSED | Key.Event.RELEASED,
    event_cb=key_handler
)
```
Long press function implementation 
```python
def long_press_handler(key, event):
    if event == Key.Event.LONG_PRESSED:
        print("Long press function triggered. Duration: {} seconds".format(key.sec)) 
    if key.sec >= 5:
    print("Execute factory reset" )

# Configure the events for long press for 2 seconds and 5 seconds 
Key(
    pin=Pin.GPIO5,
    work_mode=Key.WorkMode.CONTINUOUS,
    debounse_ms=20,
    level_on_pressed=0,
    cared_event=Key.Event.PRESSED | Key.Event.RELEASED | Key.Event.LONG_PRESSED,
    event_cb=long_press_handler,
    long_press_event = [2, 5]  # Set the long press points to 2 seconds and 5 seconds. 
)
```
## Common Issues Troubleshooting
- Physical connection problem
- Severe jitter interference
- Incorrect handling of event callbacks