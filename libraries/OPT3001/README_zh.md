# OPT3001 光照传感器示例代码说明文档

## 概述

本文档介绍如何使用基于QuecPython的OPT3001光照传感器进行光照强度测量。OPT3001是一种高精度数字光照传感器，适用于环境光监测、显示背光控制等应用场景。

## 硬件连接

在使用OPT3001模块前，请确保正确连接硬件：

- I2C接口连接（SCL/SDA）
- VCC连接至3.3V电源
- GND接地

## 快速开始

### 1. 初始化OPT3001模块

```python
from machine import I2C
from usr.opt3001 import Opt3001

# 初始化I2C接口
i2c_obj = I2C(I2C.I2C1, I2C.FAST_MODE)
# 初始化OPT3001传感器
opt = Opt3001(i2c_obj)
print("OPT3001模块初始化完成")
```

### 2. 基本功能使用

#### 单次测量模式

```python
# 设置为单次测量模式
opt.set_measure_mode(1)
# 等待测量完成（至少800ms）
utime.sleep_ms(1000)
# 读取光照强度
lux = opt.read()
print('当前光照强度: {0} lux'.format(lux))
```

#### 连续测量模式

```python
# 设置为连续测量模式
opt.set_measure_mode(2)

while True:
    # 读取光照强度
    lux = opt.read()
    print('当前光照强度: {0} lux'.format(lux))
    utime.sleep(1)  # 每秒读取一次
```

## 高级功能

### 1. 自动测量与记录

```python
# 初始化传感器
i2c_obj = I2C(I2C.I2C1, I2C.FAST_MODE)
opt = Opt3001(i2c_obj)

# 设置为单次测量模式
opt.set_measure_mode(1)

for i in range(20):
    utime.sleep_ms(1000)  # 每次测量间隔1秒
    print("测量次数: {}------------".format(i+1))
    lux = opt.read()
    print("光照强度: {0} lux".format(lux))
    # 触发下一次测量
    opt.set_measure_mode(1)
```

### 2. 低功耗模式

```python
# 设置为关机模式以节省功耗
opt.set_measure_mode(0)
print("传感器已进入低功耗模式")

# 需要测量时再唤醒
opt.set_measure_mode(1)  # 单次测量模式
utime.sleep_ms(1000)
lux = opt.read()
print("当前光照强度: {0} lux".format(lux))
```

## 注意事项

1. 确保I2C接口连接正确，SCL和SDA线不要接反
2. 单次测量模式下，每次读取后需要重新触发测量
3. 两次读取之间间隔需大于800ms（传感器转换时间）
4. 传感器默认I2C地址为0x44，如有修改请相应调整
5. 避免强光直射传感器，可能影响测量精度

## 故障排除

1. **无法读取数据**：
   - 检查I2C连接是否正确
   - 确认传感器供电正常（3.3V）
   - 验证I2C地址是否正确
2. **测量值不准确**：
   - 确保传感器表面清洁无遮挡
   - 避免传感器处于极端温度环境
   - 检查是否有强光源直接照射
3. **通信错误**：
   - 检查I2C总线是否正常工作
   - 确认上拉电阻已正确连接
   - 尝试降低I2C通信速率

## API参考

### 主要方法

- `set_measure_mode(mode)`: 设置测量模式
  - 参数：
    - mode: 0=关机, 1=单次测量, 2=连续测量
  - 返回值：0=成功, -1=失败
- `read()`: 读取光照强度值
  - 返回值：当前光照强度值（单位：lux）

I2C接口[参考](https://developer.quectel.com/doc/quecpython/API_reference/zh/peripherals/machine.I2C.html)
