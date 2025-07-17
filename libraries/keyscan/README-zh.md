# 按键驱动模块文档
## 概述

本文档介绍如何使用按键驱动模块实现各类按键检测功能，包括单次按键、连续检测按键、短按/长按识别等。该驱动通过中断机制实现高效按键检测，支持多按键同时管理和复杂事件处理。
## 主要特性

- 支持单次按键检测和连续按键检测模式
- 支持按键按下/释放事件独立处理
- 支持长按键识别（可自定义长按时间）
- 内置硬件消抖机制
- 中断驱动的高效事件处理
- 多按键并行管理
- 线程安全的回调机制

## 快速入门
### 1. 导入所需模块
```python
from machine import Pin
from key_driver import Key
```
### 2. 定义按键事件处理函数
```python
def key_event_handler(key, event):
    if event == Key.Event.PRESSED:
        print("按键{}被按下".format(key.pin))
    elif event == Key.Event.RELEASED:
        print("按键{}释放，持续 {} 秒".format(key.pin, key.sec))
    elif event == Key.Event.LONG_PRESSED:
        print("按键{}长按 {} 秒".format(key.pin, key.sec))
```
### 3. 初始化按键对象
```python
# 配置K1按键 (GPIO4)
# 工作模式: 连续检测
# 消抖时间: 20ms
# 按下电平: 低电平(0)
# 关注事件: 按下和释放
k1 = Key(
    pin=Pin.GPIO4,
    work_mode=Key.WorkMode.CONTINUOUS,
    debounse_ms=20,
    level_on_pressed=0,
    cared_event=Key.Event.PRESSED | Key.Event.RELEASED,
    event_cb=key_event_handler
)
```
### 4. 运行主程序
```python
while True:
    # 主程序逻辑
    sleep_ms(100)
```
## API接口说明
**`Key(pin, work_mode, debounse_ms, level_on_pressed, cared_event, event_cb, long_press_event=[])`**

构造函数，初始化按键对象。

​**​参数说明:**

- pin: GPIO引脚号
- work_mode: 工作模式
    - Key.WorkMode.ONE_SHOT: 单次按键模式
    - Key.WorkMode.CONTINUOUS: 连续检测模式
- debounse_ms: 消抖时间（毫秒）
- level_on_pressed: 按键按下时的电平
    - 0: 按下为低电平
    - 1: 按下为高电平
- cared_event: 关注的事件类型组合
    - Key.Event.PRESSED: 按键按下事件
    - Key.Event.RELEASED: 按键释放事件
    - Key.Event.LONG_PRESSED: 长按事件
- event_cb: 按键事件回调函数
- long_press_event: 长按时间设置（秒列表）

**`disable()`**

禁用按键检测。
**`enable()`**

启用按键检测。

## 应用示例
基本按键检测
```python
def key_handler(key, event):
    if event == Key.Event.PRESSED:
        print("按键按下")
    elif event == Key.Event.RELEASED:
        print("按键释放")

# 初始化按键K1
Key(
    pin=Pin.GPIO4,
    work_mode=Key.WorkMode.CONTINUOUS,
    debounse_ms=20,
    level_on_pressed=0,
    cared_event=Key.Event.PRESSED | Key.Event.RELEASED,
    event_cb=key_handler
)
```
长按功能实现
```python
def long_press_handler(key, event):
    if event == Key.Event.LONG_PRESSED:
        print("长按功能触发，持续 {} 秒".format(key.sec))
        if key.sec >= 5:
            print("执行恢复出厂设置")

# 配置长按2秒和5秒事件
Key(
    pin=Pin.GPIO5,
    work_mode=Key.WorkMode.CONTINUOUS,
    debounse_ms=20,
    level_on_pressed=0,
    cared_event=Key.Event.PRESSED | Key.Event.RELEASED | Key.Event.LONG_PRESSED,
    event_cb=long_press_handler,
    long_press_event=[2, 5]  # 设置2秒和5秒长按点
)
```
## 常见问题排查
- 物理连接问题
- 抖动干扰严重
- 事件回调未正确处理