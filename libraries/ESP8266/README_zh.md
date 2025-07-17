# ESP8266 WiFi模块驱动文档
## 概述

本文档介绍如何使用ESP8266 WiFi模块驱动实现物联网设备的无线连接功能。该驱动通过SLIP协议和TLV数据格式与ESP8266模块通信，支持创建WiFi接入点（AP）和连接移动数据网络。

## 主要特性
- WiFi接入点配置：支持自定义SSID和密码
- 自动路由配置：实现网络间无缝通信
- 模块化管理：简洁的AP配置和工作模式控制
- 错误处理机制：完善的异常检测和处理

## 快速入门
### 1. 导入所需模块

```python
from machine import UART
from esp8266_ap import Esp8266_ap
import utime
```

### 2. 初始化ESP8266模块
```python
# 使用UART2接口初始化ESP8266模块
esp = Esp8266_ap(UART.UART2)
```
### 3. 设置WiFi接入点
```python
# 配置WiFi接入点（SSID：MyAP，密码：12345678）
esp.set_ap(name='MyAP', pwd='12345678')
```

### 4. 启用WiFi功能

```python
# 启用WiFi模块并完成网络配置
if esp.wifi_on() == 0:
    print('WiFi模块启动成功')
    # 这里可以添加设备联网后的业务逻辑
    while True:
        utime.sleep(10)
else:
    print('WiFi模块启动失败')
```
## API接口说明

**`Esp8266_ap(uart)`**

构造函数，初始化ESP8266模块。

​​**参数说明:**

- uart: UART接口实例

**`set_ap(name=None, pwd=None, project_name='wifi_setap', project_version='1.0.0')`**


配置WiFi接入点参数。

​**参数说明:​​**

- name: WiFi接入点名称（SSID）
- pwd: WiFi接入点密码
- project_name: 项目名称（用于网络检测）
- project_version: 项目版本（用于网络检测）

​**​返回值:​​**

- 0: 成功
- -1: 失败

**`wifi_on()`**

启用WiFi功能并配置网络。

​​**返回值:​​**

- 0: 成功
- -1: 失败

**`wifi_off()`**

关闭WiFi功能，释放资源

## 应用示例
基础WiFi接入点配置
```python
# 设置自定义SSID和密码
esp.set_ap(name='Quectel_WiFi', pwd='SecurePass123')
```
无密码开放式AP
```python
# 创建无密码开放式接入点
esp.set_ap(name='Free_WiFi_Access')
```
仅密码保护的AP
```python
# 创建使用密码保护但隐藏SSID的接入点
esp.set_ap(pwd='HiddenNetworkPass')
```
多网络协作应用
```python
esp = Esp8266_ap(UART.UART2)
esp.set_ap(name='IoT_Gateway', pwd='iot12345')

if esp.wifi_on() == 0:
    print('设备已连接到移动网络和WiFi网络')
    
    while True:
        # 这里可以添加同时访问双网络的业务逻辑
        # 例如：通过移动网络上报数据，通过本地WiFi管理设备
        utime.sleep(60)
```
网络健康监测
```python
import ujson

def network_health_check():
    # 检查网络状态
    esp_info = esp._wait_datacall_success()
    return ujson.dumps(esp_info)

esp.set_ap(name='Network_Monitor')
esp.wifi_on()

# 定期上报网络状态
while True:
    status = network_health_check()
    print("当前网络状态: {}".format(status))
    utime.sleep(300)
```

## 技术说明
### 1. SLIP协议使用

- 串行线路接口协议（Serial Line IP）
- 工作在UART通信基础上
- 协议类型: SLIP_INNER（内部网络）

### 2. TLV数据格式
|字段|长度|说明|
|----|----|----|
|头部|2字节|标识数据类型（F1/F2/F3）|
|长度|4字节|数据内容长度（0000-9999）|
|内容|变长|实际配置数据|

​​**头部说明:​**​

- F1: 仅密码模式
- F2: 仅SSID模式
- F3: SSID+密码完整模式

### 3. 路由配置

- 默认网关: 172.16.1.2
- AP地址段: 192.168.4.0/24
- 子网掩码: 255.255.255.0

## 网络配置参数
### 1. 默认服务器

- IP地址: 172.16.1.5
- 端口号: 1000

### 2. 设备绑定地址

- IP地址: 172.16.1.2
- 端口号: 10001

### 3. 移动网络优先级
|网络类型|优先级|
|----|----|
|LTE/5G|高|
|WiFi|	中|
|有线网络|低|

## 常见问题排查
### 1. 初始化失败

- ​​现象​​: slip netif construct fail错误
- ​​解决方案​​:
    - 检查UART接线是否正确（TX/RX交叉连接）
    - 确认UART波特率设置一致（通常115200）
    - 验证ESP8266模块供电是否稳定

### 2. AP配置失败

- ​现象​​: fail to set ap错误
- ​​解决方案​​:
    - 检查网络连接状态checkNet.wait_network_connected()
    - 确认服务器地址可达（172.16.1.5）
    - 验证SSID和密码长度（SSID:1-32字符，密码:8-64字符）

### 3. 网络路由异常

- ​​现象​​: 无法同时访问双网络
- ​​解决方案​​:
    - 确认调用wifi_on()后的返回值为0
    - 检查路由表是否包含192.168.4.0/24网段
    - 验证默认网关设置是否正确

### 4. 连接稳定性问题

- ​​现象​​: 连接频繁断开
- ​​解决方案​​:
    - 缩短设备与AP间的距离
    - 避免2.4GHz频段干扰（如微波炉、蓝牙设备）
    - 更新ESP8266固件到最新版本

​​连接状态监控​​:
```python
def check_connection():
    try:
        # 尝试访问服务器验证连接
        sock = usocket.socket()
        sock.connect(('172.16.1.5', 1000))
        return True
    except:
        return False
```
​​自动重连机制​​:
```python
    while True:
        if not check_connection():
            print('连接丢失，尝试重连...')
            esp.wifi_off()
            esp.set_ap(name='MyAP', pwd='password')
            esp.wifi_on()
        utime.sleep(60)
```
本驱动为ESP8266模块提供了完整的WiFi配置和管理方案
