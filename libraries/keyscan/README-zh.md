# Key 按键驱动模块

**类引用**
```python
from key_driver import Key
``` 

**实例化参数**

| 名称 | 必填 | 类型 | 说明 |
| ---- | ---- | ---- | ---- |
| pin | 是 | int | GPIO引脚号 |
| work_mode | 是 | int |工作模式：Key.WorkMode.ONE_SHOT 或 Key.WorkMode.CONTINUOUS
| debounse_ms | 是 | int | 按键消抖时间（毫秒）|
| level_on_pressed | 是 | int | 按键按下时的电平（0或1）|
| cared_event | 是 | int | 关心的事件类型（Key.Event.PRESSED、Key.Event.RELEASED 或其组合）|
| event_cb | 是 | function | 事件回调函数 |
| long_press_event | 否 | list | 长按事件时间列表（秒）|

**事件类型**

| 名称 | 值 | 说明 |
|----|----|----|
| Key.Event.PRESSED | 0x01 | 按键按下事件 |
| Key.Event.RELEASED | 0x02 | 按键释放事件 |
| Key.Event.LONG_PRESSED | 0x04 | 长按事件 |

**工作模式**

| 名称 | 值 | 说明 |
|----|----|----|
| Key.WorkMode.ONE_SHOT	| 0x01 | 单次触发模式|
| Key.WorkMode.CONTINUOUS	| 0x02 | 连续触发模式 |

方法

l disable()

禁用按键中断检测

​​参数：​​ 无
​​
返回值：​​ 无

l enable()

启用按键中断检测

​​参数：​​ 无

​​返回值：​​ 无