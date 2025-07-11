# LCD Application Instruction Document

## Interface Description

### st7789

**Class reference:**

```python
from peripheral.lcd.st7789 import St7789
```

 

**Instance parameters:**

| Name     | Required | Type  | Description            | 
| -------- | ---- | ----- | ----------------------- |
| InitData | No   | tuple | Configuration commands to be sent to the LCD |
| width    | No   | int   | Width of the LCD screen, default 240 |
| height   | No   | int   | Height of the LCD screen, default 240 |
| clk      | No   | int   | LCD SPI clock, default 13000 |

```
lcd_test = St7789()
```

**Interface function:**

l **DrawPoint(x, y, color)**

​    Plot the point function.

Parameters: 

| Name | Required | Type | Description | 
| ----- | ---- | ---- | --------------------- |
| x     | Yes  | int  | X coordinate                                                  |
| y     | Yes  | int  | Y coordinate                                                  |
| color | Yes  | int  | Color<br />Red: 0xF800<br />Green: 0x07E0<br />Blue: 0x001F<br />White: 0xFFFF<br />Black: 0x0000 |

Return value: 

No

l **Clear (color)**

Clear the screen. 

Parameters: 

| Name | Required | Type | Description | 
| ----- | ---- | ---- | ------------- |
| Color | Yes | int | Color<br />Red: 0xF800<br />Green: 0x07E0<br />Blue: 0x001F<br />White: 0xFFFF<br />Black: 0x0000 |

返回值：

​       无

l **Fill(x_s, y_s, x_e, y_e, color)**

Fill a rectangle whose diagonal is defined by the starting and ending coordinates. 

Parameters: 

| Name | Required | Type | Description | 
| ----- | ---- | ---- | ----------------------------- |
| x_s   | Yes   | int  | Starting x-coordinate                                              |
| y_s   | Yes   | int  | Starting y-coordinate                                              |
| x_e   | Yes   | int  | Ending x-coordinate                                              |
| y_e   | Yes   | int  | Ending y-coordinate                                              | 
| Color | Yes | int | Color<br />Red: 0xF800<br />Green: 0x07E0<br />Blue: 0x001F<br />White: 0xFFFF<br />Black: 0x0000 |


Return value: 

No

l **DrawLine(x0, y0, x1, y1, color)** 

​	Underline.

Underline. 

Parameters: 

| Name | Required | Type | Description | 
| ----- | ---- | ---- | ------------------------------ |
| x0    | Yes  | int  | Starting x-coordinate                                              |
| y0    | Yes  | int  | Starting y-coordinate                                              |
| x1    | Yes  | int  | Ending x-coordinate                                              |
| y1    | Yes  | int  | Ending y-coordinate                                              | 
| Color | Yes | int | Color<br />Red: 0xF800<br />Green: 0x07E0<br />Blue: 0x001F<br />White: 0xFFFF<br />Black: 0x0000 |


Return value: 

No

l **DrawRectangle (x0, y0, x1, y1, color)** 

Draw a rectangle. 

Parameters: 

| Name | Required | Type | Description | 
| ----- | ---- | ---- | ------------------------ |
| x0    | Yes  | int  | Starting x-coordinate                                              |
| y0    | Yes  | int  | Starting y-coordinate                                              |
| x1    | Yes  | int  | Ending x-coordinate                                              |
| y1    | Yes  | int  | Ending y-coordinate                                              | 
| Color | Yes | int | Color<br />Red: 0xF800<br />Green: 0x07E0<br />Blue: 0x001F<br />White: 0xFFFF<br />Black: 0x0000 |


Return value: 

No

l **DrawCircle (x0, y0, r, color)** 

Draw a rectangle. 

Parameters: 

| Name | Required | Type | Description | 
| ----- | ---- | ---- | --------------------------- |
| x0    | Yes  | int  | Initial x-coordinate                                              |
| y0    | Yes  | int  | Initial y-coordinate                                              |
| r     | Yes  | int  | Radius                                                           | 
| Color | Yes | int | Color<br />Red: 0xF800<br />Green: 0x07E0<br />Blue: 0x001F<br />White: 0xFFFF<br />Black: 0x0000 |


Return value: 

No

l **DrawCircle (x0, y0, r, color)** 

Draw a rectangle. 

Parameters: 

| Name | Required | Type | Description | | ----- | ---- | ---- | ------------------------------------------------------------ |
| x0    | Yes  | int  | Initial x-coordinate                                              |
| y0    | Yes  | int  | Initial y-coordinate                                              |
| r     | Yes  | int  | Radius                                                           | 
| Color | Yes | int | Color<br />Red: 0xF800<br />Green: 0x07E0<br />Blue: 0x001F<br />White: 0xFFFF<br />Black: 0x0000 |


Return value: 

No

l **ShowChar(x, y, xsize, ysize, ch_buf, fc, bc)** 

Single string display. 

Parameters: 

| Name   | Required | Type | Description             | 
| ------ | ---- | ---- | ---------------------- |
| x      | Yes  | int  | X coordinate              |
| y      | Yes  | int  | Y coordinate              |
| xsize  | Yes  | int  | Font width                |
| ysize  | Yes  | int  | Font height                |
| ch_buf | Yes  | int  | Tuple or list storing characters |
| fc     | Yes  | int  | Font color, RGB565        |
| bc     | Yes  | int  | Background color, RGB565  | 

Return value: 

No


l **ShowAscii (x, y, xsize, ysize, ch_buf, fc, bc)**


ASCII character display.

Parameters: 

| Name   | Required | Type | Description                | 
| ------ | ---- | ---- | --------------------------- |
| x      | Yes  | int  | X coordinate                   |
| y      | Yes  | int  | Y coordinate                   |
| xsize  | Yes  | int  | Font width                     |
| ysize  | Yes  | int  | Font height                     |
| ch_buf | Yes  | int  | Tuple or list storing ASCII characters |
| fc     | Yes  | int  | Font color, RGB565             |
| bc     | Yes  | int  | Background color, RGB565       | 

Return value: 

No

l **ShowAsciiStr(x, y, xsize, ysize, str_ascii, fc, bc)** 

ASCII string display. 

Parameters: 

| Name      | Required | Type | Description        | 
| --------- | ---- | ---- | ------------------- |
| x         | Yes  | int  | X coordinate         |
| y         | Yes  | int  | Y coordinate         |
| xsize     | Yes  | int  | Font width           |
| ysize     | Yes  | int  | Font height           |
| str_ascii | Yes  | int  | ASCII string to be displayed |
| fc        | Yes  | int  | Font color, RGB565   |
| bc        | Yes  | int  | Background color, RGB565  | 

Return value: 

No

l **ShowJpg(name, start_x, start_y)** 

Display the picture. If it is larger than the screen, it will be scaled down and displayed in the center of the screen. 

Parameters: 

| Name    | Required | Type | Description | 
| ------- | ---- | ---- | --------- |
| name    | Yes  | str  | Image path  |
| start_x | Yes  | int  | Starting x-coordinate |
| start_y | Yes  | int  | Starting y-coordinate | 

Return value: 

No

l **lcd_show_image(image_data, x, y, width, heigth)** 

For bytearray images, if the width and height of the image are less than 80x80, you can directly call this function to write and display it at once. 

Parameters: 

| Name       | Required | Type     | Description | 
| ---------- | ---- | --------- | --------- |
| image_data | Yes | bytearray | Image path  |
| x          | Yes | int       | Starting x-coordinate |
| y          | Yes | int       | Starting y-coordinate |
| width      | Yes | int       | Image width  |
| height     | Yes | int       | Image height  | 

Return value: 

No



### st7735


**Class Reference:** 

```python
from peripheral.lcd.st7735 import St7735
```





**Instantiation Parameters:** 

| Name     | Required | Type  | Description            | 
| -------- | ---- | ----- | ----------------------- |
| InitData | No   | tuple | Configuration commands to be sent to the LCD |
| width    | No   | int   | Width of the LCD screen, default 128 |
| height   | No   | int   | Height of the LCD screen, default 160 |
| clk      | No   | int   | LCD SPI clock, default 13000 | 

```python
lcd_test = St7735()
```


**Interface Function:**

Same as st7789 





### ili9225


**Class Reference:** 

```python
from peripheral.lcd.ili9225 import Ili9225
```





**Instantiation Parameters:** 

| Name     | Required | Type  | Description            | | -------- | ---- | ----- | ----------------------- |
| InitData | No   | tuple | Configuration commands to be sent to the LCD |
| width    | No   | int   | Width of the LCD screen, default 176 |
| height   | No   | int   | Height of the LCD screen, default 220 |
| clk      | No   | int   | LCD SPI clock, default 13000 | 

**Interface Function:**


Same as st7789 





### ili9341


**Class Reference:** 

```python
from peripheral.lcd.ili9341 import Ili9341
```





**Instantiation Parameters:** 

| Name     | Required | Type  | Description            | | -------- | ---- | ----- | ----------------------- |
| InitData | No   | tuple | Configuration commands to be sent to the LCD |
| width    | No   | int   | Width of the LCD screen, default 320 |
| height   | No   | int   | Height of the LCD screen, default 240 |
| clk      | No   | int   | LCD SPI clock, default 13000 | 

**Interface Function:**


Same as st7789