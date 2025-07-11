# BH1750(gy-302)


**Class Reference: ** 

```python
from BH1750 import Bh1750
```


**Instantiation Parameters:** 

| Name     | Required | Type   | Description | 
| -------- | ---- | ------- | ---- |
| I2C      | Yes  | I2C object |      |
| Device address | No  | int     | 0x23 | 

```python
i2c_obj=I2C(I2C.I2C1,I2C.STANDARD_MODE)
bh1750 = Bh1750(i2c_obj)
```


**Interface Function: ** 

l **on(), off(), reset()**


Activate the sensor, put it in an inactive state, and reset the sensor. 

Parameters: 

No. 

Return value: 

No. 

l **set_measure_mode(mode)**


Set the measurement mode, for continuous measurement or single measurement, with different levels of accuracy. 

Parameters: 

| Name | Required | Type | Description | 
| ---- | ---- | ---- | ------------------------- |
| mode | No  | int  | Default: 0.5lx precision;<br />0x10: (1lx precision)<br />0x13: (0.5lx precision) | 

Return value: 

No


l **read ()**


Read the illuminance value. 

Parameters: 

No. 

Return value: 

| Name | Type | Description | 
| ---- | ---- | -------- |
| lux  | int  | Illuminance value |