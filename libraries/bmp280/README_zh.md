# BMP280 温压传感器驱动文档

## 一、概述

本文提供了基于 QuecPython 的 BMP280 系列 I2C 接口温压传感器驱动类`BMP280`。BMP280 是一款高精度、低功耗的温度和气压传感器，支持通过 I2C 总线通信，适用于气象监测、海拔计算等场景。该驱动类封装了 BMP280 的底层 I2C 通信协议、传感器初始化流程、原始数据读取及校准补偿算法，方便在 QuecPython 环境中快速获取高精度的温度和气压数据。

## 二、核心类与方法详解

### 1. 类初始化 `__init__(self, i2c, slaveaddr)`

功能：初始化 BMP280 驱动类，关联 I2C 总线设备并设置传感器 I2C 地址。
参数：

- `i2c`：I2C 总线设备（如`machine.I2C(I2C.I2C0, I2C.STANDARD_MODE)`），需为`machine.I2C`类型。
- `slaveaddr`：BMP280 的 I2C 从机地址（默认值为`0x76`，对应常量`BMP280_ADDR`）。

说明：该类继承自`I2CIOWrapper`，复用其 I2C 读写方法实现与传感器的底层通信。

### 2. 基础 I2C 通信方法（继承自`I2CIOWrapper`）

以下方法为 I2C 协议的底层实现，支撑传感器寄存器的读写操作，无需用户直接调用：

#### `read(self, addr, size=1, delay=0)`

功能：从指定寄存器地址读取数据。
参数：

- `addr`：寄存器地址（如`b'\xF7'`，表示读取温压原始数据寄存器）。
- `size`：读取数据的字节数（默认 1 字节）。
- `delay`：读取前的延迟时间（单位：ms，默认 0）。
  返回值：字节数组（`bytearray`），包含读取的寄存器数据。
  异常：若读取失败，抛出`I2CIOWrapper.I2CReadError`。

#### `write(self, addr, data)`

功能：向指定寄存器地址写入数据。
参数：

- `addr`：寄存器地址（如`b'\xF4'`，表示模式配置寄存器）。
- `data`：待写入的数据（需为`bytes`或`bytearray`类型，如`b'\x27'`表示配置为正常模式）。
  异常：若写入失败，抛出`I2CIOWrapper.I2CWriteError`。

### 3. 寄存器读写辅助方法（内部使用）

#### `read_word(self, reg)`

功能：从指定寄存器读取 16 位无符号整数。
参数：`reg`：寄存器起始地址（如`b'\x88'`，对应温度校准系数`dig_T1`）。
返回值：16 位无符号整数（通过高低字节拼接得到）。

#### `read_sword(self, reg)`

功能：从指定寄存器读取 16 位有符号整数。
参数：`reg`：寄存器起始地址（如`b'\x8A'`，对应温度校准系数`dig_T2`）。
返回值：16 位有符号整数（自动处理符号位，超过 32767 时转换为负值）。

### 4. 核心功能方法

#### `init(self)`

功能：初始化 BMP280 传感器，完成复位、设备验证、校准数据读取及工作模式配置。
流程：

1. 传感器复位：向复位寄存器（`BMP280_RESET_ADDR = b'\xE0'`）写入复位值（`BMP280_RESET_VALUE = b'\xB6'`），并等待 1 秒稳定。
2. 设备 ID 验证：读取 ID 寄存器（`BMP280_ID_ADDR = b'\xD0'`），若值不等于`BMP280_ID = 0x58`，抛出`ValueError`。
3. 读取校准数据：调用`_read_calibration()`获取传感器出厂校准系数（用于数据补偿）。
4. 配置工作模式：默认配置为正常模式（向模式寄存器`b'\xF4'`写入`b'\x27'`），若配置失败则自动切换为强制模式（写入`b'\x01'`）。

#### `_read_calibration(self)`

功能：读取传感器内置的校准系数（存储于非易失性存储器），用于温度和气压的补偿计算。
说明：校准系数包括温度相关（`dig_T1`-`dig_T3`）和气压相关（`dig_P1`-`dig_P9`），共 11 个参数，分别从固定寄存器地址（`0x88`-`0x9E`）读取并存储为类属性。

#### `is_measuring(self)`

功能：检查传感器是否正在进行温压测量。
返回值：`True`表示测量中，`False`表示测量完成。
说明：通过读取状态寄存器（`b'\xF3'`）的第 3 位（`0x08`）判断测量状态。

#### `read_raw_data(self)`

功能：读取未经补偿的原始温度和气压数据。
流程：

1. 等待测量完成（通过`is_measuring()`判断，未完成则每 10ms 轮询一次）。
2. 从数据寄存器（`b'\xF7'`）读取 6 字节数据，其中前 3 字节为气压原始值，后 3 字节为温度原始值。
3. 对原始数据进行移位处理（右移 4 位，去除低 4 位无效数据）。
   返回值：元组`(raw_temp, raw_press)`，分别为原始温度和气压值。

#### `compensate_temperature(self, raw_temp)`

功能：将原始温度数据转换为实际温度值（℃），基于校准系数进行补偿计算。
参数：`raw_temp`：通过`read_raw_data()`获取的原始温度值。
返回值：浮点型温度值（单位：℃）。
说明：补偿过程基于芯片 datasheet 提供的算法，通过`dig_T1`-`dig_T3`计算，并将中间结果`t_fine`存储为类属性（用于气压补偿）。

#### `compensate_pressure(self, raw_press)`

功能：将原始气压数据转换为实际气压值（hPa），基于校准系数和温度补偿结果`t_fine`进行计算。
参数：`raw_press`：通过`read_raw_data()`获取的原始气压值。
返回值：浮点型气压值（单位：hPa）。
说明：补偿过程基于芯片 datasheet 提供的复杂算法，通过`dig_P1`-`dig_P9`和`t_fine`计算，最终转换为百帕（hPa）单位。

#### `read_data(self)`

功能：一站式获取补偿后的温度和气压值。
流程：调用`read_raw_data()`获取原始数据，分别通过`compensate_temperature()`和`compensate_pressure()`计算实际值。
返回值：元组`(temp, press)`，分别为温度（℃）和气压（hPa）。

## 三、使用示例

### 示例：初始化传感器并循环读取温压数据

```python
from machine import I2C
import utime
from bmp280_driver import BMP280  # 假设脚本保存为bmp280_driver.py

# 初始化I2C总线（使用I2C0，标准模式）
i2c_dev = I2C(I2C.I2C0, I2C.STANDARD_MODE)

# 初始化BMP280传感器（地址0x76）
sensor = BMP280(i2c_dev, BMP280_ADDR)
sensor.init()  # 完成传感器初始化

try:
    while True:
        # 读取补偿后的温压数据
        temp, press = sensor.read_data()
        
        # 打印数据（保留2位小数）
        print("--------------------------------------------------")
        print(f"Temperature: {temp:.2f} °C")
        print(f"Pressure: {press:.2f} hPa")
        print("")
        
        # 间隔3秒读取一次
        utime.sleep(3)

except KeyboardInterrupt:
    print("Program stopped")
```

## 四、常量说明

| 常量名               | 值        | 说明                       |
| -------------------- | --------- | -------------------------- |
| `BMP280_ADDR`        | `0x76`    | BMP280 的 I2C 从机地址     |
| `BMP280_ID`          | `0x58`    | BMP280 的设备 ID（固定值） |
| `BMP280_ID_ADDR`     | `b'\xD0'` | 设备 ID 寄存器地址         |
| `BMP280_RESET_ADDR`  | `b'\xE0'` | 复位寄存器地址             |
| `BMP280_RESET_VALUE` | `b'\xB6'` | 复位命令值                 |
| `BMP280_MODE_ADDR`   | `b'\xF4'` | 工作模式配置寄存器地址     |