# GL5516 Light Dependent Resistor (LDR) Driver Documentation

## Overview

This document describes how to use the GL5516 light dependent resistor (photoresistor) driver to measure ambient light levels by reading resistance values.

## Features

- Read raw voltage values from ADC
- Convert voltage to resistance values
- Simple API for light sensing applications

## Quick Start

### 1. Import Required Modules

```python
from misc import ADC
from gl5516 import Gl5516
import utime as time
```

### 2. Initialize the Sensor

```python
# Create ADC device instance
adc_device = ADC()

# Initialize GL5516 sensor on ADC channel 0
ldr_sensor = Gl5516(adc_device, ADC.ADC0)
```

### 3. Read Sensor Data

#### Read Resistance Value

```python
resistance = ldr_sensor.read()
print("Photoresistor resistance: {}Ω".format(resistance))
```

#### Read Raw Voltage Value

```python
voltage = ldr_sensor.read_volt()
print("Raw voltage: {}mV".format(voltage))
```

## API Reference

### `Gl5516(adc_dev, adcn)`

Constructor to initialize the GL5516 sensor.

**Parameters:**

- `adc_dev`: ADC device instance
- `adcn`: ADC channel number (e.g., `ADC.ADC0`)

### `read()`

Reads and returns the photoresistor resistance value in ohms (Ω).

**Returns:**

- Photoresistor resistance value (Ω)

### `read_volt()`

Reads and returns the raw voltage value from the ADC.

**Returns:**

- Voltage value in millivolts (mV)

## Example Application

```python
from misc import ADC
from gl5516 import Gl5516
import utime as time

# Initialize sensor
adc = ADC()
ldr = Gl5516(adc, ADC.ADC0)

# Continuous light monitoring
while True:
    resistance = ldr.read()
    voltage = ldr.read_volt()
    
    print("Light Level - Resistance: {}Ω, Voltage: {}mV".format(resistance, voltage))
    
    if resistance > 10000:  # Dark condition
        print("Dark environment detected")
    elif resistance < 2000:  # Bright condition
        print("Bright environment detected")
    
    time.sleep(1)
```

## Technical Notes

1. The resistance calculation assumes a specific voltage divider circuit configuration with:
   - 4.7kΩ resistor (R1)
   - 40.2kΩ resistor (R2)
   - 3.3V supply voltage
2. For different circuit configurations, modify the `_voltage_to_resistance()` method accordingly.
3. The sensor response time is typically in milliseconds, making 1-second intervals suitable for most applications.
4. Typical resistance ranges:
   - Bright light: ~1kΩ
   - Darkness: ~100kΩ or more

## Troubleshooting

- If readings are unstable, check for proper connections and stable power supply
- Ensure the ADC channel is correctly configured
- Verify the voltage divider circuit matches the driver's assumptions

This driver provides a simple interface for light sensing applications using the GL5516 photoresistor, suitable for automatic lighting control, daylight detection, and other light-sensitive applications.