# MCP2515 CAN总线通信示例解析

## 类和方法

### `MCP2515` 类

#### 构造函数

```python
MCP2515(can_id, tx_pin, baudrate, rx_buffer_size)
```

- `can_id`: CAN控制器ID（这里使用0）
- `tx_pin`: 发送引脚（示例中使用Pin.GPIO21）
- `baudrate`: 波特率（示例中为500kbps）
- `rx_buffer_size`: 接收缓冲区大小（示例中为512字节）

#### 主要方法

1. `get_frame_number()`
   - 功能: 获取当前接收缓冲区中待处理的CAN帧数量
   - 参数: 无
   - 返回值: 待处理的CAN帧数量（整数）
2. `read(frame_num)`
   - 功能: 从接收缓冲区读取指定数量的CAN帧
   - 参数:
     - `frame_num`: 要读取的帧数量
   - 返回值: 读取到的CAN帧数据（具体格式依赖于库的实现）
3. `write(id, ext, rtr, data)`
   - 功能: 发送一帧CAN数据
   - 参数:
     - `id`: CAN消息的ID（示例中为0x6FF）
     - `ext`: 扩展帧标志（示例中为0，表示标准帧）
     - `rtr`: 远程传输请求标志（示例中为0，表示数据帧）
     - `data`: 要发送的数据（字节类型）

## 示例代码解析

### 1. 导入模块

```python
import MCP2515            # 导入MCP2515驱动
import utime              # 导入时间模块
import _thread            # 导入线程模块
from machine import Pin   # 导入Pin类
```

### 2. 全局变量初始化

```python
mcp2515 = MCP2515(0, Pin.GPIO21, 500, 512)  # 初始化MCP2515对象
can_frame_cnt = 0                            # 记录接收到的总帧数
```

### 3. CAN帧读取线程函数

```python
def read_can_frame_thread():
    while True:
        frame_num = mcp2515.get_frame_number()  # 获取待处理帧数量
        if frame_num > 0:
            can_data = mcp2515.read(frame_num)  # 读取所有待处理帧
            global can_frame_cnt
            can_frame_cnt = can_frame_cnt + frame_num  # 累加接收帧数
            print("can_frame_cnt: {}".format(can_frame_cnt))
        utime.sleep_ms(100)  # 每100ms检查一次
```

### 4. 主程序

```python
if __name__ == "__main__":
    # 启动CAN帧读取线程
    _thread.start_new_thread(read_can_frame_thread, ())
    send_cnt = 0
    while True:
        if send_cnt < 1000:
            # 构造发送数据：两个字节，高位在前
            send_bytearr = bytearray(2)
            send_bytearr[1] = send_cnt & 0xff         # 低字节
            send_bytearr[0] = (send_cnt >> 8) & 0xff  # 高字节
            
            # 发送CAN帧（ID:0x6FF，标准帧，数据帧）
            mcp2515.write(0x6FF, 0, 0, bytes(send_bytearr))
            utime.sleep_ms(500)  # 每500ms发送一帧
            send_cnt = send_cnt + 1
        else:
            print("send finish,cnt:", send_cnt)
            break
```

## 工作流程

1. 初始化MCP2515对象，设置CAN通信参数
2. 启动独立线程处理CAN帧接收
3. 主线程循环发送1000帧CAN数据
4. 接收线程持续检查并处理接收到的CAN帧
5. 发送完成后退出主循环

## 注意事项

1. 使用多线程处理接收和发送，避免阻塞主程序
2. 数据格式采用大端序（高位在前，低位在后）
3. 接收线程定时检查一次缓冲区
4. 发送间隔根据实际需求调整
5. 确保硬件连接正确
6. 波特率需与通信对方一致
7. 接收缓冲区大小根据通信负载调整