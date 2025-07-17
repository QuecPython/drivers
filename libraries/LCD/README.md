# LCD Universal Driver Documentation
## Overview 

This document explains how to use the LCD universal driver module to achieve various display functions. This driver provides a rich set of drawing and display interfaces, supporting basic graphic drawing such as points, lines, rectangles, and circles, as well as the display of characters, Chinese characters, images, etc.
## Main Features
- Supports basic graphic drawing: points, lines, rectangles, circles
- Supports ASCII character display (8x16, 16x24)
- Supports Chinese character display (16x16, 16x24, 24x24)
- Supports image display (JPG format or RGB data)
- Supports clearing the screen and area filling
- Supports RGB565 color format
- Provides color conversion tool functions

## Quick Start
### 1. Create an LCD subclass 
```python
from machine import LCD
from usr import Peripheral_LCD


class MyLCD(Peripheral_LCD):
    def __init__(self):
        # Initialize the actual LCD device 
        self._lcd = LCD()
        self._lcd.lcd_init()
        self._lcd_w = 240  # LCD width
        self._lcd_h = 320  # LCD height 
        # Call the initialization of the parent 
        class super().__init__(self)
# Create an LCD instance
lcd = MyLCD()
```
### 2. Basic Drawing Operations 
```python
# Clear screen to white 
lcd.Clear(0xFFFF)

# Draw a red rectangle 
lcd.DrawRectangle(50, 50, 150, 150, 0xF800)

# Draw a blue circle 
lcd.DrawCircle(120, 160, 50, 0x001F)

# Draw the green diagonal line 
lcd.DrawLine(0, 0, 239, 319, 0x07E0)
```
### 3. Text Display 
```python
# Display ASCII string 
lcd.ShowAsciiStr(10, 10, 8, 16, "Hello World!" , 0x0000, 0xFFFF)

# Display Chinese characters
lcd.lcd_show_chinese_str(10, 30, 16, 16, "Chinese Test", 0x0000, 0xFFFF) 
```
## API Interface Description 

**`DrawPoint(x, y, color)`**


Draw a point at the designated position. 

**Parameter Explanation:**


- x: X coordinate
- y: Y coordinate
- color: RGB565 color value 

**`Clear(color)`**


Clear the screen using the specified color. 

**Parameter Explanation:**

- color: RGB565 color value 

**`Fill(x_s, y_s, x_e, y_e, color)`**


Fill the specified rectangular area. 

**Parameter Explanation:**


- x_s: Initial X coordinate
- y_s: Initial Y coordinate
- x_e: End X coordinate
- y_e: End Y coordinate
- color: RGB565 color value 

**`DrawLine(x0, y0, x1, y1, color)`**


Draw a straight line. 

**Parameter Explanation:**


- x0, y0: Starting coordinates
- x1, y1: Ending coordinates
- color: RGB565 color value

**`DrawRectangle(x0, y0, x1, y1, color)`**

Draw a rectangular border. 

**Parameter Explanation:**


- x0, y0: Top-left coordinate
- x1, y1: Bottom-right coordinate
- color: RGB565 color value 

**`DrawCircle(x0, y0, r, color)`**


Draw a circle. 

**Parameter Explanation:**


- x0, y0: Coordinates of the center of the circle
- r: Radius
- color: RGB565 color value 

**`ShowChar(x, y, xsize, ysize, ch_buf, fc, bc)`**


Display individual characters (supporting Chinese characters and ASCII). 

**Parameter Explanation:**


- x, y: Display position
- xsize, ysize: Character size
- ch_buf: Character bitmap data
- fc: Foreground color (RGB565)
- bc: Background color (RGB565) 

**`ShowAscii(x, y, xsize, ysize, ch, fc, bc)`**


Display ASCII characters. 

**Parameter Explanation:**


- x, y: Display position
- xsize, ysize: Character size
- ch: ASCII character
- fc: Foreground color (RGB565)
- bc: Background color (RGB565) 

**`ShowAsciiStr(x, y, xsize, ysize, str_ascii, fc, bc)`**


Display the ASCII string. 

**Parameter Explanation:**


- x, y: Starting position
- xsize, ysize: Character size
- str_ascii: ASCII string
- fc: Foreground color (RGB565)
- bc: Background color (RGB565) 

**`ShowJpg(name, start_x, start_y)`**


Display JPG image. 

**Parameter Explanation:**


- name: File name of the image
- start_x, start_y: Display position

**`lcd_show_chinese(x, y, xsize, ysize, ch, fc, bc)`**

Display a single Chinese character. 

**Parameter Explanation:**


- x, y: Display position
- xsize, ysize: Character size
- ch: Chinese character
- fc: Foreground color (RGB565)
- bc: Background color (RGB565) 

**`lcd_show_chinese_str(x, y, xsize, ysize, str_ch, fc, bc)`**


Display the Chinese character string. 

**Parameter Explanation:**


- x, y: Starting position
- xsize, ysize: Character size
- str_ch: Chinese character string
- fc: Foreground color (RGB565)
- bc: Background color (RGB565) 

**`lcd_show_image(image_data, x, y, width, height)`**


Display the RGB data image. 

**Parameter Explanation:**


- image_data: RGB565 格式的图片数据
- x, y: Display position
- width, height: Image size 

**`lcd_show_image_file(path, x, y, width, height, h)`**


Display image files (supporting segmented display of large images). 

**Parameter Explanation:**


- path: Path of the image file
- x, y: Display position
- width, height: Image size
- h: Segmentation height (it is recommended that widthh2 < 4096) 

**`get_rgb565_color(r, g, b)`**


RGB888 to RGB565 color conversion. 

**Parameter Explanation:**


- r: Red component (0 - 255)
- g: Green component (0 - 255)
- b: Blue component (0 - 255) 

**Return Value:** 

RGB565 color value

## Application Example

Create a digital clock interface 
```python
def digital_clock(lcd):
    # Clear screen to a dark blue color 
    lcd.Clear(0x0019)

    # Draw the outer frame of the clock 
    lcd.DrawRectangle(50, 50, 190, 110, 0xFFFF)
    lcd.Fill(51, 51, 189, 109, 0x0000)

    # Display time label 
    lcd.ShowAsciiStr(60, 60, 8, 16, "TIME:", 0xFFFF, 0x0000)

# Updated Time Display 
while True:
    # Obtain the current time 
    current_time = "12:34:56"

    # Clear Old Time 
    lcd.Fill(100, 60, 180, 75, 0x0000)

    # Display new time 
    lcd.ShowAsciiStr(100, 60, 16, 24, current_time, 0xFFFF, 0x0000)

    utime.sleep(1)

# Usage Example 
lcd = MyLCD()
digital_clock(lcd)
```


Display the sensor data dashboard 
```python
def sensor_dashboard(lcd, temp, humi, press):
    # Clear Screen 
    lcd.Clear(0xFFFF)

    # Display Title
    lcd.lcd_show_chinese_str(80, 10, 24, 24, "Environmental Monitoring", 0x0000, 0xFFFF) 
    # Temperature Display
    lcd.lcd_show_chinese_str(30, 50, 16, 16, "Temperature:", 0x0000, 0xFFFF) lcd.ShowAsciiStr(80, 50, 16, 24, "{:.1f}°C".format(temp), 0xF800, 0xFFFF)

    # Humidity Display
    lcd.lcd_show_chinese_str(30, 90, 16, 16, "Humidity:", 0x0000, 0xFFFF) lcd.ShowAsciiStr(80, 90, 16, 24, "{:.1f}%".format(humi), 0x001F, 0xFFFF)
    
    # Pressure Display
    lcd.lcd_show_chinese_str(30, 130, 16, 16, "Pressure:", 0x0000, 0xFFFF) lcd.ShowAsciiStr(80, 130, 16, 24, "{:.1f}hPa".format(press), 0x07E0, 0xFFFF)

    # Draw a divider line 
    lcd.DrawLine(20, 170, 220, 170, 0x0000)

    # Status Indication
    status = "Normal" if 18 <= temp <= 28 and 40 <= humi <= 60 else "Exception"
    color = 0x07E0 if status == "Normal" else 0xF800
    lcd.lcd_show_chinese_str(80， 190， 16， 16， "Status： {}".format(status)， color， 0xFFFF) 

    # Usage Example
    sensor_dashboard(lcd, 25.5, 45.2, 1013.2) 
```


## Common Issues Troubleshooting
- Verify if the coordinates are beyond the screen boundaries
- Ensure that the image data is in the RGB565 format
- Use a conversion tool to preprocess the image