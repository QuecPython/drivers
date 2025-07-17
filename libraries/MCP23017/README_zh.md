# MCP23017 I/O扩展器示例代码说明文档

## 概述

本文档介绍如何使用基于QuecPython的MCP23017 I/O扩展器进行GPIO扩展和控制。MCP23017是一款16位I/O扩展器，通过I2C接口提供额外的GPIO端口，适用于需要扩展I/O能力的各种应用场景。

## 硬件连接

在使用MCP23017模块前，请确保正确连接硬件：

- I2C接口连接（SCL/SDA）
- VCC连接至3.3V或5V电源（根据模块要求）
- GND接地
- A0/A1/A2地址选择引脚（根据需要接地或接VCC）
- RESET引脚（通常接VCC）
- INT引脚（可选中断功能）

## 快速开始

### 1. 初始化MCP23017模块

```python
from machine import I2C
from usr import mcp23017

# 初始化I2C接口
i2c = I2C(I2C.I2C1, I2C.STANDARD_MODE)
# 初始化MCP23017扩展器（默认地址0x20）
mcp = mcp23017.Mcp23017(i2c)
print("MCP23017模块初始化完成")
```

### 2. 基本功能使用

#### 配置输入引脚

```python
# 配置GPIO0为输入模式
mcp.pin(0, mode=1)  # mode=1表示输入
# 配置GPIO1为输入模式并启用上拉电阻
mcp.pin(1, mode=1, pullup=True)
```

#### 配置输出引脚

```python
# 配置GPIO2为输出模式并设置高电平
mcp.pin(2, mode=0, value=1)  # mode=0表示输出
# 配置GPIO3为输出模式并设置低电平
mcp.pin(3, mode=0, value=0)
```

## 高级功能

### 1. 端口级操作

```python
# 配置整个PORTA为输出
mcp.porta.mode = 0x00  # 0=输出
# 设置PORTA所有引脚输出高电平
mcp.porta.gpio = 0xFF

# 配置整个PORTB为输入并启用上拉
mcp.portb.mode = 0xFF  # 1=输入
mcp.portb.pullup = 0xFF
```

### 2. 中断功能

```python
# 配置GPIO4为输入并启用中断
mcp.pin(4, mode=1, interrupt_enable=1)

while True:
    # 检查PORTA中断
    if mcp.porta.interrupt_flag:
        print("PORTA中断触发")
        # 读取中断时的引脚状态
        captured = mcp.interrupt_captured_gpio(0)
        print(f"捕获值: {captured:08b}")
    
    # 检查PORTB中断
    if mcp.portb.interrupt_flag:
        print("PORTB中断触发")
        captured = mcp.interrupt_captured_gpio(1)
        print(f"捕获值: {captured:08b}")
    
    utime.sleep_ms(100)
```

## 类和方法参考

**I2C接口[参考](https://developer.quectel.com/doc/quecpython/API_reference/zh/peripherals/machine.I2C.html)**

### `Mcp23017` 类

#### 构造函数

python

```python
Mcp23017(i2c, address=0x20, bank=1)
```

- `i2c`: I2C总线对象
- `address`: 设备I2C地址（默认0x20）
- `bank`: 寄存器组模式（0=交替，1=分组）

#### 主要方法

- `pin(pin, **kwargs)`: 配置单个引脚
  - `pin`: 引脚编号（0-15）
  - `mode`: 方向（0=输出，1=输入）
  - `value`: 输出值（0/1）
  - `pullup`: 上拉使能（True/False）
  - `interrupt_enable`: 中断使能（0/1）
- `interrupt_triggered_gpio(port)`: 获取触发中断的GPIO
- `interrupt_captured_gpio(port)`: 获取中断捕获值

#### 端口属性

- `porta`: PORTA端口对象
- `portb`: PORTB端口对象

### `Port` 类（porta/portb）

#### 主要属性

- `mode`: 端口方向（0=输出，1=输入）
- `pullup`: 上拉使能
- `gpio`: GPIO值
- `interrupt_flag`: 中断标志（只读）
- `interrupt_captured`: 中断捕获值（只读）

## 示例代码

```python
from machine import I2C
from usr import mcp23017
import utime

def mcp23017_test():
    # 初始化I2C和MCP23017
    i2c = I2C(I2C.I2C1, I2C.STANDARD_MODE)
    mcp = mcp23017.Mcp23017(i2c, address=0x20)
    
    # 基本引脚配置
    mcp.pin(0, mode=1)  # GPIO0输入
    mcp.pin(1, mode=1, pullup=True)  # GPIO1输入带上拉
    mcp.pin(2, mode=0, value=1)  # GPIO2输出高
    mcp.pin(3, mode=0, value=0)  # GPIO3输出低
    
    # 端口操作示例
    mcp.porta.mode = 0x0F  # 低4位输入，高4位输出
    mcp.porta.gpio = 0xF0  # 高4位输出高电平
    
    # 中断示例
    mcp.pin(4, mode=1, interrupt_enable=1)
    
    while True:
        if mcp.porta.interrupt_flag:
            print("中断触发!")
            print("捕获值:", mcp.interrupt_captured_gpio(0))
        utime.sleep_ms(100)

if __name__ == "__main__":
    mcp23017_test()
```

## 注意事项

1. 确保I2C地址配置正确（A0/A1/A2引脚状态）
2. 输出引脚不要直接驱动大电流负载
3. 中断引脚需要正确配置上拉/下拉电阻
4. 注意寄存器组模式（bank参数）对寄存器地址的影响
5. 输入引脚建议启用上拉或下拉电阻

## 故障排除

1. **无法通信**：
   - 检查I2C连接和地址
   - 验证电源电压
   - 确认RESET引脚状态
2. **中断不工作**：
   - 检查INT引脚连接
   - 验证中断配置参数
   - 确认中断极性设置
3. **引脚状态异常**：
   - 检查模式配置（输入/输出）
   - 验证上拉电阻设置
   - 检查是否有短路或过载

## 寄存器参考

| 寄存器  | 地址 | 描述             |
| :------ | :--- | :--------------- |
| IODIR   | 0x00 | I/O方向          |
| IPOL    | 0x01 | 输入极性         |
| GPINTEN | 0x02 | 中断使能         |
| DEFVAL  | 0x03 | 默认值           |
| INTCON  | 0x04 | 中断控制         |
| IOCON   | 0x05 | 配置             |
| GPPU    | 0x06 | 上拉电阻使能     |
| INTF    | 0x07 | 中断标志（只读） |
| INTCAP  | 0x08 | 中断捕获（只读） |
| GPIO    | 0x09 | 通用I/O          |
| OLAT    | 0x0A | 输出锁存器       |
