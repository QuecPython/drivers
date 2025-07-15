

# LIS2DH12 加速度传感器驱动使用说明

## 概述

本文档介绍了如何使用 Quectel 提供的 LIS2DH12 加速度传感器驱动代码。LIS2DH12 是一款低功耗三轴加速度计，适用于各种运动检测应用。

## 主要功能

- 传感器初始化与重置
- 加速度数据读取
- 中断功能配置（单击、双击、运动检测等）
- 工作模式设置

## 快速开始

### 1. 初始化传感器

```python
def __init__(self, i2c_dev, int_pin, slave_address=0x19):
        self._address = slave_address
        self._i2c_dev = i2c_dev
        self._int_pin = int_pin
        self._extint = None
        self._sensor_init()
```

### 2. 读取加速度数据

```python
# 读取三轴加速度数据
 def read_acceleration(self):
        '''
        read acceleration
        :return: x,y,z-axis acceleration
        '''

        while 1:
            status = self._read_data(LIS2DH12_STATUS_REG,1)[0]
            xyzda = status & 0x08   # if xyz data exists, set 1
            xyzor = status & 0x80
            if not xyzda:
                continue
            else:
                x,y,z = self._acceleration
                return (x, y, z)
```

### 3. 配置中断功能

```
# 定义中断回调函数
 def set_int_callback(self, cb):
        self._extint = ExtInt(self._int_pin, ExtInt.IRQ_FALLING, ExtInt.PULL_PU, cb)
```

## API详解

### 1. 构造函数 `__init__(self, i2c_dev, int_pin, slave_address=0x19):`

- 参数：
  - `i2c_dev`: I2C设备对象
  - `int_pin`: 连接传感器中断引脚的GPIO号
  - `slave_address`: 传感器I2C地址(默认0x19)

### 2. 主要方法

#### `sensor_reset()`

重置传感器

#### `int_enable(int_type, int_ths=0x12, time_limit=0x18, time_latency=0x12, time_window=0x55, duration=0x03)`

启用中断功能

- 参数：
  - `int_type`: 中断类型(如XYZ_SINGLE_CLICK_INT等)
  - `int_ths`: 中断阈值
  - `time_limit`: 时间限制(用于点击中断)
  - `time_latency`: 延迟时间(用于双击中断)
  - `time_window`: 时间窗口(用于双击中断)
  - `duration`: 持续时间

#### `set_int_callback(cb)`

设置中断回调函数

- 参数：
  - `cb`: 回调函数

#### `set_mode(mode)`

设置工作模式

- 参数：
  - `mode`: 0-高分辨率模式, 1-普通模式, 2-低功耗模式

### 3. 主要属性

#### `read_acceleration`

读取当前三轴加速度值(单位: g)

#### `int_processing_data()`

处理中断并返回当前加速度值

## 中断类型常量

| 常量名称             | 描述          |
| :------------------- | :------------ |
| XYZ_SINGLE_CLICK_INT | XYZ轴单击中断 |
| X_SINGLE_CLICK_INT   | X轴单击中断   |
| Y_SINGLE_CLICK_INT   | Y轴单击中断   |
| Z_SINGLE_CLICK_INT   | Z轴单击中断   |
| XYZ_DOUBLE_CLICK_INT | XYZ轴双击中断 |
| MOVE_RECOGNIZE       | 运动识别中断  |
| FF_RECOGNIZE         | 自由落体中断  |

## 注意事项

1. 使用前确保I2C总线已正确初始化
2. 中断引脚需要正确配置
3. 读取加速度数据前建议检查数据就绪状态
4. 不同工作模式会影响功耗和精度

## 技术支持

如需更多帮助，请联系Quectel技术支持团队。