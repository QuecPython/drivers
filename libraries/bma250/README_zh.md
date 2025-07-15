

# BMA250加速度传感器驱动使用说明

## 概述

本文档介绍Quectel开发的BMA250加速度传感器驱动使用方法。BMA250是一款低功耗数字三轴加速度传感器，具有灵活的配置选项。

## 主要功能

- 传感器初始化和复位
- 可配置测量范围(±2g至±16g)
- 可调输出数据速率(7.81Hz至1000Hz)
- 多种中断功能(敲击、倾斜、方向等)
- 加速度数据读取

## 快速入门

### 1. 初始化

```python
from machine import I2C
from bma250 import Bma250

# 初始化I2C接口
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)

# 创建传感器实例
sensor = Bma250(i2c_dev)
```

### 2. 基本配置

```python
# 设置测量范围(默认±2g)
sensor.set_range(Bma250.RANGE_SEL_2G)  # 选项: RANGE_SEL_2G, RANGE_SEL_4G, RANGE_SEL_8G, RANGE_SEL_16G

# 设置输出数据速率(默认7.81Hz)
sensor.set_hz(Bma250.BW_SEL_1000)  # 选项从BW_SEL_7_81到BW_SEL_1000
```

### 3. 读取加速度数据

```python
# 读取加速度值(x, y, z单位g)
x, y, z = sensor.read_acceleration()
print(f"X: {x}g, Y: {y}g, Z: {z}g")
```

## 中断配置

### 可用中断类型

| 中断常量        | 描述                 |
| :-------------- | :------------------- |
| `slope_en_x`    | X轴倾斜检测          |
| `slope_en_y`    | Y轴倾斜检测          |
| `slope_en_z`    | Z轴倾斜检测          |
| `slope_en_xyx`  | 任意轴倾斜检测       |
| `d_tap_en`      | 双击检测             |
| `s_tap_en`      | 单击检测             |
| `orient_en`     | 方向变化检测         |
| `flat_en`       | 水平位置检测         |
| `low_g_en`      | 低重力检测(自由落体) |
| `high_g_en_x`   | X轴高重力检测        |
| `high_g_en_y`   | Y轴高重力检测        |
| `high_g_en_z`   | Z轴高重力检测        |
| `high_g_en_xyx` | 任意轴高重力检测     |

### 示例:配置敲击检测

```python
# 启用单击检测
sensor.int_enable(Bma250.s_tap_en)

# 等待并处理敲击事件
while True:
    if sensor.process_single_tap():
        print("检测到单击!")
        x, y, z = sensor.read_acceleration()
        print(f"当前加速度: X={x}g, Y={y}g, Z={z}g")
        break
    utime.sleep_ms(10)
```

### 示例:自由落体检测

```python
# 启用低重力(自由落体)检测
sensor.int2_enable(Bma250.low_g_en)

# 等待自由落体事件
while True:
    if sensor.process_low_g():
        print("检测到自由落体!")
        break
    utime.sleep_ms(10)
```

## 高级配置

### 中断参数

中断函数接受多个配置参数:

```python
# 包含所有参数的示例(显示默认值)
sensor.int_enable(
    int_code=Bma250.s_tap_en,
    tap_thr=0x03,     # 敲击阈值
    tap_dur=0x04,     # 敲击持续时间
    slop_thr=0x14,    # 倾斜阈值
    slop_dur=0x03,    # 倾斜持续时间
    flat_hold_time=0x10  # 水平位置保持时间
)

sensor.int2_enable(
    int_code=Bma250.low_g_en,
    low_mode=0x81,    # 低重力模式
    low_th=0x30,      # 低重力阈值
    low_dur=0x09,     # 低重力持续时间
    high_th=0xc0,     # 高重力阈值
    high_dur=0x0f     # 高重力持续时间
)
```

## 错误处理

驱动会抛出`CustomError`异常处理各种错误情况:

```python
try:
    sensor = Bma250(i2c_dev)
    sensor.set_range(Bma250.RANGE_SEL_4G)
except CustomError as e:
    print(f"错误: {e}")
```

## 应用示例

```python
from machine import I2C
from bma250 import Bma250
import utime

# 初始化
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
sensor = Bma250(i2c_dev)

# 配置为高灵敏度
sensor.set_range(Bma250.RANGE_SEL_2G)
sensor.set_hz(Bma250.BW_SEL_1000)

# 启用方向检测
sensor.int_enable(Bma250.orient_en)

# 主循环
while True:
    if sensor.process_orient():
        x, y, z = sensor.read_acceleration()
        print(f"方向改变! 当前值: X={x}g, Y={y}g, Z={z}g")
    
    utime.sleep_ms(100)
```

## 注意事项

1. 传感器需要正确的电源供应和I2C上拉电阻
2. 中断引脚必须在硬件上正确配置
3. 更高的数据速率会消耗更多电量
4. 更小的测量范围提供更好的分辨率但可检测的最大加速度更小

如需技术支持，请联系Quectel无线解决方案。