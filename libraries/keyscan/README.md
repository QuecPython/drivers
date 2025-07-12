Key button driver module 

**Class Reference: ** 
```python
from key_driver import Key
```


**Instantiation Parameters:**

| Name | Required | Type | Description | 
|----|----|----|----|
| pin | is | int | GPIO pin number |
| work_mode | is | int | Working mode: Key.WorkMode.ONE_SHOT or Key.WorkMode.CONTINUOUS |
| debounce_ms | is | int | Debouncing time for the key press (in milliseconds) |
| level_on_pressed | is | int | Level when the key is pressed (0 or 1) |
| cared_event | is | int | Type of event to be cared about (Key.Event.PRESSED, Key.Event.RELEASED or their combination) |
| event_cb | is | function | Event callback function |
| long_press_event | is | list | List of long press event times (in seconds) | 

**Event Type:** 

| Name | Value | Description | 
|----|----|----|
| Key.Event.PRESSED | 0x01 | Key Pressed Event |
| Key.Event.RELEASED | 0x02 | Key Released Event |
| Key.Event.LONG_PRESSED | 0x04 | Long Press Event | 

**Work Mode:** 

| Name | Value | Description |
|----|----|----|
| Key.WorkMode.ONE_SHOT | 0x01 | One-shot trigger mode |
| Key.WorkMode.CONTINUOUS | 0x02 | Continuous trigger mode | 

**Method:**

l disable()


Disable the key interrupt detection. 

l enable()


Enable key interrupt detection.