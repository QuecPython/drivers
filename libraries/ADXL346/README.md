# adxl346


Default initialization for a 2G range. 

**Class Reference:** 

```python
from adxl346 import Adxl346
```


**Instantiation Parameters:** 

| Name     | Required | Type    | Description                        | 
| -------- | ---- | ------- | ----------------------------------- |
| I2C      | Yes  | I2C object | Such as I2C(I2C.I2C1, I2C.STANDARD_MODE) |
| Device address | No  | int     | Default: 0x53                        | 

```python
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
adxl = Adxl346(i2c_dev)
```


**Interface Function:**

l **set_range(range=0)**


Set the range. 

Parameters: 

| Name | Required | Type | Description | 
| ----- | ---- | ---- | ------------ |
| range | No | int | range_2g: 0;<br />range_4g : 1;<br />range_8g : 2;<br />range_16g: 3 | 

Return value: 

No. 

l **int_enable(int_code,tap_thr,dur,tap_axis,laten,window,ff_thr,ff_time,act_thr,act_axis,inact_thr,inact_axis,inact_time)**


Interrupt enable. 

Parameters: 

| Name       | Required | Type | Description                                           | 
| ---------- | ---- | ---- | ------------------------------ |
| int_code   | Yes  | int  | Interrupt type<br />Single-click interrupt: 0x40<br />Double-click interrupt: 0x20<br />Motion interrupt: 0x10<br />Stationary interrupt: 0x08<br />Free fall interrupt: 0x04 |
| tap_thr    | No   | int  | Optional for single or double click interrupts<br />Click threshold, default 0x30, recommended not to be less than this value |
| dur        | No   | int  | Optional for single or double click interrupts<br />Click duration, default 0x20, recommended to be greater than 0x10 |
| tap_axis   | No   | int  | Optional for single or double click interrupts<br />Click axis, default 0x07, which is xyz<br />Only x-axis: 0x04<br />Only y-axis: 0x02<br />Only z-axis: 0x01 |
| laten      | No   | int  | Optional for double click interrupts<br />Delay, double click needs to be triggered after the single click detection for this period, default 0x15 |
| window     | No   | int  | Optional for double click interrupts<br />Window, double click needs to be completed within this time, default 0xff |
| ff_thr     | No   | int  | Optional for free fall interrupt<br />Acceleration threshold, trigger needs to be greater than this acceleration, default 0x06, recommended 3-9 |
| ff_time    | No   | int  | Optional for free fall interrupt<br />Acceleration time, trigger needs to be greater than this time, default 0x15, recommended 0x14-0x46 |
| act_thr    | No   | int  | Optional for motion interrupt<br />Acceleration threshold, trigger needs to be greater than this acceleration, default 0x03 |
| act_axis   | No   | int  | Optional for motion interrupt, motion axis, default 0xf0<br />Only x-axis: 0xc0<br />Only y-axis: 0xa0<br />Only z-axis: 0x90 |
| inact_thr  | No   | int  | Optional for stationary interrupt<br />Acceleration threshold, trigger needs to be greater than this acceleration, default 0x03 |
| inact_axis | No   | int  | Optional for stationary interrupt, motion axis, default 0x0f<br />Only x-axis: 0x0c<br />Only y-axis: 0x0a<br />Only z-axis: 0x09 |
| inact_time | No   | int  | Optional for stationary interrupt<br />Stationary duration, trigger needs to be stationary for more than this time, default 0x03 | 

Return value: 

0 : Success 

-1 : Failure 

l **clear_int(int_code)**

Clear the enable of a certain interrupt. 

Parameters: 

| Name     | Required | Type | Description        | 
| -------- | ---- | ---- | --------------------- |
| int_code | Yes | int | Interrupt type<br />Single-click interrupt: 0x40<br />Double-click interrupt: 0x20<br />Movement interrupt: 0x10<br />Stationary interrupt: 0x08<br />Free fall interrupt: 0x04 | 

Return value: 

No


l **read_acceleration()**


Read the three-axis acceleration. 

Parameters: 

No. 

Return value: 

| Name    | Type  | Description            | 
| ------- | ----- | --------------------- |
|(x, y, z) | tuple | Axial accelerations along the x, y, and z axes, in units of G | 




l **process_single_tap ()**


Loop through reading the interrupt source register and click on interrupt detection. 

Note: If no interruption is detected, it will result in an infinite loop. It is recommended to execute it in the main thread with caution. Before execution, make sure to enable the interruption and configure it correctly. 

Parameters: 

No. 

Return value: 

Detected a click interruption 

l **process_double_tap()**


Loop through reading the interrupt source register, and double-click the interrupt detection. 

Note: If no interruption is detected, it will result in an infinite loop. It is recommended to execute it in the main thread with caution. Before execution, make sure to enable the interrupt function and configure it correctly by double-clicking. 

Parameters: 

No. 

Return value: 

Detected double-click interruption 

l **process_act ()**


Loop through reading the interrupt source register and perform motion interrupt detection. 

Note: If no interruption is detected, it will result in an infinite loop. It is recommended to execute it in the main thread with caution. Before execution, make sure that the motion interruption is enabled and configured correctly. 

Parameters: 

No. 

Return value: 

Motion interruption has been detected. 

l **process_inact()**


Loop through reading the interrupt source register and perform static interrupt detection. 

Note: If no interruption is detected, it will result in an infinite loop. It is recommended to execute it in the main thread with caution. Before execution, make sure that the interrupt enable is enabled and the configuration is correct. 

Parameters: 

No. 

Return value: 

Detected a static interruption 

l **process_ff ()**


Loop through reading the interrupt source register and detect free-fall interrupts. 

Note: If no interruption is detected, it will result in an infinite loop. It is recommended to execute it in the main thread with caution. Before execution, make sure that the free fall interruption is enabled and configured correctly. 

Parameters: 

No. 

Return value: 

1: Detected a break in free fall