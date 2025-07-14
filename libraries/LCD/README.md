# LCD Application Guide Document 

## Interface Description 

### st7789


**Class Reference:** 

```python
from peripheral.lcd.st7789 import St7789
```





**Instantiation Parameters:** 

| Name     | Required | Type  | Description            | 
| -------- | ---- | ----- | ----------------------- |
| InitData | No   | tuple | Configuration commands to be sent to the LCD |
| width    | No   | int   | Width of the LCD screen, default 240 |
| height   | No   | int   | Height of the LCD screen, default 240 |
| clk      | No   | int   | LCD SPI clock, default 13000 | 

```
lcd_test = St7789()
```


**Interface Function: ** 

l **DrawPoint(x, y, color)**


Make a dot. 

Parameters: 

| Name | Required | Type | Description | 
| ----- | ---- | ---- | ------------------------------------------------------------ |
| x     | Yes  | int  | X coordinate                                                  |
| y     | Yes  | int  | Y coordinate                                                  |
| color | Yes  | int  | Color<br />Red: 0xF800<br />Green: 0x07E0<br />Blue: 0x001F<br />White: 0xFFFF<br />Black: 0x0000 | 

Return value: 

No


l **Clear (color)**


Clear the screen. 

Parameters: 

| Name | Required | Type | Description | 
| ----- | ---- | ---- | ------------------------------------------------------------ |
| Color | Yes | int | Color<br />Red: 0xF800<br />Green: 0x07E0<br />Blue: 0x001F<br />White: 0xFFFF<br />Black: 0x0000 | 

Return value: 

No


l **Fill(x_s, y_s, x_e, y_e, color)**


Fill a rectangle whose diagonal is defined by the starting and ending coordinates. 

Parameters: 

| Name | Required | Type | Description | 
| ----- | ---- | ---- | ------------------------------------------------------------ |
| x_s   | Yes   | int  | Starting x-coordinate                                              |
| y_s   | Yes   | int  | Starting y-coordinate                                              |
| x_e   | Yes   | int  | Ending x-coordinate                                              |
| y_e   | Yes   | int  | Ending y-coordinate                                              |
| color | Yes   | int  | Color<br />Red: 0xF800<br />Green: 0x07E0<br />Blue: 0x001F<br />White: 0xFFFF<br />Black: 0x0000<br /> | 

Return value: 

No


l **DrawLine(x0, y0, x1, y1, color)**


Underline. 

Parameters: 

| Name | Required | Type | Description | 
| ----- | ---- | ---- | ------------------------------------------------------------ |
| x0    | Yes  | int  | Starting x-coordinate                                              |
| y0    | Yes  | int  | Starting y-coordinate                                              |
| x1    | Yes  | int  | Ending x-coordinate                                              |
| y1    | Yes  | int  | Ending y-coordinate                                              |
| color | Yes  | int  | Color<br />Red: 0xF800<br />Green: 0x07E0<br />Blue: 0x001F<br />White: 0xFFFF<br />Black: 0x0000<br /> | 

Return value: 

No


l **DrawRectangle (x0, y0, x1, y1, color)**


Draw a rectangle. 

Parameters: 

| Name | Required | Type | Description | 
| ----- | ---- | ---- | ------------------------------------------------------------ |
| x0    | Yes  | int  | Starting x-coordinate                                              |
| y0    | Yes  | int  | Starting y-coordinate                                              |
| x1    | Yes  | int  | Ending x-coordinate                                              |
| y1    | Yes  | int  | Ending y-coordinate                                              |
| color | Yes  | int  | Color<br />Red: 0xF800<br />Green: 0x07E0<br />Blue: 0x001F<br />White: 0xFFFF<br />Black: 0x0000<br /> | 

Return value: 

No


l **DrawCircle (x0, y0, r, color)**


Draw a rectangle. 

Parameters: 

| Name | Required | Type | Description | 
| ----- | ---- | ---- | ------------------------------------------------------------ |
| x0    | Yes  | int  | Initial x-coordinate                                              |
| y0    | Yes  | int  | Initial y-coordinate                                              |
| r     | Yes  | int  | Radius                                                         |
| color | Yes  | int  | Color<br />Red: 0xF800<br />Green: 0x07E0<br />Blue: 0x001F<br />White: 0xFFFF<br />Black: 0x0000<br /> | 

Return value: 

No


l **DrawCircle (x0, y0, r, color)**


Draw a rectangle. 

Parameters: 

| Name | Required | Type | Description | 
| ----- | ---- | ---- | ------------------------------------------------------------ |
| x0    | Yes  | int  | Initial x-coordinate                                              |
| y0    | Yes  | int  | Initial y-coordinate                                              |
| r     | Yes  | int  | Radius                                                         |
| color | Yes  | int  | Color<br />Red: 0xF800<br />Green: 0x07E0<br />Blue: 0x001F<br />White: 0xFFFF<br />Black: 0x0000 | 

Return value: 

No


l **ShowChar(x, y, xsize, ysize, ch_buf, fc, bc)**


Single string display. 

Parameters: 

| Name   | Required | Type | Description         | 
| ------ | ---- | ---- | ---------------------- |
| x      | Yes  | int  | X coordinate              |
| y      | Yes  | int  | Y coordinate              |
| xsize  | Yes  | int  | Font width                |
| ysize  | Yes  | int  | Font height                |
| ch_buf | Yes  | int  | Tuple or list storing characters |
| fc     | Yes  | int  | Font color, RGB565       |
| bc     | Yes  | int  | Background color, RGB5