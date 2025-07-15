# GL5516光敏电阻传感器驱动文档

## 概述

本文档介绍如何使用GL5516光敏电阻驱动模块测量环境光照强度，通过读取电阻值变化来感知光线强弱。

## 主要特性

- 读取ADC原始电压值
- 将电压值转换为电阻值
- 简洁易用的光照传感API接口

## 快速入门

### 1. 导入所需模块

```python
from misc import ADC
from gl5516 import Gl5516
import utime as time
```

### 2. 初始化传感器

```python
# 创建ADC设备实例
adc_device = ADC()

# 在ADC通道0上初始化GL5516传感器
ldr_sensor = Gl5516(adc_device, ADC.ADC0)
```

### 3. 读取传感器数据

#### 读取电阻值

```python
resistance = ldr_sensor.read()
print(f"光敏电阻阻值: {resistance}Ω")
```

#### 读取原始电压值

```python
voltage = ldr_sensor.read_volt()
print(f"原始电压值: {voltage}mV")
```

## API接口说明

### `Gl5516(adc_dev, adcn)`

构造函数，用于初始化GL5516传感器。

**参数说明:**

- `adc_dev`: ADC设备实例
- `adcn`: ADC通道号(例如: `ADC.ADC0`)

### `read()`

读取并返回光敏电阻的阻值，单位为欧姆(Ω)。

**返回值:**

- 光敏电阻阻值(Ω)

### `read_volt()`

读取并返回ADC原始电压值。

**返回值:**

- 电压值，单位为毫伏(mV)

## 应用示例

```python
from misc import ADC
from gl5516 import Gl5516
import utime as time

# 初始化传感器
adc = ADC()
ldr = Gl5516(adc, ADC.ADC0)

# 持续监测光照强度
while True:
    resistance = ldr.read()
    voltage = ldr.read_volt()
    
    print(f"光照强度 - 电阻值: {resistance}Ω, 电压值: {voltage}mV")
    
    if resistance > 10000:  # 黑暗环境
        print("检测到黑暗环境")
    elif resistance < 2000:  # 明亮环境
        print("检测到明亮环境")
    
    time.sleep(1)
```

## 技术说明

1. 电阻值计算基于特定分压电路配置：
   - 4.7kΩ电阻(R1)
   - 40.2kΩ电阻(R2)
   - 3.3V供电电压
2. 如需使用不同电路配置，请相应修改`_voltage_to_resistance()`方法。
3. 传感器响应时间通常在毫秒级，1秒的采样间隔适用于大多数应用场景。
4. 典型阻值范围：
   - 强光环境：约1kΩ
   - 黑暗环境：约100kΩ或更高

## 常见问题排查

- 如果读数不稳定，请检查连接是否可靠和电源是否稳定
- 确保ADC通道配置正确
- 确认分压电路与驱动程序的假设相匹配

本驱动为使用GL5516光敏电阻的光照传感应用提供了简洁的接口，适用于自动照明控制、日光检测等光敏应用场景。 

