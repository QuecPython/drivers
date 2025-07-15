# CH423 GPIO扩展器驱动脚本文档

## 一、概述

本脚本提供了基于QuecPython的CH423系列I2C接口GPIO扩展器驱动类`Ch423s`。CH423是一款通过I2C总线控制的通用I/O端口扩展器件，支持8位/16位GPIO输入输出配置、开漏输出模式、输入中断等功能。该驱动类封装了CH423的底层I2C通信协议及上层功能调用，方便在QuecPython环境中快速控制CH423芯片。

## 二、核心类与方法详解

### 1. 类初始化 `__init__(self, clk, dio)`

**功能**：初始化CH423芯片，配置时钟引脚（SCL）和数据引脚（SDA），并完成芯片复位。
​**​参数​**​：

- `clk`：连接CH423的时钟引脚（如`Pin.GPIO12`），需为`machine.Pin`类型。
- `dio`：连接CH423的数据引脚（如`Pin.GPIO13`），需为`machine.Pin`类型。

**说明**：
初始化时会通过I2C发送系统参数命令`CH423_SYS_CMD`（0x48）并将初始值设为0x00，完成芯片基本配置。

### 2. 基础I2C通信方法（内部使用）

以下方法为I2C协议的底层实现，无需用户直接调用：

#### `_start_signal(self)`

生成I2C起始信号：数据线先拉高，时钟拉高后数据拉低，时钟拉低完成起始。

#### `_stop_signal(self)`

生成I2C停止信号：时钟拉低后数据拉低，时钟拉高后数据拉高，完成停止。

#### `ack(self, is_ack)`

发送ACK/NACK信号：`is_ack=True`表示发送ACK（数据线拉低），`False`表示NACK（数据线保持高）。

#### `_wait_ack(self)`

等待从设备返回ACK响应：检测数据线电平，超时（>2000次循环）则报错并停止通信。

#### `_write_byte(self, data)`

通过I2C发送单字节数据：按高位到低位顺序逐位发送，每发送1位后时钟拉高并等待ACK。

#### `_read_byte(self)`

通过I2C读取单字节数据：逐位读取时钟拉高时的数据线电平，最后发送ACK信号。

### 3. 寄存器读写方法（内部使用）

#### `_read_reg(self, cmd)`

读取指定命令对应的寄存器值：通过I2C起始信号→发送命令→读取数据→停止信号的流程完成。

#### `_write_reg(self, cmd, val)`

向指定命令对应的寄存器写入值：通过I2C起始信号→发送命令→发送值→停止信号的流程完成。

### 4. 核心功能方法

#### `reset(self)`

**功能**：重置CH423芯片，恢复默认配置。
​**​实现​**​：调用`_write_reg`向系统参数命令寄存器（`CH423_SYS_CMD`）写入0x00。

#### `config(self, dir=GPIO_IN, int=0, odr=0)`

**功能**：配置GPIO方向、输入中断使能及开漏输出使能。
​**​参数​**​：

- `dir`：GPIO方向（0=输入，1=输出）。
- `int`：输入电平变化中断使能（0=禁用，1=启用）。
- `odr`：开漏输出使能（0=推挽输出，1=开漏输出）。

**说明**：
通过修改系统参数寄存器（`CH423_SYS_CMD`）实现配置，参数需为0或1，否则返回-1。

#### `gpio_pin(self, pin, value=1)`

**功能**：单独设置某一路GPIO引脚的电平（仅当GPIO为输出模式时有效）。
​**​参数​**​：

- `pin`：引脚编号（0-7，对应IO0-IO7）。
- `value`：目标电平（0=低电平，1=高电平）。

**说明**：
先读取当前GPIO状态（`read_gpio`），再根据`value`修改对应位后写回（`CH423_SET_IO_CMD`）。

#### `gpo_h(self, value)`

**功能**：设置高8位GPIO（IO8-IO15）的整体输出电平（仅当GPIO为输出模式时有效）。
​**​参数​**​：

- `value`：8位数值（0-255），每一位对应IO8-IO15的电平（1=高，0=低）。

**说明**：直接向高8位输出命令寄存器（`CH423_OC_H_CMD`）写入值。

#### `gpo_l(self, value)`

**功能**：设置低8位GPIO（IO0-IO7）的整体输出电平（仅当GPIO为输出模式时有效）。
​**​参数​**​：

- `value`：8位数值（0-255），每一位对应IO0-IO7的电平（1=高，0=低）。

**说明**：直接向低8位输出命令寄存器（`CH423_OC_L_CMD`）写入值。

#### `gpio(self, value)`

**功能**：整体设置8位GPIO（IO0-IO7）的输出电平（仅当GPIO为输出模式时有效）。
​**​参数​**​：

- `value`：8位数值（0-255），每一位对应IO0-IO7的电平（1=高，0=低）。

**说明**：等价于`gpo_l`，直接向低8位输出命令寄存器写入值。

#### `read_gpio(self)`

**功能**：读取当前GPIO引脚的状态（输入或输出模式均可）。
​**​返回值​**​：8位数值（0-255），每一位对应IO0-IO7的状态（1=高，0=低）。
​**​说明​**​：

- 若`BIT_IO_OE`（`CH423_SYS_CMD`的第0位）为0（推挽输入模式），读取的是引脚的实际输入电平。
- 若`BIT_IO_OE`为1（推挽输出/开漏输出模式），读取的是引脚的输出锁存值（非实时电平）。

## 三、使用示例

### 示例1：初始化与基础输出

```python
from machine import Pin
import utime
from ch423_driver import Ch423s  # 假设脚本保存为ch423_driver.py

# 初始化CH423，使用GPIO12（SCL）和GPIO13（SDA）
ch423 = Ch423s(Pin.GPIO12, Pin.GPIO13)
utime.sleep(1)  # 等待初始化完成

# 配置所有GPIO为输出模式（dir=1）
ch423.config(dir=1)
print("GPIO已设置为输出模式")

# 循环点亮第5号引脚（IO5）
for _ in range(10):
    ch423.gpio_pin(pin=5, value=1)  # IO5输出高电平
    utime.sleep(1)
    print("当前GPIO状态:", bin(ch423.read_gpio()))  # 打印所有GPIO状态（二进制）
    ch423.gpio(0x00)  # 所有GPIO输出低电平
    utime.sleep(1)
    print("当前GPIO状态:", bin(ch423.read_gpio()))  # 打印所有GPIO状态（二进制）
```

### 示例2：开漏输出模式

```python
# 配置所有GPIO为开漏输出模式（odr=1）
ch423.config(odr=1)
print("GPIO已设置为开漏输出模式")

# 设置高8位GPIO为0x0F（IO8-IO11输出高，IO12-IO15输出低）
ch423.gpo_h(0x0F)
# 设置低8位GPIO为0xF0（IO4-IO7输出高，IO0-IO3输出低）
ch423.gpo_l(0xF0)
utime.sleep(1)
print("开漏输出状态:", bin(ch423.read_gpio()))  # 输出锁存值（非实时电平）
```

