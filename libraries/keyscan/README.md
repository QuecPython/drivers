# Key Button Driver Module 

"Class Reference" ```python
from key_driver import Key
```


"Instantiation Parameters" 

| Name | Required | Type | Description | | ---- | ---- | ---- | ---- |
| pin | Is | int | GPIO pin number |
| work_mode | Is | int | Working mode: Key.WorkMode.ONE_SHOT or Key.WorkMode.CONTINUOUS |
| debounce_ms | Is | int | Button debouncing time (milliseconds) |
| level_on_pressed | Is | int | Button level when pressed (0 or 1) |
| cared_event | Is | int | Careful event type (Key.Event.PRESSED, Key.Event.RELEASED or their combination) |
| event_cb | Is | function | Event callback function |
| long_press_event | No | list | List of long press event times (seconds) | 

**Event Type** 

| Name | Value | Description | |----|----|----|
| Key.Event.PRESSED | 0x01 | Key Pressed Event |
| Key.Event.RELEASED | 0x02 | Key Released Event |
| Key.Event.LONG_PRESSED | 0x04 | Long Press Event | 

**Work Mode** 

| Name | Value | Description | |----|----|----|
| Key.WorkMode.ONE_SHOT | 0x01 | One-shot trigger mode |
| Key.WorkMode.CONTINUOUS | 0x02 | Continuous trigger mode | 

Method 

l disable()


Disable key interrupt detection 

Parameter: None 

Return value: None 

l enable()


Enable key interrupt detection 

Parameter: None 

Return value: None