from machine import LCD
from usr.LCD import Peripheral_LCD
import utime as time

class Uc1628(Peripheral_LCD):
    def __init__(self, InitData, width, height, clk):
        self._lcd_w = width
        self._lcd_h = height
        self._lcd_clk = clk

        init_para = (
            2, 0, 120,

            0, 1, 0x04,
            1, 1, 0x00,
            0, 0, 0x10,
            0, 0, 0x13,
            0, 0, 0x15,
            0, 0, 0x20,

            0, 0, 0x2D,
            0, 1, 0x40,
            1, 1, 0x00,
            0, 1, 0x60,
            1, 1, 0x00,
            0, 2, 0x81,
            1, 1, 0x00,
            1, 1, 0x98,
            0, 0, 0x86,
            0, 0, 0x89,
            0, 0, 0xc7,

            0, 0, 0xeb,
            0, 1, 0xf1,
            1, 1, 0xA0,
            0, 2, 0xc8,
            1, 1, 0x00,
            1, 1, 0x00,
            0, 1, 0xc9,
            1, 1, 0xad,

            0, 2, 0x17,
            1, 1, 0x01,
            1, 1, 0x0f,

            0, 2, 0x17,
            1, 1, 0x02,
            1, 1, 0x1e,

            0, 2, 0x17,
            1, 1, 0x03,
            1, 1, 0x28,

            0, 2, 0x17,
            1, 1, 0x04,
            1, 1, 0x32,

            0, 2, 0x17,
            1, 1, 0x05,
            1, 1, 0x3c,

            0, 2, 0x17,
            1, 1, 0x06,
            1, 1, 0x55,

            0, 2, 0x17,
            1, 1, 0x07,
            1, 1, 0x6e,

            0, 2, 0x17,
            1, 1, 0x08,
            1, 1, 0x82,

            0, 2, 0x17,
            1, 1, 0x09,
            1, 1, 0x91,

            0, 2, 0x16,
            1, 1, 0x01,
            1, 1, 0x00,

            0, 2, 0x16,
            1, 1, 0x02,
            1, 1, 0x00,

            0, 2, 0x16,
            1, 1, 0x03,
            1, 1, 0x00,

            0, 2, 0x16,
            1, 1, 0x04,
            1, 1, 0x04,

            0, 2, 0x16,
            1, 1, 0x05,
            1, 1, 0x06,

            0, 2, 0x16,
            1, 1, 0x06,
            1, 1, 0x0d,

            0, 2, 0x16,
            1, 1, 0x07,
            1, 1, 0x0e,

            0, 2, 0x16,
            1, 1, 0x08,
            1, 1, 0x0f,

            0, 2, 0x16,
            1, 1, 0x09,
            1, 1, 0x14,

            0, 2, 0x81,
            1, 1, 0x01,
            1, 1, 0x31,

            0, 2, 0x81,
            1, 1, 0x02,
            1, 1, 0x2c,

            0, 2, 0x81,
            1, 1, 0x03,
            1, 1, 0x27,

            0, 2, 0x81,
            1, 1, 0x04,
            1, 1, 0x22,

            0, 2, 0x81,
            1, 1, 0x05,
            1, 1, 0x1D,

            0, 2, 0x81,
            1, 1, 0x06,
            1, 1, 24,

            0, 2, 0x81,
            1, 1, 0x07,
            1, 1, 20,

            0, 2, 0x81,
            1, 1, 0x08,
            1, 1, 15,

            0, 2, 0x81,
            1, 1, 0x09,
            1, 1, 10,

            2, 0, 10,)

        invalid = (
            0, 1, 0x40,
            1, 1, 161,
            0, 1, 0x60,
            1, 1, 0,
            0, 1, 0x04,
            1, 1, 128,
            0, 0, 0x01,)

        if InitData is None:
            self._initData = bytearray(init_para)
        else:
            self._initData = InitData

        self._invalidData = bytearray(invalid)

        self._lcd = LCD()
        self._lcd.lcd_init(InitData,
                           self._lcd_w,
                           self._lcd_h,
                           self._lcd_clk,
                           1,
                           4,
                           1,
                           self._invalidData,
                           None,
                           None,
                           None)
        super().__init__(self)


image_data = [
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X80,0X80,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X3C,0X3C,0X3C,0X3C,0X3C,0XBC,
0XBC,0XBC,0XBC,0XBC,0XBC,0XBC,0XBC,0XBC,0XBC,0XBC,0XBC,0XBC,0XBC,0XBC,0XBC,0XBC,
0X9C,0X9E,0X0E,0X0F,0X07,0X07,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0XFC,0X0C,
0X0C,0XFC,0XC0,0XC0,0XFE,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0XC0,0XDC,0XDC,0XDC,0X1C,0X1D,
0XDD,0XDD,0XDD,0XDD,0XDD,0XDD,0XDD,0XDD,0XDD,0XDD,0XDD,0XDD,0XDD,0XDD,0XDD,0X1D,
0X1D,0X1D,0X1C,0X9C,0XDC,0XC0,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0XFC,0X0C,
0X0C,0XFC,0X0C,0X0C,0X0C,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XF0,0X78,
0XFF,0XFF,0XFF,0X03,0X03,0X03,0XFB,0XFB,0XFB,0XFB,0XFB,0XFB,0XFB,0XFB,0XFB,0XF8,
0XFC,0XFE,0X9F,0X8F,0X07,0X03,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X7E,0X06,
0X06,0X7E,0X06,0X06,0X7E,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X1F,0X1F,0X1F,0X1F,0X00,0X00,
0X1F,0X1F,0X1F,0X1E,0X1E,0X1E,0X1E,0X1E,0X1E,0X1E,0X1E,0X1E,0X1E,0X1E,0X1E,0X00,
0X01,0X03,0X0F,0X3F,0X3F,0X3E,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0XF0,0X18,
0X18,0X18,0X18,0X18,0XF0,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0XF8,0XFC,0XFC,0XFC,0X3C,0X3C,
0XBC,0XBC,0XBC,0X3C,0X3C,0X3C,0X3C,0X3C,0X3C,0X3C,0X3C,0X3C,0X3C,0XBC,0XBC,0XBC,
0X3C,0X1E,0X1E,0X0F,0X07,0X03,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0XF8,0X8C,
0X8C,0X8C,0X8C,0X8C,0XF8,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0X00,0X00,
0X03,0X87,0X87,0XCF,0XCE,0XFC,0X78,0X30,0X78,0XFC,0XFE,0XCE,0X87,0X87,0X03,0X03,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X18,0X39,
0XD9,0X19,0X19,0X19,0X18,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X7F,0XFF,0XFF,0XFF,0XF0,0XF0,
0XF7,0XF7,0XF7,0XF3,0XF1,0XF0,0XF0,0XF0,0XF0,0XF0,0XF1,0XF3,0XF7,0XF7,0XF7,0XF7,
0XF0,0XF0,0XF0,0XF0,0XF0,0XE0,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X66,0XE7,
0X66,0X66,0X66,0X66,0X66,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0XE0,0XE0,0XE0,0XE0,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0XE0,0XE0,
0XE0,0XE0,0X07,0X07,0X07,0X07,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X98,0X9C,
0X9B,0X98,0X98,0X98,0X18,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0X0F,0X0F,
0X0F,0XFF,0XFF,0XFF,0X0F,0X0F,0X0F,0X0F,0XFF,0XFF,0XFF,0X0F,0X0F,0X0F,0XFF,0XFF,
0XFF,0XFF,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X99,0X99,
0X99,0X99,0X99,0X99,0X87,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XC0,0XC0,
0XC0,0XFF,0XFF,0XFF,0XC0,0XC0,0XC0,0XC0,0XFF,0XFF,0XFF,0XC0,0XC0,0XC0,0XFF,0XFF,
0XFF,0XFF,0XC0,0XC0,0XC0,0XC0,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X31,0X33,
0X35,0X39,0X39,0X31,0X31,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X1F,0X1F,0X1F,0X1F,0X03,0X03,
0X03,0X03,0X03,0X03,0X03,0X03,0X03,0X03,0X03,0X03,0X03,0X03,0X03,0X03,0X1F,0X1F,
0X1F,0X1F,0X03,0X03,0X03,0X03,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X8F,0XC6,
0XC6,0XC6,0XC6,0XC6,0X8F,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X18,0X3C,0X3C,0X18,0X00,
0X3F,0X3F,0X3F,0X3C,0X3C,0X3C,0X3C,0X3C,0X3C,0X3C,0X3C,0X3C,0X3C,0X3C,0X3C,0X3C,
0X3E,0XFE,0XDE,0X9E,0X0E,0X06,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X07,0X80,
0X40,0X60,0XE0,0X60,0X67,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0XFF,0XFF,0XFF,0X00,0XC0,0X80,
0XFF,0XFF,0X07,0X87,0X87,0XF7,0XF7,0XF7,0X87,0X87,0XF7,0XF7,0XF7,0X87,0X87,0X87,
0X07,0X00,0XFF,0XFF,0XFF,0XFC,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0XC1,0X02,
0X04,0X0C,0X0F,0X0C,0X0C,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0XFF,0XFF,0XFF,0XE0,0XF3,0X77,
0XFF,0XFF,0X00,0X07,0X07,0X7F,0X7F,0X7F,0X07,0X07,0X7F,0X7F,0X7F,0X07,0X07,0X87,
0XC0,0X00,0XFF,0XFF,0XFF,0XFF,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0XCF,0X83,
0X83,0X83,0X83,0X83,0XC3,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X03,0X07,0X07,0X07,0X01,0X00,
0XC7,0XC7,0XC7,0X07,0X07,0X07,0X07,0X07,0X07,0X07,0X07,0X07,0X07,0X07,0X07,0X07,
0X03,0X00,0X03,0X07,0X07,0X07,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0XE3,0X31,
0X31,0X31,0X31,0X31,0XE3,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0XC0,0XC6,0XCF,0XCF,0X06,0X00,
0X0F,0X0F,0X0F,0X0F,0X0F,0X0F,0X0F,0XCF,0XCF,0XCF,0XCF,0X0F,0X0F,0X0F,0X0F,0X0F,
0X0F,0X0F,0X7F,0X7F,0X7E,0X7C,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X63,0XE6,
0X66,0X66,0X66,0X66,0X63,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0X00,0X00,
0X3C,0X3C,0X3C,0X3C,0X3C,0X3C,0X3C,0XFF,0XFF,0XFF,0XFF,0X3C,0X3C,0X3C,0X3C,0X3C,
0X3C,0X3C,0X3C,0X3C,0X3C,0X3C,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X8C,0X8C,
0X8D,0X8E,0X0E,0X0C,0X8C,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X0F,0X1F,0X3F,0X3F,0X3C,0X3C,
0X3C,0X3C,0X3C,0X3C,0X3C,0X3C,0X3C,0X3D,0X3D,0X3D,0X3D,0X3C,0X3C,0X3C,0X3C,0X3C,
0X3C,0X3C,0XFC,0XFC,0XF8,0XF0,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X1F,0X01,
0X01,0X1F,0X18,0X18,0X1F,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X01,0X01,0X01,0X01,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
]

if __name__ == '__main__':
    lcd = Uc1628(None,163,256,13000)
    image_test = bytearray(image_data)
    lcd.lcd_write(image_test,0,0,127,19)



