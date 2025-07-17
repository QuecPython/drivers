# HLW8110 Energy Measurement Chip Demo Documentation

## Overview

This document provides a demonstration guide for using the HLW8110 energy measurement chip via UART interface. The HLW8110 is a high-precision IC for measuring AC/DC voltage, current, power and phase angle.

## Key Features

- Measures voltage (0.5V-5V input range)
- Measures current (via external shunt resistor)
- Calculates active power
- Phase angle measurement
- Overvoltage/undervoltage detection
- Zero-crossing detection
- Interrupt capability

## Hardware Setup

1. Connect HLW8110 UART pins to MCU:
   - TX -> MCU RX
   - RX -> MCU TX
   - GND -> Common ground
2. Connect voltage input through appropriate divider
3. Connect current shunt resistor (typical 1-10mΩ)

## Demo Code Explanation

### 1. Initialization

```python
hlw8110 = Hlw8110_uart(uart_n=UART.UART2)  # Initialize with UART2
```

### 2. Basic Measurements

#### Read Current

```python
curr, ic = hlw8110.read_i()  # Returns (raw value, conversion coefficient)
```

- For actual current:
  `I_actual = (raw_value * shunt_ratio) / ic`

#### Read Voltage

```python
volt, uc = hlw8110.read_u()
```

- For actual voltage:
  `V_actual = (raw_value * divider_ratio) / uc`

#### Read Power

```python
power, pc = hlw8110.read_power()
```

- Active power calculation:
  `P_actual = (raw_value * V_ratio * I_ratio) / pc`

#### Phase Angle

```python
angle = hlw8110.read_angle()  # Returns degrees
```

### 3. Advanced Features

#### Zero-Crossing Detection

```python
hlw8110.zx_en(zx_type=3)  # Enable both rising/falling edge detection
```

#### Interrupt Configuration

```python
# Enable undervoltage interrupt
hlw8110.int_en(int_type=11)

# Check interrupts
flag = hlw8110.process_int()
if flag & 0x0800:
    print("Undervoltage detected!")
```

### 4. Full Demo Output

```
start reading...
reading complete.
电流寄存器值：1258291, 电流有效值转换系数：32768 
电压寄存器值：3145728, 电压有效值转换系数：32768
有功功率寄存器值：536870912, 有功功率转换系数：32768
相角：30.2
电压欠压中断 just happened
```

## Calibration Notes

1. Voltage measurement:
   - Apply known voltage
   - Adjust divider ratio until readings match
2. Current measurement:
   - Apply known current
   - Tune shunt resistor value
3. Power calculation:
   - Verify with reference load
   - Adjust coefficients if needed

## Troubleshooting

- **No readings**: Check UART connections and baud rate (fixed at 9600)
- **Incorrect values**: Verify reference voltages and resistor values
- **Interrupts not firing**: Confirm proper interrupt enable sequence

## Application Ideas

- Smart power strips
- Energy monitoring systems
- Power quality analyzers
- Appliance load profiling

For detailed register descriptions and conversion formulas, refer to the HLW8110 datasheet.