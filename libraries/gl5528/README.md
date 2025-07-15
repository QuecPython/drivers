# GL5528 Photoresistor Sensor Driver Documentation

## Overview

This document describes the usage of the GL5528 photoresistor sensor driver, which measures ambient light intensity and converts it to both resistance values and illuminance (lux) levels.

## Key Features

- Read raw ADC voltage values
- Convert voltage to resistance values
- Map resistance values to illuminance (lux) using predefined lookup table
- Provides both resistance and illuminance outputs

## Quick Start Guide

### 1. Import Required Modules

```python
from misc import ADC
from gl5528 import Gl5528
import utime as time
```

### 2. Initialize the Sensor

```python
# Create ADC device instance
adc_device = ADC()

# Initialize GL5528 sensor on ADC channel 0
ldr_sensor = Gl5528(adc_device, ADC.ADC0)
```

### 3. Read Sensor Data

#### Read Resistance and Illuminance

```python
resistance, lux = ldr_sensor.read()
print(f"Photoresistor resistance: {resistance}Ω, Illuminance: {lux}lux")
```

#### Read Raw Voltage Value

```python
voltage = ldr_sensor.read_volt()
print(f"Raw voltage: {voltage}mV")
```

## API Reference

### `Gl5528(adc_dev, adcn)`

Constructor for initializing the GL5528 sensor.

**Parameters:**

- `adc_dev`: ADC device instance
- `adcn`: ADC channel number (e.g., `ADC.ADC0`)

### `read()`

Reads and returns both photoresistor resistance and illuminance.

**Returns:**

- Tuple (resistance, lux)
  - resistance: Photoresistor value in ohms (Ω)
  - lux: Illuminance value (may be None if out of lookup table range)

### `read_volt()`

Reads and returns the raw ADC voltage value.

**Returns:**

- Voltage value in millivolts (mV)

### `r2i(resis)`

Converts resistance value to illuminance (lux).

**Parameters:**

- resis: Resistance value in ohms (Ω)

**Returns:**

- Illuminance value (lux) or None (if out of lookup table range)

## Example Application

```python
from misc import ADC
from gl5528 import Gl5528
import utime as time

# Initialize sensor
adc = ADC()
ldr = Gl5528(adc, ADC.ADC0)

# Continuous light monitoring
while True:
    resistance, lux = ldr.read()
    
    if lux:
        print(f"Current environment - Resistance: {resistance}Ω, Illuminance: {lux}lux")
    else:
        print(f"Current environment - Resistance: {resistance}Ω (Out of measurement range)")
    
    # Light-dependent control logic
    if lux and lux > 500:
        print("Bright environment detected")
    elif lux and lux < 100:
        print("Dim environment detected")
    
    time.sleep(1)
```

## Technical Specifications

1. **Resistance Calculation** based on specific voltage divider configuration:
   - 4.7kΩ resistor (R1)
   - 40.2kΩ resistor (R2)
   - 3.3V power supply
2. **Illuminance Conversion** uses predefined resistance-illuminance lookup table (o2i_table) with precise mapping for 400Ω-82kΩ range
3. **Typical Applications**:
   - Indoor light monitoring
   - Automatic lighting control
   - Ambient light sensing devices
4. **Measurement Range**:
   - Resistance range: ~400Ω-82kΩ
   - Illuminance range: 1-1300lux (depending on lookup table)

## Troubleshooting

1. **Unstable Readings**:
   - Check circuit connections
   - Ensure stable power supply
   - Avoid direct exposure to flickering light sources
2. **None Values Returned**:
   - Verify resistance is within 400Ω-82kΩ range
   - Check ADC configuration
3. **Accuracy Issues**:
   - Extend o2i_table for higher precision
   - Consider using higher precision ADC module

This driver provides complete interface for GL5528 photoresistor, particularly suitable for applications requiring both resistance and illuminance measurements. The included lookup table enables direct conversion from resistance to standard lux values for convenient light intensity evaluation.
