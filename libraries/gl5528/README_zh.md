# GL5528光敏电阻传感器驱动文档

## 概述

本文档介绍GL5528光敏电阻传感器的驱动使用方法，该传感器可测量环境光照强度并转换为电阻值和光照度(lux)值。

## 主要特性

- 读取ADC原始电压值
- 将电压值转换为电阻值
- 通过预设对照表将电阻值转换为光照度(lux)
- 提供电阻值和光照度双输出

## 快速入门

### 1. 导入所需模块

```python
from misc import ADC
from gl5528 import Gl5528
import utime as time
```

### 2. 初始化传感器

```python
# 创建ADC设备实例
adc_device = ADC()

# 在ADC通道0上初始化GL5528传感器
ldr_sensor = Gl5528(adc_device, ADC.ADC0)
```

### 3. 读取传感器数据

#### 读取电阻值和光照度

```python
resistance, lux = ldr_sensor.read()
print("光敏电阻阻值: {}Ω, 光照度: {}lux".format(resistance, lux))
```

#### 读取原始电压值

```python
voltage = ldr_sensor.read_volt()
print("原始电压值: {}mV".format(voltage))
```

## API接口说明

### `Gl5528(adc_dev, adcn)`

构造函数，用于初始化GL5528传感器。

**参数说明:**

- `adc_dev`: ADC设备实例
- `adcn`: ADC通道号(例如: `ADC.ADC0`)

### `read()`

读取并返回光敏电阻的阻值和光照度。

**返回值:**

- 元组(resistance, lux)
  - resistance: 光敏电阻阻值(Ω)
  - lux: 光照度值(可能为None，表示超出对照表范围)

### `read_volt()`

读取并返回ADC原始电压值。

**返回值:**

- 电压值，单位为毫伏(mV)

### `r2i(resis)`

将电阻值转换为光照度(lux)。

**参数:**

- resis: 电阻值(Ω)

**返回值:**

- 光照度值(lux)或None(超出对照表范围)

## 应用示例

```python
from misc import ADC
from gl5528 import Gl5528
import utime as time

# 初始化传感器
adc = ADC()
ldr = Gl5528(adc, ADC.ADC0)

# 持续监测光照强度
while True:
    resistance, lux = ldr.read()
    
    if lux:
        print("当前环境 - 电阻值: {}Ω, 光照度: {}lux".format(resistance, lux))
    else:
        print("当前环境 - 电阻值: {}Ω (超出测量范围)".format(resistance))
    
    # 根据光照度控制逻辑
    if lux and lux > 500:
        print("强光环境")
    elif lux and lux < 100:
        print("弱光环境")
    
    time.sleep(1)
```

## 技术说明

1. **电阻值计算**基于特定分压电路配置：
   - 4.7kΩ电阻(R1)
   - 40.2kΩ电阻(R2)
   - 3.3V供电电压
2. **光照度转换**使用预设的电阻-照度对照表(o2i_table)，包含400Ω-820Ω范围内的精确对应关系
3. **典型应用场景**：
   - 室内光照监测
   - 自动照明控制
   - 环境光感应设备
4. **测量范围**：
   - 电阻范围：约400Ω-82kΩ
   - 照度范围：1-1300lux(取决于对照表)

## 常见问题排查

1. **读数不稳定**：
   - 检查电路连接是否可靠
   - 确保供电电压稳定
   - 避免传感器直接暴露在闪烁光源下
2. **返回None值**：
   - 确认电阻值是否在400Ω-82kΩ范围内
   - 检查ADC配置是否正确
3. **精度问题**：
   - 如需更高精度，可扩展o2i_table对照表
   - 考虑使用更高精度的ADC模块

本驱动为GL5528光敏电阻提供了完整的接口，特别适合需要同时获取电阻值和光照度的应用场景。
