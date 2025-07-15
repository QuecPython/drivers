# RDA5807 FM收音机模块驱动使用说明

## 概述

本文档介绍RDA5807 FM收音机模块的Python驱动使用方法。该驱动通过I2C接口与RDA5807芯片通信，提供完整的FM收音机功能控制。

## 主要功能

- FM收音机初始化与配置
- 频率设置与频道搜索
- 音量控制与静音功能
- 信号强度检测
- 高低音调节

## 快速入门

### 1. 硬件连接

```python
# 定义引脚连接
rdaclk = Pin.GPIO2  # 时钟线
rdadio = Pin.GPIO3  # 数据线
```

### 2. 初始化收音机

```python
from machine import Pin
import RDA5807  # 假设驱动保存为RDA5807.py

# 创建收音机实例
radio = RDA5807.RDA5807(rdaclk=Pin.GPIO2, rdadio=Pin.GPIO3)

# 初始化收音机
radio._rda_init()
print("收音机初始化完成")
```

### 3. 基本操作

```python
# 启用FM功能
radio.fm_enable(1)

# 设置音量(0-15)
radio.vol_set(10)

# 搜索并播放频道
current_freq = radio.seek_channel()
print(f"当前频率: {current_freq}MHz")
```

## API详细说明

### 核心方法

#### `_rda_init()`

初始化RDA5807芯片，设置默认参数

#### `fm_enable(flag)`

启用/禁用FM功能

- `flag`: 1=启用, 0=禁用

#### `vol_set(vol)`

设置音量

- `vol`: 音量级别(0-15)

#### `mute_set(mute)`

设置静音

- `mute`: 1=静音, 0=取消静音

#### `bass_set(bass)`

设置低音增强

- `bass`: 1=启用, 0=禁用

### 频道控制

#### `freq_set(freq)`

设置特定频率

- `freq`: 频率值(单位10kHz)，范围6500-10800(即87.0-108.0MHz)

#### `seek_channel()`

自动搜索并锁定频道，返回找到的频率(MHz)

#### `next_chanl()`

搜索并播放下一个可用频道

#### `seek_direction(dir)`

设置搜索方向

- `dir`: 1=向上搜索, 0=向下搜索

### 信号检测

#### `rssi_get()`

获取当前信号强度(0-127)

#### `seekth_set(rssi)`

设置自动搜台信号阈值

- `rssi`: 阈值(0-15)，数值越低搜到的台越多

## 应用示例

### 基本收音机功能

```python
# 初始化
radio = RDA5807.RDA5807(rdaclk=Pin.GPIO2, rdadio=Pin.GPIO3)
radio._rda_init()

# 启用收音机
radio.fm_enable(1)
radio.vol_set(12)  # 设置中等音量

# 搜索并播放频道
current_freq = radio.seek_channel()
print(f"正在播放: {current_freq}MHz")

# 5秒后切换到下一个频道
time.sleep(5)
radio.next_chanl()
```

### 信号强度监测

```python
while True:
    strength = radio.rssi_get()
    print(f"当前信号强度: {strength}")
    if strength < 30:
        print("信号较弱，尝试重新搜索...")
        radio.seek_channel()
    time.sleep(2)
```

## 注意事项

1. 确保硬件连接正确，特别是I2C引脚连接
2. 初始化后等待至少30ms再进行其他操作
3. 频率设置范围是87.0-108.0MHz(对应6500-10800)
4. 音量设置范围是0-15，建议初始设置为8-10
5. 搜索频道时可能需要几秒钟时间

## 故障排除

- 如果初始化失败，检查I2C线路和电源
- 无声音时检查静音设置和音量级别
- 信号差时尝试调整天线位置或降低搜索阈值

## 技术支持

如需进一步帮助，请参考RDA5807芯片数据手册或联系硬件供应商。

------

> 注意：本文档基于提供的RDA5807驱动代码编写，所有API和示例均来自源代码实现。实际使用时请根据硬件环境调整引脚定义和参数设置。