# BH1750(GY302) 环境光传感器驱动文档
## 概述

本文档介绍如何使用BH1750（或GY302模块）环境光传感器检测光照强度。该传感器支持高精度光强测量（最高0.5lx分辨率），使用I2C接口通信。
## 主要特性

- 测量范围：1-65535 lx
- 精度范围：0.5-4lx（可选）
- 低电流（120μA）
- I2C接口（地址0x23）
- 50Hz/60Hz光源噪声抑制
- 数字输出（无需AD转换）
-  温度依赖性低

## 快速入门

###  示例代码
```python
from machine import I2C
from bh1750 import Bh1750

# 初始化I2C（以EC600U为例）
i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
# 初始化传感器
sensor = Bh1750(i2c_dev)

# 激活传感器
sensor.on()

# 设置测量模式（最高精度）
sensor.set_measure_mode(CONTI_H_MODE2)

# 读取环境光照值
light_level = sensor.read()
print("光照强度：", light_level, "lx")

# 暂停使用时关闭传感器
sensor.off()
```

## API接口说明
```python
Bh1750(i2c, dev_addr=0x23)
```
构造函数，初始化传感器。

​**​参数说明:**

- i2c: I2C对象（已初始化的I2C实例）
- dev_addr: I2C设备地址（默认0x23，可选0x5C）

**`on()`**

激活传感器，准备进行测量。
**`off()`**

关闭传感器，进入低功耗状态（仅消耗1μA电流）。
**`reset()`**

重置传感器，清除历史数据。
**`set_measure_mode(mode=CONTI_H_MODE2)`**

设置测量模式。

​​**模式说明:**

- CONTI_H_MODE：连续高分辨率模式（1lx精度）
- CONTI_H_MODE2：连续高分辨率模式2（0.5lx精度）※推荐
- CONTI_L_MODE：连续低分辨率模式（4lx精度）
- ONE_H_MODE：单次高分辨率模式（1lx精度）
- ONE_H_MODE2：单次高分辨率模式2（0.5lx精度）
- ONE_L_MODE：单次低分辨率模式（4lx精度）

**`read()`**

读取当前光照强度值。

**​​返回值:**

- 光照强度值（单位：勒克斯lx）


## 典型应用
自动背光调节
```python
sensor = Bh1750(i2c_dev)
sensor.on()
sensor.set_measure_mode(CONTI_H_MODE2)

# 背光级别映射表
brightness_levels = [
    (0, 10, 1),     # 极暗环境
    (10, 50, 2),    # 低光环境
    (50, 200, 3),   # 普通室内
    (200, 500, 4),  # 明亮室内
    (500, 1000, 5), # 明亮光照
    (1000, 3000, 6),# 户外阴天
    (3000, 20000, 7) # 阳光直射
]

while True:
    light = sensor.read()
    
    # 确定背光级别
    level = 0
    for min_lux, max_lux, lvl in brightness_levels:
        if min_lux <= light < max_lux:
            level = lvl
            break
    
    set_backlight(level)  # 设置背光强度
    utime.sleep(5)       # 每5秒检测一次
```
光照记录器
```python
def light_logger(interval=60, duration=86400):
    '''连续记录光照强度'''
    sensor.on()
    sensor.set_measure_mode(ONE_H_MODE2)  # 单次高精度模式
    log = []
    start_time = utime.time()
    
    while utime.time() - start_time < duration:
        # 读取并存储数据
        timestamp = utime.localtime()
        light_level = sensor.read()
        log.append((timestamp, light_level))
        
        # 休眠直到下次测量
        utime.sleep(interval - 0.1)  # 考虑测量时间补偿
    
    # 日志处理和数据存储
    save_to_file(log)
    sensor.off()

# 记录24小时数据（每5分钟记录一次）
light_logger(interval=300, duration=86400)
```

## 常见问题排查
- 传感器位置​​：避免被遮挡，确保测量真实环境光
-  ​光源干扰​​：避免光线直接照射在传感器上造成读数偏差
- ​功耗优化​​：不需要频繁检测时关闭传感器
- ​光照范围​​：超出传感器范围时（>65535lx）会达到最大测量值
- 校准调整​​：首次使用时需在不同光照条件下校准读数准确性