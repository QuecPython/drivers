# HDC1080温湿度传感器驱动文档
## 概述

本文档介绍如何使用HDC1080温湿度传感器驱动模块测量环境温度和湿度。该传感器通过I2C接口提供高精度的温湿度数据，适用于各种环境监测应用。
## 主要特性

- 同时测量温度和湿度
- 高精度测量（温度±0.2°C，湿度±2%）
- 超低功耗设计（典型1.2μA）
- I2C数字接口
- 快速响应时间

## 快速入门
### 1. 导入所需模块
```python
from machine import I2C
from hdc1080 import Hdc1080
import utime
```
### 2. 初始化传感器
```python
# 在I2C1总线上初始化HDC1080传感器
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
sensor = Hdc1080(i2c_dev)
```
### 3. 读取温湿度数据
```python
# 读取温湿度数据
humidity, temperature = sensor.read()
print("温度: {:.2f}°C, 湿度: {:.2f}%".format(temperature, humidity))
```
## API接口说明

**`Hdc1080(i2c_obj, dev_addr=0x40)`**

构造函数，初始化HDC1080传感器。

**​​参数说明:**

- i2c_obj: I2C设备实例
- dev_addr: 传感器I2C地址（默认0x40）

**`read()`**

读取并返回当前温度和湿度值。

​**​返回值:​​**

- (humidity, temperature): 湿度百分比值和温度值
    - humidity: 相对湿度（单位：%）
    - temperature: 温度（单位：°C）

**`reset()`**

重置传感器，恢复出厂设置。调用后需重新初始化传感器。

## 应用示例

基础环境监测
```python
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
sensor = Hdc1080(i2c_dev)

while True:
    humidity, temperature = sensor.read()
    print("温度: {:.2f}°C, 湿度: {:.2f}%".format(temperature, humidity))
    utime.sleep(10)
```

温度异常警报系统
```python
def check_temperature_alert(temp, hum):
    critical_alerts = []
    warnings = []
    
    if temp > 35:
        critical_alerts.append("高温警报！")
    elif temp < 0:
        critical_alerts.append("低温警报！")
    elif temp > 30:
        warnings.append("温度偏高")
    elif temp < 5:
        warnings.append("温度偏低")
    
    if hum > 85:
        warnings.append("湿度过高")
    elif hum < 20:
        warnings.append("湿度过低")
    
    return critical_alerts, warnings

sensor = Hdc1080(i2c_dev)

while True:
    humidity, temperature = sensor.read()
    critical, warnings = check_temperature_alert(temperature, humidity)
    
    if critical:
        # 紧急警报处理逻辑
        print("⚠️ 紧急警报:", ", ".join(critical))
        # 这里可以添加短信、灯光报警等逻辑
        
    if warnings:
        print("警告:", ", ".join(warnings))
    
    utime.sleep(60)
```

## 常见问题排查

- I2C地址错误（正确地址0x40）
- I2C总线未初始化
- 传感器供电异常
- 传感器附近有热源干扰
- 湿度传感器暴露在冷凝环境中