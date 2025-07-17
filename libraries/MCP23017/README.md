# MCP23017 I/O Expander Example Code Documentation

## Overview

This document describes how to use the MCP23017 I/O expander based on QuecPython for GPIO expansion and control. The MCP23017 is a 16-bit I/O expander that provides additional GPIO ports via I2C interface, suitable for various applications requiring I/O expansion.

## Hardware Connection

Before using the MCP23017 module, ensure the hardware is properly connected:

- I2C interface connection (SCL/SDA)
- VCC connected to 3.3V or 5V power supply (depending on module requirements)
- GND connected to ground
- A0/A1/A2 address selection pins (connected to GND or VCC as needed)
- RESET pin (typically connected to VCC)
- INT pin (optional interrupt function)

## Quick Start

### 1. Initialize the MCP23017 Module

```python
from machine import I2C
from usr import mcp23017

# Initialize I2C interface
i2c = I2C(I2C.I2C1, I2C.STANDARD_MODE)
# Initialize MCP23017 expander (default address 0x20)
mcp = mcp23017.Mcp23017(i2c)
print("MCP23017 module initialized")
```

### 2. Basic Functionality

#### Configure Input Pins

```python
# Configure GPIO0 as input mode
mcp.pin(0, mode=1)  # mode=1 means input
# Configure GPIO1 as input mode with pull-up resistor enabled
mcp.pin(1, mode=1, pullup=True)
```

#### Configure Output Pins

```python
# Configure GPIO2 as output mode and set high level
mcp.pin(2, mode=0, value=1)  # mode=0 means output
# Configure GPIO3 as output mode and set low level
mcp.pin(3, mode=0, value=0)
```

## Advanced Features

### 1. Port-Level Operations

```python
# Configure entire PORTA as output
mcp.porta.mode = 0x00  # 0=output
# Set all PORTA pins to high level
mcp.porta.gpio = 0xFF

# Configure entire PORTB as input with pull-up enabled
mcp.portb.mode = 0xFF  # 1=input
mcp.portb.pullup = 0xFF
```

### 2. Interrupt Functionality

```python
# Configure GPIO4 as input with interrupt enabled
mcp.pin(4, mode=1, interrupt_enable=1)

while True:
    # Check PORTA interrupt
    if mcp.porta.interrupt_flag:
        print("PORTA interrupt triggered")
        # Read pin state at interrupt
        captured = mcp.interrupt_captured_gpio(0)
        print(f"Captured value: {captured:08b}")
    
    # Check PORTB interrupt
    if mcp.portb.interrupt_flag:
        print("PORTB interrupt triggered")
        captured = mcp.interrupt_captured_gpio(1)
        print(f"Captured value: {captured:08b}")
    
    utime.sleep_ms(100)
```

## Class and Method Reference

**I2C [Reference](https://developer.quectel.com/doc/quecpython/API_reference/en/peripherals/machine.I2C.html)**

### `Mcp23017` Class

#### Constructor

```python
Mcp23017(i2c, address=0x20, bank=1)
```

- `i2c`: I2C bus object
- `address`: Device I2C address (default 0x20)
- `bank`: Register bank mode (0=alternate, 1=sequential)

#### Main Methods

- `pin(pin, **kwargs)`: Configure a single pin
  - `pin`: Pin number (0-15)
  - `mode`: Direction (0=output, 1=input)
  - `value`: Output value (0/1)
  - `pullup`: Pull-up enable (True/False)
  - `interrupt_enable`: Interrupt enable (0/1)
- `interrupt_triggered_gpio(port)`: Get GPIO that triggered interrupt
- `interrupt_captured_gpio(port)`: Get interrupt captured value

#### Port Attributes

- `porta`: PORTA port object
- `portb`: PORTB port object

### `Port` Class (porta/portb)

#### Main Attributes

- `mode`: Port direction (0=output, 1=input)
- `pullup`: Pull-up enable
- `gpio`: GPIO value
- `interrupt_flag`: Interrupt flag (read-only)
- `interrupt_captured`: Interrupt captured value (read-only)

## Example Code

```python
from machine import I2C
from usr import mcp23017
import utime

def mcp23017_test():
    # Initialize I2C and MCP23017
    i2c = I2C(I2C.I2C1, I2C.STANDARD_MODE)
    mcp = mcp23017.Mcp23017(i2c, address=0x20)
    
    # Basic pin configuration
    mcp.pin(0, mode=1)  # GPIO0 input
    mcp.pin(1, mode=1, pullup=True)  # GPIO1 input with pull-up
    mcp.pin(2, mode=0, value=1)  # GPIO2 output high
    mcp.pin(3, mode=0, value=0)  # GPIO3 output low
    
    # Port operation example
    mcp.porta.mode = 0x0F  # Lower 4 bits input, upper 4 bits output
    mcp.porta.gpio = 0xF0  # Upper 4 bits output high
    
    # Interrupt example
    mcp.pin(4, mode=1, interrupt_enable=1)
    
    while True:
        if mcp.porta.interrupt_flag:
            print("Interrupt triggered!")
            print("Captured value:", mcp.interrupt_captured_gpio(0))
        utime.sleep_ms(100)

if __name__ == "__main__":
    mcp23017_test()
```

## Notes

1. Ensure I2C address is configured correctly (A0/A1/A2 pin states)
2. Do not drive high-current loads directly from output pins
3. Interrupt pins require proper pull-up/down resistor configuration
4. Note the impact of register bank mode (bank parameter) on register addresses
5. Input pins should preferably have pull-up or pull-down resistors enabled

## Troubleshooting

1. **Communication failure**:
   - Check I2C connections and address
   - Verify power supply voltage
   - Confirm RESET pin state
2. **Interrupt not working**:
   - Check INT pin connection
   - Verify interrupt configuration parameters
   - Confirm interrupt polarity settings
3. **Abnormal pin states**:
   - Check mode configuration (input/output)
   - Verify pull-up resistor settings
   - Check for short circuits or overloads

## Register Reference

| Register | Address | Description             |
| :------- | :------ | :---------------------- |
| IODIR    | 0x00    | I/O Direction           |
| IPOL     | 0x01    | Input Polarity          |
| GPINTEN  | 0x02    | Interrupt Enable        |
| DEFVAL   | 0x03    | Default Value           |
| INTCON   | 0x04    | Interrupt Control       |
| IOCON    | 0x05    | Configuration           |
| GPPU     | 0x06    | Pull-up Resistor Enable |
| INTF     | 0x07    | Interrupt Flag (RO)     |
| INTCAP   | 0x08    | Interrupt Capture (RO)  |
| GPIO     | 0x09    | General Purpose I/O     |
| OLAT     | 0x0A    | Output Latch            |