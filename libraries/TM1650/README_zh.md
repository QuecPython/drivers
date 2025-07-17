# TM1650数码管驱动文档
## 概述

本文档介绍如何使用TM1650数码管驱动模块控制4位7段数码管显示。该驱动支持数字、字母、符号的显示，以及亮度控制、循环显示等高级功能。
## 主要特性

- 支持4位数码管独立控制
- 显示数字、字母和常用符号
- 支持小数点显示
- 亮度控制开关
- 循环显示功能
- 清屏和全显功能
- 简洁易用的API接口

## 快速入门
### 1. 初始化数码管
```python
from machine import Pin
from tm1650 import Tm1650

# 初始化数码管 (DIO=GPIO13, CLK=GPIO12)
tube = Tm1650(dio=Pin.GPIO13, clk=Pin.GPIO12)
```
### 2. 基本显示操作
```python
# 开启数码管
tube.on()

# 显示数字
tube.show_num(1234)

# 显示字符串
tube.show_str("HELL")

# 显示带小数点的数字
tube.show_num(56.78)  # 显示"56.78"

# 关闭数码管
tube.off()
```
## API接口说明
**`Tm1650(dio=None, clk=None)`**

构造函数，初始化数码管。

​​**参数说明:**

- dio: 数据引脚 (默认GPIO10)
- clk: 时钟引脚 (默认GPIO13)

**`on()`**

开启数码管显示。

**`off()`**

关闭数码管显示。

**`all_clear()`**

清除所有数码管显示。

**`clear_bit(bit)`**

清除指定位置的数码管显示。

**​​参数说明:**

- bit: 数码管位置 (1-4)

**`all_show()`**

所有数码管全亮（测试用）。

**`show_num(num)`**

显示数字。

​**​参数说明:**

- num: 要显示的数字 (-999到9999)

**`show_str(st)`**

显示字符串。

​**​参数说明:​​**

- st: 要显示的字符串 (最多4个字符)

**`show_dp(bit=1)`**

在指定位置显示小数点。

**​​参数说明:​​**

- bit: 小数点位置 (1-4)

**`circulate_show(st)`**

循环显示字符串。

**​​参数说明:**

- st: 要循环显示的字符串 (建议不超过12字符)

应用示例
温度显示应用
```python
def display_temperature(temp):
    # 显示温度值
    if temp >= 0:
        tube.show_num(int(temp * 100))  # 显示带两位小数
        tube.show_dp(3)  # 在第三位显示小数点
    else:
        tube.show_num(int(temp))  # 负数显示整数部分

# 示例使用
tube = Tm1650(Pin.GPIO13, Pin.GPIO12)
tube.on()

while True:
    temperature = read_temperature_sensor()  # 假设的温度读取函数
    display_temperature(temperature)
    utime.sleep(1)
```
倒计时功能
```python
def countdown(seconds):
    tube.on()
    for i in range(seconds, -1, -1):
        tube.show_num(i)
        utime.sleep(1)
    tube.show_str("END")
    utime.sleep(2)
    tube.off()

# 10秒倒计时
countdown(10)
```

## 常见问题排查

- 数码管不亮	
    - 电源未接通
    - 未调用on()
    - 初始化引脚错误
- 部分段不亮	
    - 硬件损坏
    - 段位映射错误
    - 驱动电流不足
- 显示乱码	
    - 字符未在映射表中
    - 数据传输错误
- 亮度无法调节	
    - 控制命令错误
    - 亮度寄存器未配置
