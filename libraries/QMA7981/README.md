# QMA7981 Accelerometer Driver Documentation

## Overview

This document describes how to use the `i2c_qma7981.py` driver to interface with the QMA7981 accelerometer sensor. The driver provides functionalities for sensor initialization, interrupt configuration, acceleration data reading, and step counting.

## Key Features

1. Sensor initialization and interrupt pin configuration
2. Configuration of various interrupt types (motion detection, no-motion detection, step counting, hand raise detection, etc.)
3. Three-axis acceleration data reading
4. Step count reading
5. Step counter clearing

## Quick Start

### 1. Import Module and Initialize Sensor

```python
from machine import ExtInt
from i2c_qma7981 import qma7981

# Define interrupt callback function
def user_cb(event, data):
    if event == qma7981.SIG_MOT_INT:
        print("Significant motion interrupt triggered")
    elif event == qma7981.ANY_MOT_INT_X:
        print("X-axis motion interrupt triggered")
    # Other event handling...

# Initialize sensor with GPIO33 as INT1 interrupt pin, falling edge trigger
sensor = qma7981(user_cb, INT1=ExtInt.GPIO33, INT1_output_mode=qma7981.IRQ_FALLING)
```

### 2. Configure Interrupts

#### Any-Motion Interrupt

```python
# Enable any-motion interrupt with threshold of 200mg and sample count of 1
sensor.set_any_motion_intr(True, threshod=200, sample_times=1)
```

#### Significant Motion Interrupt (Axis-specific)

```python
# Enable X-axis significant motion interrupt
sensor.set_sig_motion_intr(True, threshod=300, sample_times=2, axis_direction=0)
```

#### No-Motion Interrupt

```python
# Enable no-motion interrupt with threshold of 100mg and duration of 10 sample periods
sensor.set_no_motion_intr(True, threshod=100, duration_time=10, axis_direction=0x03)
```

#### Step Counter Interrupt

```python
# Enable step counter interrupt
sensor.set_step_intr(True)
```

#### Hand Raise Interrupt

```python
# Enable hand raise detection interrupt
sensor.set_raise_intr(True, wake_sum_th=10, wake_diff_th=1.0)
```

### 3. Read Sensor Data

#### Read Acceleration Data

```python
acc_data = sensor.readacc()
print(f"X: {acc_data[0]}mg, Y: {acc_data[1]}mg, Z: {acc_data[2]}mg")
```

#### Read Step Count

```python
step_count = sensor.readstep()
print(f"Step count: {step_count}")
```

#### Clear Step Counter

```python
sensor.clearstep()
```

## Interrupt Type Constants

| Constant       | Value | Description                  |
| :------------- | :---- | :--------------------------- |
| SIG_MOT_INT    | 0     | Significant motion interrupt |
| ANY_MOT_INT_X  | 1     | X-axis motion interrupt      |
| ANY_MOT_INT_Y  | 2     | Y-axis motion interrupt      |
| ANY_MOT_INT_Z  | 3     | Z-axis motion interrupt      |
| NO_MOT_INT     | 4     | No-motion interrupt          |
| HAND_RAISE_INT | 5     | Hand raise interrupt         |
| HAND_DOWN_INT  | 6     | Hand down interrupt          |
| STEP_INT       | 7     | Step count interrupt         |

## Example Code

```python
from machine import ExtInt
from i2c_qma7981 import qma7981
import utime as time

def sensor_callback(event, data):
    if event == qma7981.SIG_MOT_INT:
        print("Significant motion detected")
    elif event == qma7981.ANY_MOT_INT_X:
        print("X-axis motion detected")
    elif event == qma7981.STEP_INT:
        print(f"Step count updated: {data}")
    elif event == qma7981.HAND_RAISE_INT:
        print("Hand raise detected")
    # Read current acceleration
    acc = sensor.readacc()
    print(f"Current acceleration - X: {acc[0]}mg, Y: {acc[1]}mg, Z: {acc[2]}mg")

# Initialize sensor
sensor = qma7981(sensor_callback, INT1=ExtInt.GPIO33, INT1_output_mode=qma7981.IRQ_FALLING)

# Configure interrupts
sensor.set_any_motion_intr(True, threshod=200)  # 200mg threshold
sensor.set_step_intr(True)  # Enable step counting
sensor.set_raise_intr(True)  # Enable hand raise detection

# Main loop
while True:
    # Read step count every 5 seconds
    steps = sensor.readstep()
    print(f"Current step count: {steps}")
    time.sleep(5)
```

## Important Notes

1. Ensure correct I2C address (determined by AD0 pin: 0x12 or 0x13)
2. Interrupt pin configuration must match actual hardware connection
3. Acceleration unit is in mg by default (1g = 1000mg)
4. Sample period and threshold settings should be adjusted according to application requirements

## Technical Specifications

- **Communication Interface**: I2C (supports standard and fast modes, 100kHz to 400kHz)
- **Acceleration Range**: Configurable (default 16g with 1.95mg/LSB resolution)
- **Interrupt Modes**: Latch mode by default
- **Power Mode**: Active mode (0xC0 written to PM_ADDR register during initialization)

This driver provides a comprehensive interface to utilize all major features of the QMA7981 accelerometer in your embedded projects. The interrupt-based architecture allows for efficient event detection without constant polling.