# AHT10 温湿度传感器示例代码说明文档

## 概述

本文档介绍如何使用基于QuecPython的AHT10温湿度传感器进行环境温湿度测量。AHT10是一款高精度数字温湿度传感器，适用于智能家居、气象监测、工业控制等场景。

## 硬件连接

在使用AHT10模块前，请确保正确连接硬件：

- I2C接口连接（SCL/SDA）
- VCC连接至3.3V电源
- GND接地
- 地址选择引脚（ADDR）悬空时默认地址为0x38

## 快速开始

### 1. 初始化AHT10模块

```python
from machine import I2C
from drivers.aht10 import Aht10

# 初始化I2C接口,使用实际的I2C接口
i2c_obj = I2C(I2C.I2C1, I2C.FAST_MODE)
# 初始化AHT10传感器（默认地址0x38）
aht = Aht10(i2c_obj)
print("AHT10模块初始化完成")
```

### 2. 基本功能使用

#### 单次测量模式

```python
# 读取温湿度数据
humidity, temperature = aht.read()
print('当前湿度: {0}%RH，温度: {1}℃'.format(humidity, temperature))
```

#### 连续测量模式（需配合定时任务实现）

```python
import utime

while True:
    humidity, temperature = aht.read()
    print('当前湿度: {0}%RH，温度: {1}℃'.format(humidity, temperature))
    utime.sleep(2)  # 每2秒读取一次
```

## 注意事项

1. 确保I2C接口连接正确，SCL和SDA线不要接反
2. 传感器供电电压范围：3.3V±0.1V
3. 测量前需等待至少15ms稳定时间
4. 避免暴露在极端温度（-40~85℃）或高湿度（>95%RH）环境

## 故障排除

1. **无法读取数据**：
   - 检查I2C连接是否正确
   - 确认传感器供电正常（3.3V）
   - 验证I2C地址是否正确（默认0x38）
2. **测量值异常**：
   - 检查传感器是否受阳光直射或热源干扰
   - 确保测量环境通风良好
   - 重启设备重置传感器状态

## API参考

### 类初始化

```python
class Aht10:
    def __init__(self, i2c, address=0x38):
        """
        初始化AHT10传感器
        :param i2c: I2C对象
        :param address: I2C从设备地址（默认0x38）
        """
```

### 核心方法

|         方法名         | 参数说明 |               返回值                |      功能描述      |
| :--------------------: | :------: | :---------------------------------: | :----------------: |
|         read()         |    无    | (humidity:float, temperature:float) |   获取温湿度数据   |
| get_calibration_data() |    无    |                dict                 | 获取传感器校准参数 |

## 补充说明

- 数据手册参考：`drivers/libraries/aht10/AHT10.pdf`
- 示例代码路径：`drivers/libraries/aht10/aht10_demo.py`
- [I2C接口参考](https://developer.quectel.com/doc/quecpython/API_reference/zh/peripherals/machine.I2C.html)