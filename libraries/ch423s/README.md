# CH423 GPIO Expander Driver Documentation

## 1. Overview

This script provides a driver class `Ch423s` for the CH423 series I2C interface GPIO expander based on QuecPython. The CH423 is an I2C bus-controlled general-purpose I/O port expander that supports 8-bit/16-bit GPIO input/output configuration, open-drain output mode, input interrupt functions, etc. This driver class encapsulates the underlying I2C communication protocol and upper-layer function calls of the CH423, facilitating quick control of the CH423 chip in a QuecPython environment.

## 2. Core Class and Method Details

### 2.1 Class Initialization `__init__(self, clk, dio)`

**Function**: Initializes the CH423 chip, configures the clock pin (SCL) and data pin (SDA), and completes the chip reset.
​**​Parameters​**:

- `clk`: Clock pin (SCL) connected to the CH423 (e.g., `Pin.GPIO12`), must be of type `machine.Pin`.
- `dio`: Data pin (SDA) connected to the CH423 (e.g., `Pin.GPIO13`), must be of type `machine.Pin`.

**Description**:
During initialization, the system parameter command `CH423_SYS_CMD` (0x48) is sent via I2C, and the initial value is set to 0x00 to complete the basic configuration of the chip.

### 2.2 Basic I2C Communication Methods (Internal Use)

The following methods are low-level implementations of the I2C protocol and typically do not need to be called directly by users:

#### `_start_signal(self)`

Generates the I2C start signal: The data line is pulled high first, then the clock is pulled high, followed by the data line being pulled low, and finally the clock is pulled low to complete the start condition.

#### `_stop_signal(self)`

Generates the I2C stop signal: The clock is pulled low, then the data line is pulled low, followed by the clock being pulled high, and finally the data line is pulled high to complete the stop condition.

#### `ack(self, is_ack)`

Sends an ACK/NACK signal: `is_ack=True` indicates sending an ACK (data line pulled low), `False` indicates NACK (data line remains high).

#### `_wait_ack(self)`

Waits for the slave device to return an ACK response: Detects the data line level, and if a timeout occurs (>2000 loops), an error is reported, and communication is stopped.

#### `_write_byte(self, data)`

Sends a single byte of data via I2C: Sends data from the most significant bit to the least significant bit, pulling the clock high after each bit is sent and waiting for an ACK.

#### `_read_byte(self)`

Reads a single byte of data via I2C: Reads the data line level bit by bit when the clock is high, and finally sends an ACK signal.

### 2.3 Register Read/Write Methods (Internal Use)

#### `_read_reg(self, cmd)`

Reads the value of the register corresponding to the specified command: Completes the process via the I2C start signal → send command → read data → stop signal.

#### `_write_reg(self, cmd, val)`

Writes a value to the register corresponding to the specified command: Completes the process via the I2C start signal → send command → send value → stop signal.

### 2.4 Core Functional Methods

#### `reset(self)`

**Function**: Resets the CH423 chip to restore default configuration.
​**​Implementation​**: Calls `_write_reg` to write 0x00 to the system parameter command register (`CH423_SYS_CMD`).

#### `config(self, dir=GPIO_IN, int=0, odr=0)`

**Function**: Configures the GPIO direction, input interrupt enable, and open-drain output enable.
​**​Parameters​**:

- `dir`: GPIO direction (0=input, 1=output).
- `int`: Input level change interrupt enable (0=disable, 1=enable).
- `odr`: Open-drain output enable (0=push-pull output, 1=open-drain output).

**Description**:
Configures the system parameter register (`CH423_SYS_CMD`) to set the parameters. Parameters must be 0 or 1; otherwise, -1 is returned.

#### `gpio_pin(self, pin, value=1)`

**Function**: Sets the level of a specific GPIO pin (only valid when GPIO is in output mode).
​**​Parameters​**:

- `pin`: Pin number (0-7, corresponding to IO0-IO7).
- `value`: Target level (0=low level, 1=high level).

**Description**:
Reads the current GPIO state (`read_gpio`), modifies the corresponding bit according to `value`, and writes it back to (`CH423_SET_IO_CMD`).

#### `gpo_h(self, value)`

**Function**: Sets the overall output level of the high 8-bit GPIO (IO8-IO15) (only valid when GPIO is in output mode).
​**​Parameters​**:

- `value`: 8-bit value (0-255), where each bit corresponds to the level of IO8-IO15 (1=high, 0=low).

**Description**:
Directly writes the value to the high 8-bit output command register (`CH423_OC_H_CMD`).

#### `gpo_l(self, value)`

**Function**: Sets the overall output level of the low 8-bit GPIO (IO0-IO7) (only valid when GPIO is in output mode).
​**​Parameters​**:

- `value`: 8-bit value (0-255), where each bit corresponds to the level of IO0-IO7 (1=high, 0=low).

**Description**:
Directly writes the value to the low 8-bit output command register (`CH423_OC_L_CMD`).

#### `gpio(self, value)`

**Function**: Sets the overall output level of the 8-bit GPIO (IO0-IO7) (only valid when GPIO is in output mode).
​**​Parameters​**:

- `value`: 8-bit value (0-255), where each bit corresponds to the level of IO0-IO7 (1=high, 0=low).

**Description**:
Equivalent to `gpo_l`, directly writes the value to the low 8-bit output command register.

#### `read_gpio(self)`

**Function**: Reads the current state of the GPIO pins (valid in both input and output modes).
​**​Return Value​**: 8-bit value (0-255), where each bit corresponds to the state of IO0-IO7 (1=high, 0=low).
​**​Description​**:

- If `BIT_IO_OE` (bit 0 of `CH423_SYS_CMD`) is 0 (push-pull input mode), the actual input level of the pin is read.
- If `BIT_IO_OE` is 1 (push-pull output/open-drain output mode), the output latch value of the pin is read (not the real-time level).

## 3. Usage Examples

### Example 1: Initialization and Basic Output

```python
from machine import Pin
import utime
from ch423_driver import Ch423s  # Assuming the script is saved as ch423_driver.py

# Initialize CH423, using GPIO12 (SCL) and GPIO13 (SDA)
ch423 = Ch423s(Pin.GPIO12, Pin.GPIO13)
utime.sleep(1)  # Wait for initialization to complete

# Configure all GPIOs as output mode (dir=1)
ch423.config(dir=1)
print("GPIO has been set to output mode")

# Loop to light up pin 5 (IO5)
for _ in range(10):
    ch423.gpio_pin(pin=5, value=1)  # IO5 outputs high level
    utime.sleep(1)
    print("Current GPIO state:", bin(ch423.read_gpio()))  # Print all GPIO states (binary)
    ch423.gpio(0x00)  # All GPIOs output low level
    utime.sleep(1)
    print("Current GPIO state:", bin(ch423.read_gpio()))  # Print all GPIO states (binary)
```

### Example 2: Open-Drain Output Mode

```python
# Configure all GPIOs as open-drain output mode (odr=1)
ch423.config(odr=1)
print("GPIO has been set to open-drain output mode")

# Set high 8-bit GPIO to 0x0F (IO8-IO11 output high, IO12-IO15 output low)
ch423.gpo_h(0x0F)
# Set low 8-bit GPIO to 0xF0 (IO4-IO7 output high, IO0-IO3 output low)
ch423.gpo_l(0xF0)
utime.sleep(1)
print("Open-drain output state:", bin(ch423.read_gpio()))  # Output latch value (not real-time level)
```