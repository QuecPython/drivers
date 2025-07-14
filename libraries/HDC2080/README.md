# HDC2080

**Class reference:**

```python
from hdc2080 import Hdc2080
```



**Instance parameters:**

| Name     | Required | Type | Description            | 
| -------- | ---- | ---- | ----------------------- |
| i2c_obj  | Yes  | int  | I2C object                |
| dev_addr | No   | int  | I2C slave device address, default 0x40 |

```python
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
hdc = Hdc2080(i2c_dev)
```

**Interface function:**

l **read()**

Read the register value and convert it into humidity and temperature. 

Parameters:

No.

Return value:

| Name                   | Type  | Description | 
| ---------------------- | ----- | ---------- |
| (humidity, temperature) | tuple | Humidity, Temperature |

l **reset()**

Reset hdc1080.

Parameters:

No.

Return value:

No.