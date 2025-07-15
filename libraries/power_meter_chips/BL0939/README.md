# BL0939 Electric Energy Metering Chip Sample Code Description Document

## Overview

This document explains how to use the BL0939 energy measurement chip driver interface provided by Quectel. The BL0939 is a high-precision energy measurement chip capable of measuring AC voltage, current (dual-channel), power, and other parameters.

------

## Quick Start

### 1. Initialize the BL0939 Object

```python
from bl0939 import Bl0939

# Parameters: port=SPI port number (default: 1), mode=SPI mode (default: 1), clk=clock frequency (default: 0)
bl0939 = Bl0939(port=1, mode=1, clk=0)
```

### 2. Read Measurement Data

```python
# Read all parameters (Channel A current, Channel B current, voltage)
ia, ib, vol = bl0939.read()

# Read parameters individually  
current_a = bl0939.current_a  # Channel A current (RMS)  
current_b = bl0939.current_b  # Channel B current (RMS)  
voltage = bl0939.voltage      # Voltage (RMS)  
```

------

## Detailed API Reference

### Class `Bl0939`

#### Constructor

```python
Bl0939(port=1, mode=1, clk=0)
```

- **Parameters**:
  - `port`: SPI port number (default: 1).
  - `mode`: SPI mode (default: 1).
  - `clk`: SPI clock frequency (default: 0).
- **Function**: Initializes the SPI interface and resets the chip.

------

#### Methods

##### `read()`

```python
read() -> (int, int, int)
```

- **Returns**: A tuple `(Channel A current, Channel B current, Voltage)`.
- **Function**: Reads all measurements in a single call.

##### `reset()`

```python
reset()
```

- **Function**: Resets the chip (soft reset).

------

#### Properties

##### `current_a`

```python
current_a -> int
```

- **Returns**: Channel A current (RMS) (raw register value).
- **Note**: Must be converted to actual current (e.g., mA/A) based on the hardware circuit.

##### `current_b`

```python
current_b -> int
```

- **Returns**: Channel B current (RMS) (raw register value).

##### `voltage`

```python
voltage -> int
```

- **Returns**: Voltage (RMS) (raw register value).
- **Note**: Must be converted to actual voltage (e.g., V) based on the voltage divider circuit.

------

## Example Code

### Continuous Data Reading

```python
import utime
from bl0939 import Bl0939

bl0939 = Bl0939(port=1)

for i in range(10):
    ia, ib, vol = bl0939.read()
    print("Channel A Current: {}, Channel B Current: {}, Voltage: {}".format(ia, ib, vol))
    utime.sleep(1)
```

### Output Explanation

- The output values are raw register data and must be converted to physical quantities:
  - **Current Conversion**:
    `Actual Current = Register Value × (Shunt Resistor Ratio / Calibration Factor)`
  - **Voltage Conversion**:
    `Actual Voltage = Register Value × (Voltage Divider Ratio / Calibration Factor)`

------

## Notes

1. **SPI Configuration**: Ensure the SPI port, mode, and clock frequency match the hardware.
2. **Calibration**: Calibrate scaling factors (e.g., pulse constant) for accurate measurements.
3. **Isolation Design**: Use optocouplers or transformers when measuring high voltage.
4. **Unit Conversion**: Register values are unsigned integers; convert them to real-world units as per the datasheet.

------

## Troubleshooting

- **SPI Communication Failure**: Check wiring (CS/CLK/MOSI/MISO) and port configuration.
- **Abnormal Data**: Verify shunt resistor/voltage divider parameters.

For further assistance, refer to the BL0939 datasheet or contact Quectel technical support.