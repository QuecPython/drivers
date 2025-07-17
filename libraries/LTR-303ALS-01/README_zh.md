# LTR303ALS环境光传感器驱动文档

## 概述

本文档介绍如何使用基于QuecPython的LTR303ALS环境光传感器进行光强度检测和中断控制。LTR303ALS是一款双通道光传感器，支持I2C通信接口，适用于需要精确光感测的应用场景（如自动亮度调节、环境监测等）。

## 硬件连接

在使用LTR303ALS模块前，请确保正确连接硬件：

- **I2C接口**：连接SCL/SDA引脚至开发板对应接口
- **VCC**：连接至3.3V电源（传感器工作电压范围2.7-3.6V）
- **GND**：接地
- **INT引脚**：连接至开发板GPIO中断引脚（如GPIO32）
- **ADDR引脚**：接地保持默认地址0x29（悬空时地址为0x4D）

## 快速开始

### 1. 初始化LTR303ALS模块

```python
from machine import I2C, ExtInt
import itl_303als

# 初始化I2C接口（使用I2C1标准模式）
i2c = I2C(I2C.I2C1, I2C.STANDARD_MODE)

# 初始化传感器（地址0x29，中断引脚GPIO32，下降沿触发，阈值100lux）
als = itl_303als(i2c, 0x29, ExtInt.GPIO32, 100, itl_303als.IRQ_FALLING)
```

### 2. 基本功能使用

```python
# 读取当前光强值（CH0/CH1）
ch0, ch1 = als.read()
print(f"CH0: {ch0}, CH1: {ch1}")

# 设置新的中断阈值（200lux）
als.set_threshold(200)
```

## 高级功能

### 1. 中断配置

```python
# 配置中断触发模式（上升沿/下降沿）
als.config_interrupt(itl_303als.IRQ_RISING)

# 设置中断持续条件（连续10次检测有效）
als.set_persist(0x0A)
```

### 2. 自动校准

```python
# 启动自动校准模式（持续10秒）
als.start_calibration(10000)

# 读取校准后的阈值
calibrated = als.get_calibrated_threshold()
print(f"Calibrated threshold: {calibrated}")
```

## 类和方法参考

### `itl_303als` 类

#### 构造函数

```python
itl_303als(i2c_bus, i2c_addr=0x29, int_pin=None, threshold=100, int_mode=IRQ_FALLING)
```

- `i2c_bus`: I2C总线对象
- `i2c_addr`: 设备I2C地址（默认0x29）
- `int_pin`: 中断引脚对象（可选）
- `threshold`: 初始中断阈值（lux）
- `int_mode`: 触发模式（IRQ_RISING/IRQ_FALLING）

#### 主要方法

|            方法名            |      参数      |       描述        |
| :--------------------------: | :------------: | :---------------: |
|           `read()`           |       无       | 读取CH0/CH1光强值 |
|      `set_threshold()`       | threshold(int) |   设置中断阈值    |
|     `config_interrupt()`     |   mode(int)    | 配置中断触发模式  |
|    `start_calibration()`     |  duration(ms)  |   启动自动校准    |
| `get_calibrated_threshold()` |       无       |  获取校准后阈值   |

#### 属性

|        属性名        | 类型 |      描述      |
| :------------------: | :--: | :------------: |
| `interrupt_occurred` | bool | 中断触发标志位 |
| `current_threshold`  | int  |  当前中断阈值  |

### 常量定义

| 常量          | 值   | 描述           |
| :------------ | :--- | :------------- |
| `IRQ_RISING`  | 0    | 上升沿触发中断 |
| `IRQ_FALLING` | 1    | 下降沿触发中断 |

## 注意事项

1. 确保I2C地址配置正确（ADDR引脚状态决定最终地址）
2. 中断引脚需配置正确上下拉电阻
3. 避免在强光环境下长时间工作（可能损坏传感器）
4. 校准时需保持环境光稳定

## 故障排除

|     现象     |    可能原因    |      解决方案      |
| :----------: | :------------: | :----------------: |
| 无法读取数据 |  I2C通信失败   | 检查接线和地址设置 |
|  中断不触发  | 阈值设置不合理 | 调整threshold参数  |
| 数据波动较大 |  电源噪声干扰  |    增加滤波电容    |