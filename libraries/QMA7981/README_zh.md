# QMA7981 加速度传感器驱动使用说明文档

## 概述

本文档介绍如何使用 `i2c_qma7981.py` 驱动文件与 QMA7981 加速度传感器进行交互。该驱动提供了初始化传感器、配置中断、读取加速度数据和步数等功能。

## 主要功能

1. 初始化传感器并配置中断引脚
2. 设置不同类型的中断（运动检测、静止检测、步数计数、抬手检测等）
3. 读取三轴加速度数据
4. 读取步数计数
5. 清除步数计数

## 快速开始

### 1. 导入模块并初始化传感器

```python
from machine import ExtInt
from i2c_qma7981 import qma7981

# 定义中断回调函数
def user_cb(event, data):
    if event == qma7981.SIG_MOT_INT:
        print("显著运动中断触发")
    elif event == qma7981.ANY_MOT_INT_X:
        print("X轴运动中断触发")
    # 其他事件处理...

# 初始化传感器，使用GPIO33作为INT1中断引脚，下降沿触发
sensor = qma7981(user_cb, INT1=ExtInt.GPIO33, INT1_output_mode=qma7981.IRQ_FALLING)
```

### 2. 配置中断

#### 任意方向运动中断

```python
# 启用任意方向运动中断，阈值为200mg，采样次数为1次
sensor.set_any_motion_intr(True, threshod=200, sample_times=1)
```

#### 特定方向显著运动中断

```python
# 启用X轴显著运动中断
sensor.set_sig_motion_intr(True, threshod=300, sample_times=2, axis_direction=0)
```

#### 静止检测中断

```python
# 启用静止检测中断，阈值为100mg，持续时间为10个采样周期
sensor.set_no_motion_intr(True, threshod=100, duration_time=10, axis_direction=0x03)
```

#### 步数计数中断

```python
# 启用步数计数中断
sensor.set_step_intr(True)
```

#### 抬手检测中断

```python
# 启用抬手检测中断
sensor.set_raise_intr(True, wake_sum_th=10, wake_diff_th=1.0)
```

### 3. 读取传感器数据

#### 读取加速度数据

```python
acc_data = sensor.readacc()
print(f"X: {acc_data[0]}mg, Y: {acc_data[1]}mg, Z: {acc_data[2]}mg")
```

#### 读取步数

```python
step_count = sensor.readstep()
print(f"步数: {step_count}")
```

#### 清除步数计数

```python
sensor.clearstep()
```

## 中断类型常量

| 常量           | 值   | 描述         |
| :------------- | :--- | :----------- |
| SIG_MOT_INT    | 0    | 显著运动中断 |
| ANY_MOT_INT_X  | 1    | X轴运动中断  |
| ANY_MOT_INT_Y  | 2    | Y轴运动中断  |
| ANY_MOT_INT_Z  | 3    | Z轴运动中断  |
| NO_MOT_INT     | 4    | 静止中断     |
| HAND_RAISE_INT | 5    | 抬手中断     |
| HAND_DOWN_INT  | 6    | 放手中断     |
| STEP_INT       | 7    | 步数中断     |

## 示例代码

```python
from machine import ExtInt
from i2c_qma7981 import qma7981
import utime as time

def sensor_callback(event, data):
    if event == qma7981.SIG_MOT_INT:
        print("检测到显著运动")
    elif event == qma7981.ANY_MOT_INT_X:
        print("检测到X轴运动")
    elif event == qma7981.STEP_INT:
        print(f"步数更新: {data}")
    elif event == qma7981.HAND_RAISE_INT:
        print("检测到抬手动作")
    # 读取当前加速度
    acc = sensor.readacc()
    print(f"当前加速度 - X: {acc[0]}mg, Y: {acc[1]}mg, Z: {acc[2]}mg")

# 初始化传感器
sensor = qma7981(sensor_callback, INT1=ExtInt.GPIO33, INT1_output_mode=qma7981.IRQ_FALLING)

# 配置中断
sensor.set_any_motion_intr(True, threshod=200)  # 200mg阈值
sensor.set_step_intr(True)  # 启用步数计数
sensor.set_raise_intr(True)  # 启用抬手检测

# 主循环
while True:
    # 每5秒读取一次步数
    steps = sensor.readstep()
    print(f"当前总步数: {steps}")
    time.sleep(5)
```

## 注意事项

1. 确保I2C地址正确（AD0脚决定地址为0x12或0x13）
2. 中断引脚配置需与实际硬件连接一致
3. 加速度单位默认为mg（1g=1000mg）
4. 采样周期和阈值设置需根据实际应用场景调整

通过以上API，您可以方便地集成QMA7981加速度传感器到您的项目中，实现运动检测、步数计数等功能。