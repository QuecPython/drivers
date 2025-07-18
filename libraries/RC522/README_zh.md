# RC522 RFID模块示例代码说明文档

## 概述

本文档介绍如何使用基于QuecPython的RC522 RFID模块进行卡片读写操作。RC522是一种非接触式读写卡芯片，支持ISO14443A协议，常用于门禁系统、会员卡系统等场景。

## 硬件连接

在使用RC522模块前，请确保正确连接硬件：

- SPI接口连接
- RST引脚连接至GPIO12
- IRQ引脚连接至GPIO11（可选中断功能）

## 快速开始

### 1. 初始化RC522模块

```python
from mfrc522 import Mfrc522_spi
reader = Mfrc522_spi(pin_rst=Pin.GPIO12, pin_irq=Pin.GPIO11)
print("RC522模块初始化完成")
```

### 2. 基本功能使用

#### 读取卡片ID

```python
card_id = reader.read_id()
print('检测到卡片ID: {0}'.format(card_id))
```

#### 写入数据到卡片

```python
# 定义要写入的数据块地址和数据
blockAddr = 0x01  # 块地址
data = [0x00,0x0A,0x10,0x00,0x0C,0x00,0xA0,0x05,0x00,0x40,0x40,0x00,0x10,0x20]

# 执行写入操作
reader.Mfrc522_Write(blockAddr, data)
print("数据写入完成")
```

#### 从卡片读取数据

```python
# 从指定块地址读取数据
read_data = reader.Mfrc522_Read(blockAddr)
print('读取到的数据: {0}'.format(read_data))
```

## 高级功能

### 1. 中断模式

模块支持中断模式检测卡片，初始化时传入irq_cb参数可设置自定义中断回调函数：

```python
def my_callback(para):
    print("检测到卡片接近!")
    card_id = reader.read_id_no_block()
    if card_id:
        print("卡片ID:", card_id)

reader = Mfrc522_spi(pin_rst=Pin.GPIO12, pin_irq=Pin.GPIO11, irq_cb=my_callback)
```

### 2. 多块读写

模块支持连续读写多个数据块：

```python
# 定义多个块地址
block_addrs = [8, 9, 10]

# 写入长文本数据（自动分配到多个块）
text_data = "这是一段要存储的长文本数据"
reader.write(text_data)

# 读取多块数据
id, read_text = reader.read()
print("读取到的文本:", read_text)
```

## 注意事项

1. 文中GPIO口仅为参考，具体接口请参考实际所用开发板说明手册
2. 确保RFID模块供电稳定
3. 不同卡片类型的存储结构可能不同，请参考相应卡片规格
4. 某些块可能是密钥块或控制块，写入前请确认
5. 读写操作需要验证密钥，默认密钥为[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

## 故障排除

1. **无法检测到卡片**：
   - 检查天线连接
   - 确认卡片类型为ISO14443A
   - 调整卡片与模块的距离
2. **读写失败**：
   - 检查卡片是否可写
   - 确认块地址正确
   - 验证密钥是否正确
3. **通信错误**：
   - 检查SPI连接
   - 确认RST引脚配置正确
   - 确保模块供电正常

## API参考

### 主要方法

- `read_id()`: 读取卡片ID（阻塞式）
- `read_id_no_block()`: 读取卡片ID（非阻塞式）
- `read()`: 读取卡片数据（阻塞式）
- `read_no_block()`: 读取卡片数据（非阻塞式）
- `write(text)`: 写入文本数据（阻塞式）
- `write_no_block(text)`: 写入文本数据（非阻塞式）
- `Mfrc522_Read(blockAddr)`: 读取指定块数据
- `Mfrc522_Write(blockAddr, writeData)`: 写入数据到指定块

## 示例代码

完整测试代码：

```python
import _thread
from mfrc522 import Mfrc522_spi
import utime

def rc522_test():
    reader = Mfrc522_spi(pin_rst=Pin.GPIO12, pin_irq=Pin.GPIO11)
    print("init finish.")
    blockAddr = 0x01
    data = [0x00,0x0A,0x10,0x00,0x0C,0x00,0xA0,0x05,0x00,0x40,0x40,0x00,0x10,0x20]
    reader.Mfrc522_Write(blockAddr,data)
    read_data = reader.Mfrc522_Read(blockAddr)
    #id = reader.read_id()
    print('card id is {0}'.format(read_data))
    utime.sleep_ms(200)

# 在新线程中运行测试
_thread.start_new_thread(rc522_test, ())
```

## 版本信息

- 当前版本：v1.0
- 最后更新：2023-10-15
- 适用平台：QuecPython

如需更多帮助，请参考模块完整源代码或联系技术支持。