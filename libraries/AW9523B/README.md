AW9523 GPIO Expansion Driver Module 

"Class Reference" 

```python
from aw9523 import AW9523
```


Instantiation parameters 

| Name | Required | Type | Description | 
|---- |----|----|----|
| i2c_bus | Yes | I2C object | I2C bus object |
| int_pin | No | int | Interrupt pin number, default 1 |
| int_mode | No | int | Interrupt mode, default 0 |
| int_callback | No | function | Interrupt callback function |
| address | No | int | I2C device address, default 0x58 (keypad driver address) |

Port object 

```python
porta = Port(0, aw)  # Port A
portb = Port(1, aw)  # Port B 
```


**Main method:**

l reset()


Reset the AW9523 chip. 

Parameters: 

No

Return value: 

No

l pin(pin, mode=None, value=None, interrupt_enable=None)

Configure a single pin.

Parameters: 

| Name | Type | Description | 
|----|----|----|
| pin | int | Pin number (0-15) |
| mode | int | Mode: 0 = Output, 1 = Input |
| value | int | Output value: 0 = Low level, 1 = High level |
| interrupt_enable | int | Interrupt enable: 0 = Disable, 1 = Enable | 

Return value: 

When setting the value: None
When reading the value: Current pin level (0 or 1)

l read(pin)

Read the level of a single pin. 

Parameters:
| Name | Type | Description | 
|----|----|----|
| pin | int | Pin number (0-15) | 

Return value: 

0: Low level
1: High level 

Global attribute 

| Attribute | Type | Description | 
|----|----|----|
| mode | int | All pin modes (read/write) |
| interrupt_enable | int | All pin interrupt enable (read/write) |
| interrupt_flag | int | All pin interrupt flags (read-only) |
| gpio | int | All GPIO values (read/write) |