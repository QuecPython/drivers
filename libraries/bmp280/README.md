# BMP280 Temperature and Pressure Sensor Driver  Documentation

## 1. Overview

This doc provides a `BMP280` driver class for I2C interface temperature and pressure sensors in the BMP280 series, based on QuecPython. The BMP280 is a high-precision, low-power temperature and pressure sensor that supports communication via the I2C bus, suitable for scenarios such as meteorological monitoring and altitude calculation. This driver class encapsulates the BMP280's underlying I2C communication protocol, sensor initialization process, raw data reading, and calibration compensation algorithms, facilitating quick access to high-precision temperature and pressure data in the QuecPython environment.

## 2. Detailed Explanation of Core Classes and Methods

### 1. Class Initialization `__init__(self, i2c, slaveaddr)`

Function: Initializes the BMP280 driver class, associates the I2C bus device, and sets the sensor's I2C address.
Parameters:

- `i2c`: I2C bus device (e.g., `machine.I2C(I2C.I2C0, I2C.STANDARD_MODE)`), must be of type `machine.I2C`.
- `slaveaddr`: I2C slave address of the BMP280 (default value is `0x76`, corresponding to the constant `BMP280_ADDR`).

Note: This class inherits from `I2CIOWrapper` and reuses its I2C read/write methods to implement underlying communication with the sensor.

### 2. Basic I2C Communication Methods (Inherited from `I2CIOWrapper`)

The following methods implement the underlying I2C protocol, supporting register read/write operations for the sensor, and do not need to be called directly by the user:

#### `read(self, addr, size=1, delay=0)`

Function: Reads data from the specified register address.
Parameters:

- `addr`: Register address (e.g., `b'\xF7'`, indicating reading the raw temperature and pressure data register).
- `size`: Number of bytes to read (1 byte by default).
- `delay`: Delay time before reading (in ms, 0 by default).
  Return Value: Byte array (`bytearray`) containing the read register data.
  Exception: Throws `I2CIOWrapper.I2CReadError` if reading fails.

#### `write(self, addr, data)`

Function: Writes data to the specified register address.
Parameters:

- `addr`: Register address (e.g., `b'\xF4'`, indicating the mode configuration register).
- `data`: Data to be written (must be of type `bytes` or `bytearray`, e.g., `b'\x27'` indicates configuring to normal mode).
  Exception: Throws `I2CIOWrapper.I2CWriteError` if writing fails.

### 3. Register Read/Write Auxiliary Methods (Internal Use)

#### `read_word(self, reg)`

Function: Reads a 16-bit unsigned integer from the specified register.
Parameter: `reg`: Starting address of the register (e.g., `b'\x88'`, corresponding to the temperature calibration coefficient `dig_T1`).
Return Value: 16-bit unsigned integer (obtained by concatenating high and low bytes).

#### `read_sword(self, reg)`

Function: Reads a 16-bit signed integer from the specified register.
Parameter: `reg`: Starting address of the register (e.g., `b'\x8A'`, corresponding to the temperature calibration coefficient `dig_T2`).
Return Value: 16-bit signed integer (automatically handles the sign bit, converts to a negative value if exceeding 32767).

### 4. Core Function Methods

#### `init(self)`

Function: Initializes the BMP280 sensor, completing reset, device verification, calibration data reading, and working mode configuration.
Process:

1. Sensor reset: Writes the reset value (`BMP280_RESET_VALUE = b'\xB6'`) to the reset register (`BMP280_RESET_ADDR = b'\xE0'`) and waits 1 second for stabilization.
2. Device ID verification: Reads the ID register (`BMP280_ID_ADDR = b'\xD0'`); if the value is not equal to `BMP280_ID = 0x58`, throws `ValueError`.
3. Reads calibration data: Calls `_read_calibration()` to obtain the sensor's factory calibration coefficients (used for data compensation).
4. Configures working mode: By default, configures to normal mode (writes `b'\x27'` to the mode register `b'\xF4'`); if configuration fails, automatically switches to forced mode (writes `b'\x01'`).

#### `_read_calibration(self)`

Function: Reads the built-in calibration coefficients of the sensor (stored in non-volatile memory) for temperature and pressure compensation calculations.
Note: Calibration coefficients include temperature-related (`dig_T1`-`dig_T3`) and pressure-related (`dig_P1`-`dig_P9`), totaling 11 parameters, which are read from fixed register addresses (`0x88`-`0x9E`) and stored as class attributes.

#### `is_measuring(self)`

Function: Checks if the sensor is performing temperature and pressure measurement.
Return Value: `True` indicates measurement in progress, `False` indicates measurement completed.
Note: Determines the measurement status by reading the 3rd bit (`0x08`) of the status register (`b'\xF3'`).

#### `read_raw_data(self)`

Function: Reads uncompensated raw temperature and pressure data.
Process:

1. Waits for measurement completion (judged by `is_measuring()`, polls every 10ms if not completed).
2. Reads 6 bytes of data from the data register (`b'\xF7'`), where the first 3 bytes are the raw pressure value and the last 3 bytes are the raw temperature value.
3. Performs shift processing on the raw data (shifts right by 4 bits to remove the lower 4 invalid bits).
   Return Value: Tuple `(raw_temp, raw_press)` representing the raw temperature and pressure values, respectively.

#### `compensate_temperature(self, raw_temp)`

Function: Converts raw temperature data to actual temperature value (°C) using calibration coefficients for compensation calculation.
Parameter: `raw_temp`: Raw temperature value obtained via `read_raw_data()`.
Return Value: Floating-point temperature value (unit: °C).
Note: The compensation process is based on the algorithm provided in the chip datasheet, calculated using `dig_T1`-`dig_T3`, and stores the intermediate result `t_fine` as a class attribute (used for pressure compensation).

#### `compensate_pressure(self, raw_press)`

Function: Converts raw pressure data to actual pressure value (hPa) using calibration coefficients and the temperature compensation result `t_fine` for calculation.
Parameter: `raw_press`: Raw pressure value obtained via `read_raw_data()`.
Return Value: Floating-point pressure value (unit: hPa).
Note: The compensation process is based on the complex algorithm provided in the chip datasheet, calculated using `dig_P1`-`dig_P9` and `t_fine`, and finally converted to hectopascal (hPa) units.

#### `read_data(self)`

Function: Obtains compensated temperature and pressure values in one step.
Process: Calls `read_raw_data()` to get raw data, then calculates actual values via `compensate_temperature()` and `compensate_pressure()`, respectively.
Return Value: Tuple `(temp, press)` representing temperature (°C) and pressure (hPa), respectively.

## 3. Usage Example

### Example: Initialize the Sensor and Cyclically Read Temperature and Pressure Data

```python
from machine import I2C
import utime
from bmp280_driver import BMP280  # Assume the script is saved as bmp280_driver.py

# Initialize I2C bus (using I2C0, standard mode)
i2c_dev = I2C(I2C.I2C0, I2C.STANDARD_MODE)

# Initialize BMP280 sensor (address 0x76)
sensor = BMP280(i2c_dev, BMP280_ADDR)
sensor.init()  # Complete sensor initialization

try:
    while True:
        # Read compensated temperature and pressure data
        temp, press = sensor.read_data()
        
        # Print data (retain 2 decimal places)
        print("--------------------------------------------------")
        print(f"Temperature: {temp:.2f} °C")
        print(f"Pressure: {press:.2f} hPa")
        print("")
        
        # Read once every 3 seconds
        utime.sleep(3)

except KeyboardInterrupt:
    print("Program stopped")
```

## 4. Constant Description

| Constant Name        | Value     | Description                                 |
| -------------------- | --------- | ------------------------------------------- |
| `BMP280_ADDR`        | `0x76`    | I2C slave address of BMP280                 |
| `BMP280_ID`          | `0x58`    | Device ID of BMP280 (fixed value)           |
| `BMP280_ID_ADDR`     | `b'\xD0'` | Device ID register address                  |
| `BMP280_RESET_ADDR`  | `b'\xE0'` | Reset register address                      |
| `BMP280_RESET_VALUE` | `b'\xB6'` | Reset command value                         |
| `BMP280_MODE_ADDR`   | `b'\xF4'` | Working mode configuration register address |