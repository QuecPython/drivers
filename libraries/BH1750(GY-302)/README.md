# BH1750(gy-302)

**类引用：**

```python
from BH1750 import Bh1750
```

 

**实例化参数：**

| 名称     | 必填 | 类型    | 说明 |
| -------- | ---- | ------- | ---- |
| I2C      | Yes  | I2C object |      |
| Device address | No  | int     | 0x23 | 

```python
i2c_obj=I2C(I2C.I2C1,I2C.STANDARD_MODE)
bh1750 = Bh1750(i2c_obj)
```

**接口函数：**

l **on(), off(), reset()**


Activate the sensor, put it in an inactive state, and reset the sensor. 

Parameters: 

No. 

Return value: 

No. 

l **set_measure_mode(mode)**

​	设置测量模式，持续测量或单次测量，不同精度。

参数：

| 名称 | 必填 | 类型 | 说明                                                         |
| ---- | ---- | ---- | ------------------------------------------------------------ |
| mode | 否   | int  | 默认0.5lx精度；<br />0x10：（1lx精度）<br />0x13：（0.5lx精度） |

No


l **read ()**


Read the illuminance value. 

Parameters: 

No. 

Return value: 

| Name | Type | Description | 
| ---- | ---- | -------- |
| lux  | int  | Illuminance value |