# GNSS定位模块驱动文档
## 概述

本文档介绍如何使用GNSS定位模块驱动获取卫星定位数据。该驱动支持多种定位数据获取功能，包括位置、速度、海拔、可见卫星等关键定位信息。
## 主要特性
- 获取原始GNSS数据（GGA/RMC/GSV格式）
- 定位状态检测
- 获取精确的经纬度坐标
- 测量海拔高度和移动速度
- 可见卫星信息统计
- 定位时间获取
- 支持多种定位模式识别

## 快速入门
### 1. 导入所需模块
```python
from gnss import Gnss
import utime
```
### 2. 初始化GNSS模块

```python
# UART1初始化GNSS模块（波特率9600）
gnss = Gnss(
    uartn=1,        # UART端口号
    baudrate=9600,  # 波特率
    databits=8,     # 数据位
    parity=0,       # 校验位
    stopbits=1,     # 停止位
    flowctl=0       # 流控
)
```

### 3. 获取定位数据

```python
# 获取定位信息
if gnss.isFix():
    location = gnss.getLocation()
    print("经纬度: {}{}, {}{}".format(location[0], location[1], location[2], location[3]))
else:
    print("尚未定位成功，请等待...")
```

## API接口说明

**`Gnss(uartn, baudrate, databits, parity, stopbits, flowctl)`**

构造函数，初始化GNSS模块。

**​​参数说明:​​**

- uartn: UART端口号 (1, 2等)
- baudrate: 通信波特率 (默认9600)
- databits: 数据位 (通常为8)
- parity: 校验位 (0-无校验, 1-奇校验, 2-偶校验)
- stopbits: 停止位 (1或2)
- flowctl: 流控 (0-无流控)

**`read_gnss(retry=1, debug=0)`**

读取原始GNSS数据。

​​**参数说明:​​**

- retry: 读取重试次数
- debug: 调试模式开关

​**​返回值:​​**

- 成功: (data_valid, data)
- 其中data_valid为有效位标识：
    - 0x04: GGA有效
    - 0x02: RMC有效
    - 0x01: GSV有效
- 失败: -1

**`isFix()`**

检查是否定位成功。

​**​返回值:​​**

- 1: 定位成功
- 0: 尚未定位

**`getUtcTime()`**

获取定位的UTC时间。

​**​返回值:​​**

- 成功: UTC时间字符串 (格式为"HHMMSS.SS")
- 失败: -1

**`getLocationMode()`**

获取定位模式。

​​**返回值:​​**

- -1: 获取失败
- 0: 定位不可用或无效
- 1: GPS/SPS模式 (标准定位)
- 2: DGPS/DSPS模式 (差分定位)
- 6: 估算模式 (航位推算)

**`getUsedSateCnt()`**

获取定位使用的卫星数量。

​**​返回值:​​**

- 成功: 使用卫星数量
- 失败: -1

**`getLocation()`**

获取精确的经纬度信息。

​**​返回值:​​**

- 成功: (longitude, lon_direction, latitude, lat_direction)
    - longitude: 经度值 (浮点数)
    - lon_direction: 经度方向 ('E'或'W')
    - latitude: 纬度值 (浮点数)
    - lat_direction: 纬度方向 ('N'或'S')
- 失败: -1

**`getViewedSateCnt()`**

获取可见卫星数量。

​​**返回值:**

- 成功: 可见卫星数量
- 失败: -1

**`getGeodeticHeight()`**

获取海拔高度。

​​**返回值:**

- 成功: 海拔高度 (单位: 米)
- 失败: -1

**`getCourse()`**

获取可见卫星的方位角。

​​**返回值：**​

- 成功: 字典格式的卫星方位角数据，key为卫星编号，value为方位角
- 失败: -1

**`getSpeed()`**

获取对地速度。

​**​返回值:​​**

- 成功: 对地速度 (单位: km/h)
- 失败: -1

## 应用示例
基本定位应用
```python
gnss = Gnss(1, 9600, 8, 0, 1, 0)

while True:
    if gnss.isFix():
        # 获取位置信息
        lon, lon_dir, lat, lat_dir = gnss.getLocation()
        height = gnss.getGeodeticHeight()
        speed = gnss.getSpeed()
        
        print("位置: {:.6f}{}, {:.6f}{}".format(lat, lat_dir, lon, lon_dir))
        print("海拔: {}米, 速度: {}km/h".format(height, speed))
    else:
        used_sats = gnss.getUsedSateCnt()
        visible_sats = gnss.getViewedSateCnt()
        print("定位中... 使用卫星: {}, 可见卫星: {}".format(used_sats, visible_sats))
    
    utime.sleep(1)
```


卫星信息分析
```python
gnss = Gnss(1, 9600, 8, 0, 1, 0)

def analyze_satellites():
    while not gnss.isFix():
        utime.sleep(1)
    
    # 获取卫星方位角信息
    satellite_data = gnss.getCourse()
    visible_sats = gnss.getViewedSateCnt()
    
    print("共可见 {} 颗卫星:".format(visible_sats))
    for sat_id, azimuth in satellite_data.items():
        print("卫星 {}: 方位角 {}°".format(sat_id, azimuth))

analyze_satellites()
```


## 常见问题排查
### 长时间无法定位

- ​可能原因:​​
    - 天线接触不良或损坏
    - 定位模块未上电
    - 当前环境卫星信号差



