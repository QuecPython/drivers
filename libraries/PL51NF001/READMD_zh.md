# PL5NF001传感器驱动文档
## 概述

本文档介绍如何使用PL5NF001传感器驱动模块实现基于GPIO模拟I2C协议的通信功能。该驱动提供了完整的I2C通信时序控制，支持开始信号、停止信号、数据读写等基本操作。

## 主要特性

- GPIO模拟I2C通信协议
- 支持标准I2C时序控制
- 完整的开始/停止信号实现
- ACK/NACK应答机制
- 字节读写功能
- 灵活的延时控制

## 快速入门
### 1. 初始化传感器
```python
from pl5nf001 import PL5NF001

# 初始化PL5NF001传感器
sensor = PL5NF001()
```

### 2. 基本通信操作
```python
# 发送开始信号
sensor.start_signal()

# 写入数据字节
sensor.write_data(0x55)

# 等待ACK应答
if sensor.wait_ack() == 0:
    print("收到ACK应答")
else:
    print("未收到ACK应答")

# 读取数据字节
data = sensor.read_byte(ack=1)  # 读取后发送ACK
print("读取到数据: 0x{:02X}".format(data))

# 发送停止信号
sensor.stop_signal()
```
## API接口说明

**`PL5NF001()`**

构造函数，初始化PL5NF001传感器。

**`start_signal()`**

发送I2C开始信号。

**`stop_signal()`**

发送I2C停止信号。

**`ack()`**

发送ACK应答信号。

**`nack()`**

发送NACK应答信号。

**`wait_ack()`**

等待从设备发送ACK应答。

​​**返回值:**

- 0: 收到ACK
- 1: 超时未收到ACK

**`write_data(data)`**

向从设备写入一个字节数据。

​​**参数说明:**

- data: 要写入的数据字节（0-255）

**`read_byte(ack)`**

从从设备读取一个字节数据。

​**​参数说明:**

- ack: 读取后是否发送ACK
    - 1: 发送ACK
    - 0: 发送NACK

- ​​返回值:​​

    - 读取到的数据字节

## 应用示例
基本读写操作
```python
sensor = PL5NF001()

# 启动通信
sensor.start_signal()

# 写入设备地址
sensor.write_data(0x48)
if sensor.wait_ack() != 0:
    print("设备无响应")
    return

# 写入寄存器地址
sensor.write_data(0x01)
sensor.wait_ack()

# 读取数据
data = sensor.read_byte(ack=0)  # 最后字节发送NACK

# 结束通信
sensor.stop_signal()

print("读取到寄存器值: 0x{:02X}".format(data))
```

多字节读取
```python
def read_multiple_bytes(sensor, address, reg, count):
    sensor.start_signal()
    
    # 写入设备地址 + 写模式
    sensor.write_data(address << 1)
    if sensor.wait_ack() != 0:
        return None
    
    # 写入寄存器地址
    sensor.write_data(reg)
    sensor.wait_ack()
    
    # 重新开始
    sensor.start_signal()
    
    # 写入设备地址 + 读模式
    sensor.write_data((address << 1) | 1)
    sensor.wait_ack()
    
    # 读取数据
    data = []
    for i in range(count):
        ack = 1 if i < count-1 else 0  # 最后字节发送NACK
        data.append(sensor.read_byte(ack))
    
    sensor.stop_signal()
    return data

# 读取3个字节数据
sensor = PL5NF001()
result = read_multiple_bytes(sensor, 0x48, 0x00, 3)
print("读取到数据: {}".format(result))
``` 

## 常见问题排查
|问题现象|可能原因|
|----|----|
无法收到ACK	|设备地址错误
读取数据全为0|	设备未初始化
通信不稳定	|时序参数不匹配
数据错误|	时序混乱
无法产生开始/停止信号|	GPIO配置错误