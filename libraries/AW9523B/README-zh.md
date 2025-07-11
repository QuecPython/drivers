AW9523 GPIO扩展器驱动模块

**类引用** 
```python
from aw9523 import AW9523
```

实例化参数

| 名称 | 必填 | 类型 | 说明 |
|----|----|----|----|
| i2c_bus | 是 | I2C对象 | I2C总线对象 |
| int_pin | 否 | int | 中断引脚号，默认1 |
| int_mode | 否 | int | 中断模式，默认0 |
| int_callback | 否 | function | 中断回调函数 |
| address | 否 | int | I2C设备地址，默认0x58（按键驱动地址）|

端口对象

```python
porta = Port(0, aw)  # 端口A
portb = Port(1, aw)  # 端口B
```

主要方法

l reset()

复位AW9523芯片。

​​参数：​​ 

无
​​返回值：​​ 

无

l pin(pin, mode=None, value=None, interrupt_enable=None)

配置单个引脚。

​​参数：​​

| 名称 | 类型 | 说明 |
|----|----|----|
| pin | int | 引脚号（0-15） |
| mode | int | 模式：0=输出，1=输入 |
| value | int | 输出值：0=低电平，1=高电平 |
| interrupt_enable | int | 中断使能：0=禁用，1=启用 |

​​返回值：​​

设置值时：无
读取值时：当前引脚电平（0或1）

read(pin)

读取单个引脚电平。

​​参数：​​
| 名称 | 类型 | 说明 |
|----|----|----|
| pin | int | 引脚号（0-15）|

​​返回值：​​

0：低电平
1：高电平

全局属性

| 属性 | 类型 | 说明 |
|----|----|----|
| mode | int | 所有引脚模式（读写）|
| interrupt_enable | int | 所有引脚中断使能（读写）|
| interrupt_flag | int | 所有引脚中断标志（只读）|
| gpio | int | 所有GPIO值（读写）|