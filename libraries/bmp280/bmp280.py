from machine import I2C
from usr.i2c import I2CIOWrapper
import utime

BMP280_ADDR = 0x76 #BMP280 address
BMP280_ID = 0x58 #BMP280 ID
BMP280_ID_ADDR = b'\xD0' #BMP280 ID address
BMP280_RESET_ADDR = b'\xE0' #BMP280 reset address
BMP280_RESET_VALUE = b'\xB6' #BMP280 reset value
BMP280_MODE_ADDR = b'\xF4' #BMP280 mode address

def int64(x):
    return x if isinstance(x, int) else int(x)

class BMP280(I2CIOWrapper):
    def init(self):
        """
        Initialize BMP280 sensor
        """
        self.write(BMP280_RESET_ADDR,BMP280_RESET_VALUE)#reset sensor
        utime.sleep(1)

        # Check device ID
        if self.read(BMP280_ID_ADDR)[0] != BMP280_ID:  
            raise ValueError("'0xD0'address is not '0x58'")
            
        # Read calibration data
        self._read_calibration()
        
        # Configure sensor and verify
        self.write(BMP280_MODE_ADDR, b'\x27') # Configure operating mode to normal mode
        utime.sleep_ms(500)  # Extend wait time
        
        # Double check configuration
        config = self.read(BMP280_MODE_ADDR, 1)[0]
        #print("Mode register: 0x{:x}".format(config))
        if config != 0x27:
            # Try forced mode as alternative
            self.write(BMP280_MODE_ADDR, b'\x01')  # Forced mode
            print("Switched to forced mode")
        
    
    def read_word(self, reg):
        """Read a 16-bit unsigned integer"""
        data = self.read(reg,2,20)
        return data[1] << 8 | data[0]
    
    def read_sword(self, reg):
        """Read a 16-bit signed integer"""
        val = self.read_word(reg)
        if val & 0x8000:
            val -= 0x10000
        return val
    
    def is_measuring(self):
        status = self.read(b'\xF3')[0]
        return (status & 0x08) != 0  # 0: Complete, 1: In progress
    def _read_calibration(self):
        """Read calibration data"""
        self.dig_T1 = self.read_word(b'\x88')
        self.dig_T2 = self.read_sword(b'\x8A')
        self.dig_T3 = self.read_sword(b'\x8C')
        self.dig_P1 = self.read_word(b'\x8E')
        self.dig_P2 = self.read_sword(b'\x90')
        self.dig_P3 = self.read_sword(b'\x92')
        self.dig_P4 = self.read_sword(b'\x94')
        self.dig_P5 = self.read_sword(b'\x96')
        self.dig_P6 = self.read_sword(b'\x98')
        self.dig_P7 = self.read_sword(b'\x9A')
        self.dig_P8 = self.read_sword(b'\x9C')
        self.dig_P9 = self.read_sword(b'\x9E')
    
    def read_raw_data(self):
        """Read raw temperature and pressure data"""
        while self.is_measuring():
            utime.sleep_ms(10)
        data = self.read(b'\xF7',6)
        raw_temp = (data[3] << 16) | (data[4] << 8) | data[5]
        raw_temp = raw_temp >> 4
        raw_press = (data[0] << 16) | (data[1] << 8) | data[2]
        raw_press = raw_press >> 4
        return (raw_temp, raw_press)
    
    def compensate_temperature(self, raw_temp):
        """Temperature compensation calculation"""
        var1 = (raw_temp / 16384.0 - self.dig_T1 / 1024.0) * self.dig_T2
        var2 = ((raw_temp / 131072.0 - self.dig_T1 / 8192.0) * (raw_temp / 131072.0 - self.dig_T1 / 8192.0)) * self.dig_T3
        self.t_fine = var1 + var2
        temp = (var1 + var2) / 5120.0
        return temp  
    
    def compensate_pressure(self, raw_press):
        raw_press = int(raw_press)
        t_fine = int(self.t_fine)  # Ensure t_fine is integer
        
        var1 = int64(self.t_fine) - 128000
        var2 = var1 * var1 * int64(self.dig_P6)
        var2 = var2 + (var1 * int64(self.dig_P5) << 17)
        var2 = var2 + (int64(self.dig_P4) << 35)
        
        var1 = (var1 * var1 * int64(self.dig_P3) >> 8) + (var1 * int64(self.dig_P2) << 12)
        var1 = ((((int64(1) << 47) + var1)) * int64(self.dig_P1)) >> 33
        
        if var1 == 0:
            return 0  # Avoid division by zero error
        
        p = int64(1048576) - int64(raw_press)
        p = (((p << 31) - var2) * 3125) // var1   
        var1 = (int64(self.dig_P9) * (p >> 13) * (p >> 13)) >> 25
        var2 = (int64(self.dig_P8) * p) >> 19

        p = (p + var1 + var2) >> 8
        p += int64(self.dig_P7) << 4

        # Final conversion to hPa (allowing float)
        return p / 256 / 100.0
    

    def read_data(self):
        """Read compensated temperature and pressure values"""
        raw_temp, raw_press = self.read_raw_data()
        temp = self.compensate_temperature(raw_temp)
        press = self.compensate_pressure(raw_press)

        return (temp, press)


if __name__ == "__main__":
    # Initialize BMP280 sensor
    i2c_dev = I2C(I2C.I2C0,I2C.STANDARD_MODE)
    sensor = BMP280(i2c_dev,BMP280_ADDR)
    sensor.init()
    try:
        while True:
            # Read sensor data
            ret =sensor.read_data()
            
            # Print data
            print("--------------------------------------------------------------------")
            print("")
            print("Temperature: {:.2f} °C".format(ret[0]))
            print("Pressure: {:.2f} hPa".format(ret[1]))
            print("")
            # Delay 3 second
            utime.sleep(3)
            
    except KeyboardInterrupt:
        print("Program stopped")

