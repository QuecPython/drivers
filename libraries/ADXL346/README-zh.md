# ADXL346三轴加速度传感器驱动文档
## 概述

本文档介绍如何使用ADXL346三轴加速度传感器驱动模块，通过I2C接口读取设备的运动数据，包括三轴加速度值及配置多种运动检测中断。

## 主要特性

- 读取X/Y/Z三轴加速度值
- 设置测量量程（2g/4g/8g/16g）
- 配置5种运动检测中断：
    - 单次点击（Single tap）
    - 双击（Double tap）
    - 活动检测（Activity）
    - 静止检测（Inactivity）
    - 自由落体（Free-fall）
- 实时中断状态检测

## 快速入门
### 1. 导入所需模块
```python
from machine import I2C
from adxl346 import Adxl346
import utime
```
### 2. 初始化传感器

```python
# 在I2C1总线上初始化ADXL346传感器，设备地址0x53
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
accel_sensor = Adxl346(i2c_dev)
```

### 3. 设置测量量程

```python
# 设置量程（可选2g/4g/8g/16g）
accel_sensor.set_range(Adxl346.range_8g)  # 8g量程
```

### 4. 读取传感器数据
#### 读取三轴加速度值

```python
x, y, z = accel_sensor.read_acceleration()
print("加速度值: X={}g, Y={}g, Z={}g".format(x, y, z))
```

#### 配置并使用中断（以双击检测为例）

```python
# 启用双击检测中断
accel_sensor.int_enable(Adxl346.DOUB_TAP_INT)

# 等待并处理中断事件
accel_sensor.process_double_tap()
print("检测到双击事件！")

# 读取当前加速度值
x, y, z = accel_sensor.read_acceleration()
```

## API接口说明

### **`Adxl346(i2c, dev_addr=0x53)`**

构造函数，初始化ADXL346传感器。

​​**参数说明:**

- i2c: I2C设备实例
- dev_addr: 传感器I2C地址（默认0x53）

### **`set_range(range=range_2g)`**

设置加速度测量量程。

​**​参数说明:​​**

- range: 量程选择（range_2g, range_4g, range_8g, range_16g）

### **`read_acceleration()`**

读取三轴加速度值。

​**​返回值:​​**

- (x, y, z) 三轴加速度值，单位为g

### **`int_enable(int_code, **kwargs)`**

启用特定中断功能。

​**​参数说明:​**​

- int_code: 中断类型选择：
    - SING_TAP_INT: 单次点击
    - DOUB_TAP_INT: 双击
    - ACT_INT: 活动检测
    - INACT_INT: 静止检测
    - FF_INT: 自由落体
- kwargs: 中断参数（详见技术说明）

### 中断处理函数。

阻塞等待特定中断发生：

- process_single_tap(): 单次点击
- process_double_tap(): 双击
- process_act(): 活动检测
- process_inact(): 静止检测
- process_ff(): 自由落体

## 应用示例

基本数据读取

```python
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
adxl = Adxl346(i2c_dev)
adxl.set_range(Adxl346.range_8g)

while True:
    x, y, z = adxl.read_acceleration()
    print("X={:.3f}g, Y={:.3f}g, Z={:.3f}g".format(x, y, z))
    utime.sleep(1)
```

双击检测应用
```python
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
adxl = Adxl346(i2c_dev)
adxl.int_enable(Adxl346.DOUB_TAP_INT)

while True:
    # 等待双击事件
    adxl.process_double_tap()
    
    # 事件发生后读取数据
    x, y, z = adxl.read_acceleration()
    print("双击事件！当前加速度: X={}g, Y={}g, Z={}g".format(x, y, z))
```

自由落体检测
```python
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
adxl = Adxl346(i2c_dev)
adxl.int_enable(Adxl346.FF_INT, ff_thr=0x06, ff_time=0x15)

while True:
    if adxl.process_ff():
        print("检测到自由落体事件！")
```

## 技术说明
### 1. 量程与分辨率

|量程|分辨率|最大测量值|
|----|----|----|
|2g |0.004g|±2g|
|4g|0.008g|±4g|
|8g|0.016g|	±8g|
|16g|0.032g|±16g|
### 2. 中断参数配置

各中断类型支持以下参数：
- 单次点击/双击:​​    
    - tap_thr: 触发阈值（默认0x30）
    - dur: 持续时间（默认0x20）
    - tap_axis: 检测轴（默认0x07所有轴）

- ​自由落体:​​

    - ff_thr: 触发阈值（默认0x06）
    - ff_time: 时间窗口（默认0x15）

- ​活动检测:​​

    - act_thr: 触发阈值（默认0x03）
    - act_axis: 检测轴（默认0xF0）

- ​静止检测:​​

    - inact_thr: 触发阈值（默认0x03）
    - inact_axis: 检测轴（默认0x0F）
    - inact_time: 静止时长（默认3）

### 3. 中断响应特性

- 所有中断检测响应时间均在毫秒级
- 建议主循环中至少保留20ms延时（utime.sleep_ms(20)）
- 实际应用中应根据需求调整各检测阈值参数

常见问题排查

- 检查I2C接线和地址（默认0x53）
- 确保传感器正确供电（3.3V）
- 确认中断引脚已正确连接和配置
- 确认I2C总线上无地址冲突

本驱动为使用ADXL346加速度传感器的运动检测应用提供了完整接口，适用于姿态检测、冲击检测、自由落体检测等应用场景。