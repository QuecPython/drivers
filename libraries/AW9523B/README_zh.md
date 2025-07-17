# AW9523 GPIO扩展芯片驱动文档
## 概述

本文档介绍如何使用AW9523驱动模块实现GPIO扩展功能。该芯片通过I2C接口扩展16个双向GPIO引脚，支持独立配置输入/输出模式，并具备电平变化中断检测功能。

## 主要特性
- 扩展16个双向GPIO引脚
- 独立配置每个引脚为输入/输出模式
- 支持高低电平控制（输出模式）
- 支持引脚状态读取（输入模式）
- 内置边沿中断检测功能（上升沿/下降沿）
- 中断状态实时回调通知

## 快速入门
### 1. 导入所需模块

```python
from machine import I2C, ExtInt
from aw9523 import AW9523
from usr.common import create_thread
import utime
```

### 2. 初始化传感器
```python
# 创建I2C设备实例（I2C1，标准模式）
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)

# 定义中断回调函数
def int_callback(pin_data):
    pin, level = pin_data
    print("引脚{}电平变化! 当前电平: {'高' if level else '低'}".format(pin))

# 在I2C0总线上初始化AW9523芯片（地址0x58，使用引脚1作为中断引脚）
expander = AW9523(
    i2c_bus=i2c_dev,
    int_pin=1,                 # 中断引脚编号
    int_callback=int_callback  # 中断回调函数
)
```

### 3. 配置GPIO引脚
```python
# 配置引脚0为输出模式，并设置高电平
expander.pin(0, mode=0, value=1)

# 配置引脚8为输入模式，并启用中断
expander.pin(8, mode=1, interrupt_enable=1)

# 配置引脚9为输入模式，不启用中断
expander.pin(9, mode=1, interrupt_enable=0)
```

### 4. 读取引脚状态
```python
# 读取引脚8的当前电平状态
level = expander.read(8)
print("引脚8当前电平: {}".format('高' if level else '低'))

# 批量读取所有引脚状态
all_pins_state = expander.gpio
print("所有引脚状态: {}".format(bin(all_pins_state)))
```

## API接口说明

### **`AW9523(i2c_bus, int_pin=1, int_mode=0, int_callback=None, address=0x58)`**

构造函数，初始化AW9523芯片

​**​参数说明:​​**

- i2c_bus: I2C总线实例
- int_pin: 中断检测引脚编号
- int_mode: 中断触发模式
- int_callback: 中断回调函数
- address: 设备I2C地址（0x58或0x5B）

**`pin(pin, mode=None, value=None, interrupt_enable=None)`**

配置指定引脚参数

​​**参数说明:**

- pin: 引脚编号 (0-15)
- mode: 引脚模式
    - 0: 输出模式
    - 1: 输入模式
- value: 输出电平值（输出模式时有效）
    - 0: 低电平
    - 1: 高电平
- interrupt_enable: 中断使能
    - 0: 禁用中断
    - 1: 使能中断

**`read(pin)`**

读取指定引脚电平状态

**​参数说明:**

- pin: 引脚编号 (0-15)

**​​返回值:​​**

    - 0: 低电平
    - 1: 高电平

属性访问器

- mode: 所有引脚模式状态（16位）
- interrupt_enable: 所有引脚中断使能状态（16位）
- gpio: 所有引脚电平状态（16位）

## 应用示例
基础GPIO扩展应用
```python
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
expander = AW9523(i2c_dev)

# 配置引脚0-3为输出模式
for i in range(4):
    expander.pin(i, mode=0, value=0)

# 配置引脚8-11为输入模式
for i in range(8, 12):
    expander.pin(i, mode=1, interrupt_enable=0)

while True:
    # 读取引脚8-11状态
    for i in range(8, 12):
        state = expander.read(i)
        print("Pin {} state: {}".format(i, state))
    
    utime.sleep(1)
```

中断检测应用
```python
def int_handler(pin_data):
    pin, level = pin_data
    print("Pin {} changed to {}".format(pin, level))

i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
expander = AW9523(i2c_dev, int_callback=int_handler)

# 配置引脚4-7为输入，启用中断
for i in range(4, 8):
    expander.pin(i, mode=1, interrupt_enable=1)

# 持续执行其他任务
while True:
    # 主程序逻辑
    utime.sleep(10)
```
LED控制应用
```python
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
expander = AW9523(i2c_dev)

# 配置引脚12-15为输出模式，控制LED
led_pins = [12, 13, 14, 15]
for pin in led_pins:
    expander.pin(pin, mode=0, value=0)

# LED流水灯效果
while True:
    for pin in led_pins:
        expander.pin(pin, value=1)  # 点亮LED
        utime.sleep_ms(200)
        expander.pin(pin, value=0)  # 熄灭LED
```
## 技术说明
### 1. 引脚映射

|端口|引脚范围|寄存器|
|----|----|----|
|PORTA|0-7|0x00|
|PORTB|8-15|0x01|

### 2. 中断处理机制

- 中断使用硬件INT引脚触发
- 电平变化时中断引脚触发
- 中断回调函数格式：callback([pin, level])
    - pin: 发生变化的引脚号 (0-15)
    - level: 变化后的电平 (0:低/1:高)

### 3. 配置选项
|配置类型|取值范围|说明|
|----|----|----|
|引脚模式|0/1|0=输出, 1=输入|
|输出电平|0/1|0=低电平, 1=高电平|
|中断使能|0/1|0=禁用, 1=使能|
|中断触发模式|0/1|0=双边沿, 1=单边沿(保留)|

### 4. I2C地址说明
|设备类型|I2C地址|
|----|----|
|按键驱动|0x58|
|IO扩展器|0x5B|

常见问题排查
    
- 检查I2C连线是否正确
- 确认I2C地址是否正确（0x58或0x5B）
- 确认interrupt_enable设置为1
- 检查INT引脚配置是否正确
- 确保在循环中没有阻塞中断线程的操作


本驱动为AW9523 GPIO扩展芯片提供了完整的控制接口，适用于各种需要扩展IO的应用场景