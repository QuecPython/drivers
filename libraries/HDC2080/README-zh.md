# HDC2080温湿度传感器驱动文档
## 概述

本文档介绍如何使用HDC2080温湿度传感器驱动模块精确测量环境温度和湿度。该传感器通过I2C接口提供数字化的温湿度数据，具有低功耗和高精度的特点。
## 主要特性

- 高精度温湿度测量（温度±0.2°C，湿度±2%）
- 超宽量程：温度(-40°C ~ 85°C)，湿度(0% ~ 100%)
- 双16位模数转换器
- I2C数字接口（默认地址0x40）
- 低功耗模式（典型0.1μA待机电流）

## 快速入门
### 1. 导入所需模块
```python
from machine import I2C
from hdc2080 import Hdc2080
import utime
```
### 2. 初始化传感器
```python
# 在I2C1总线上初始化HDC2080传感器
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
sensor = Hdc2080(i2c_dev)
```
### 3. 读取温湿度数据
```python
# 读取温湿度数据
humidity, temperature = sensor.read()
print("温度: {:.2f}°C, 湿度: {:.2f}%".format(temperature, humidity))
```

## API接口说明

**`Hdc2080(i2c, addr=0x40)`**

构造函数，初始化HDC2080传感器。

​​**参数说明:**

- i2c: I2C设备实例
- addr: 传感器I2C地址（默认0x40）

**`reset()`**

重置传感器，恢复出厂设置。

**`read_temperature()`**

读取当前温度值。

​**​返回值:​​**

- 温度值（单位：°C）

**`read_humidity()`**

读取当前湿度值。

​​**返回值:**

- 湿度值（单位：%）

**`read()`**

触发温湿度测量并读取结果。

**`​​返回值:​​`**

- (humidity, temperature): 湿度百分比值和温度值

## 应用示例
基础环境监测
```python
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
sensor = Hdc2080(i2c_dev)

while True:
    humidity, temperature = sensor.read()
    print("温度: {:.2f}°C, 湿度: {:.2f}%".format(temperature, humidity))
    utime.sleep(10)
```


## 常见问题排查
- I2C地址错误（正确地址0x40）
- I2C总线未初始化
- 传感器供电异常
- 传感器附近有热源干扰
- 湿度传感器暴露在冷凝环境中