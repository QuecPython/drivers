# RDA5807 FM Radio Module Driver Documentation

## Overview

This document provides usage instructions for the Python driver of the RDA5807 FM radio module. The driver communicates with the RDA5807 chip via I2C interface, offering complete FM radio control functionality.

## Key Features

- FM radio initialization and configuration
- Frequency setting and channel scanning
- Volume control and mute function
- Signal strength detection
- Bass boost adjustment

## Quick Start Guide

### 1. Hardware Connection

```python
# Define pin connections
rdaclk = Pin.GPIO2  # Clock line
rdadio = Pin.GPIO3  # Data line
```

### 2. Radio Initialization

```python
from machine import Pin
import RDA5807  # Assuming driver is saved as RDA5807.py

# Create radio instance
radio = RDA5807.RDA5807(rdaclk=Pin.GPIO2, rdadio=Pin.GPIO3)

# Initialize radio
radio._rda_init()
print("Radio initialization complete")
```

### 3. Basic Operations

```python
# Enable FM function
radio.fm_enable(1)

# Set volume (0-15)
radio.vol_set(10)

# Scan and play channel
current_freq = radio.seek_channel()
print("Current frequency: %d MHz" %current_freq)
```

## API Reference

### Core Methods

#### `_rda_init()`

Initialize RDA5807 chip with default parameters

#### `fm_enable(flag)`

Enable/disable FM function

- `flag`: 1=enable, 0=disable

#### `vol_set(vol)`

Set volume level

- `vol`: Volume level (0-15)

#### `mute_set(mute)`

Set mute

- `mute`: 1=mute, 0=unmute

#### `bass_set(bass)`

Set bass boost

- `bass`: 1=enable, 0=disable

### Channel Control

#### `freq_set(freq)`

Set specific frequency

- `freq`: Frequency value (in 10kHz units), range 6500-10800 (87.0-108.0MHz)

#### `seek_channel()`

Auto scan and lock channel, returns found frequency (MHz)

#### `next_chanl()`

Scan and play next available channel

#### `seek_direction(dir)`

Set scan direction

- `dir`: 1=up, 0=down

### Signal Detection

#### `rssi_get()`

Get current signal strength (0-127)

#### `seekth_set(rssi)`

Set auto-scan signal threshold

- `rssi`: Threshold (0-15), lower values find more stations

## Usage Examples

### Basic Radio Functionality

```python
# Initialization
radio = RDA5807.RDA5807(rdaclk=Pin.GPIO2, rdadio=Pin.GPIO3)
radio._rda_init()

# Enable radio
radio.fm_enable(1)
radio.vol_set(12)  # Set medium volume

# Scan and play channel
current_freq = radio.seek_channel()
print("Now playing: %d MHz" %current_freq)

# Switch to next channel after 5 seconds
time.sleep(5)
radio.next_chanl()
```

### Signal Strength Monitoring

```python
while True:
    strength = radio.rssi_get()
    print("Current signal strength: ",strength)
    if strength < 30:
        print("Weak signal, rescanning...")
        radio.seek_channel()
    time.sleep(2)
```

## Important Notes

1. Ensure correct hardware connections, especially I2C pins
2. Wait at least 30ms after initialization before other operations
3. Frequency range is 87.0-108.0MHz (6500-10800)
4. Volume range is 0-15, recommended initial setting 8-10
5. Channel scanning may take several seconds

## Troubleshooting

- If initialization fails, check I2C lines and power supply
- If no sound, check mute setting and volume level
- For poor signal, try adjusting antenna position or lowering scan threshold