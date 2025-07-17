# LCD通用驱动文档
## 概述

本文档介绍如何使用LCD通用驱动模块实现各种显示功能。该驱动提供了丰富的绘图和显示接口，支持点、线、矩形、圆形等基本图形绘制，以及字符、汉字、图片等内容的显示。
## 主要特性
- 支持基本图形绘制：点、线、矩形、圆形
- 支持ASCII字符显示（8x16、16x24）
- 支持汉字显示（16x16、16x24、24x24）
- 支持图片显示（JPG格式或RGB数据）
- 支持清屏和区域填充
- 支持RGB565颜色格式
- 提供颜色转换工具函数

## 快速入门
### 1. 创建LCD子类
```python
from machine import LCD
from usr import Peripheral_LCD

class MyLCD(Peripheral_LCD):
    def __init__(self):
        # 初始化实际LCD设备
        self._lcd = LCD()
        self._lcd.lcd_init()
        self._lcd_w = 240  # LCD宽度
        self._lcd_h = 320  # LCD高度
        
        # 调用父类初始化
        super().__init__(self)

# 创建LCD实例
lcd = MyLCD()
```
### 2. 基本绘图操作
```python
# 清屏为白色
lcd.Clear(0xFFFF)

# 绘制红色矩形
lcd.DrawRectangle(50, 50, 150, 150, 0xF800)

# 绘制蓝色圆形
lcd.DrawCircle(120, 160, 50, 0x001F)

# 绘制绿色对角线
lcd.DrawLine(0, 0, 239, 319, 0x07E0)
```
3. 文字显示
```python
# 显示ASCII字符串
lcd.ShowAsciiStr(10, 10, 8, 16, "Hello World!", 0x0000, 0xFFFF)

# 显示汉字
lcd.lcd_show_chinese_str(10, 30, 16, 16, "中文测试", 0x0000, 0xFFFF)
```

## API接口说明

**`DrawPoint(x, y, color)`**

在指定位置绘制一个点。

​**​参数说明:​​**

- x: X坐标
- y: Y坐标
- color: RGB565颜色值

**`Clear(color)`**

使用指定颜色清屏。

​​**参数说明:​**
    
- color: RGB565颜色值

**`Fill(x_s, y_s, x_e, y_e, color)`**

填充指定矩形区域。

**​​参数说明:​​**

- x_s: 起始X坐标
- y_s: 起始Y坐标
- x_e: 结束X坐标
- y_e: 结束Y坐标
- color: RGB565颜色值

**`DrawLine(x0, y0, x1, y1, color)`**

绘制直线。

​​**参数说明:**

- x0, y0: 起点坐标
- x1, y1: 终点坐标
- color: RGB565颜色值

**`DrawRectangle(x0, y0, x1, y1, color)`**

绘制矩形边框。

​**​参数说明:**

- x0, y0: 左上角坐标
- x1, y1: 右下角坐标
- color: RGB565颜色值

**`DrawCircle(x0, y0, r, color)`**

绘制圆形。

​**​参数说明:​​**

- x0, y0: 圆心坐标
- r: 半径
- color: RGB565颜色值

**`ShowChar(x, y, xsize, ysize, ch_buf, fc, bc)`**

显示单个字符（支持汉字和ASCII）。

​**​参数说明:​​**

- x, y: 显示位置
- xsize, ysize: 字符尺寸
- ch_buf: 字符点阵数据
- fc: 前景色（RGB565）
- bc: 背景色（RGB565）

**`ShowAscii(x, y, xsize, ysize, ch, fc, bc)`**

显示ASCII字符。

​​**参数说明:**

- x, y: 显示位置
- xsize, ysize: 字符尺寸
- ch: ASCII字符
- fc: 前景色（RGB565）
- bc: 背景色（RGB565）

**`ShowAsciiStr(x, y, xsize, ysize, str_ascii, fc, bc)`**

显示ASCII字符串。

​**​参数说明:​​**

- x, y: 起始位置
- xsize, ysize: 字符尺寸
- str_ascii: ASCII字符串
- fc: 前景色（RGB565）
- bc: 背景色（RGB565）

**`ShowJpg(name, start_x, start_y)`**

显示JPG图片。

**​​参数说明:**

- name: 图片文件名
- start_x, start_y: 显示位置

**`lcd_show_chinese(x, y, xsize, ysize, ch, fc, bc)`**

显示单个汉字。

​​**参数说明:**

- x, y: 显示位置
- xsize, ysize: 字符尺寸
- ch: 汉字字符
- fc: 前景色（RGB565）
- bc: 背景色（RGB565）

**`lcd_show_chinese_str(x, y, xsize, ysize, str_ch, fc, bc)`**

显示汉字字符串。

​**​参数说明:**

- x, y: 起始位置
- xsize, ysize: 字符尺寸
- str_ch: 汉字字符串
- fc: 前景色（RGB565）
- bc: 背景色（RGB565）

**`lcd_show_image(image_data, x, y, width, height)`**

显示RGB数据图片。

​**​参数说明:​​**

- image_data: RGB565格式图片数据
- x, y: 显示位置
- width, height: 图片尺寸

**`lcd_show_image_file(path, x, y, width, height, h)`**

显示图片文件（支持大图分段显示）。

​**​参数说明:**

- path: 图片文件路径
- x, y: 显示位置
- width, height: 图片尺寸
- h: 分段高度（建议满足 widthh2 < 4096）

**`get_rgb565_color(r, g, b)`**

RGB888转RGB565颜色转换。

​​**参数说明:**

- r: 红色分量 (0-255)
- g: 绿色分量 (0-255)
- b: 蓝色分量 (0-255)

​**​返回值:**

- RGB565颜色值

## 应用示例
创建数字时钟界面
```python
def digital_clock(lcd):
    # 清屏为深蓝色
    lcd.Clear(0x0019)
    
    # 绘制时钟外框
    lcd.DrawRectangle(50, 50, 190, 110, 0xFFFF)
    lcd.Fill(51, 51, 189, 109, 0x0000)
    
    # 显示时间标签
    lcd.ShowAsciiStr(60, 60, 8, 16, "TIME:", 0xFFFF, 0x0000)
    
    # 更新时间显示
    while True:
        # 获取当前时间
        current_time = "12:34:56"
        
        # 清除旧时间
        lcd.Fill(100, 60, 180, 75, 0x0000)
        
        # 显示新时间
        lcd.ShowAsciiStr(100, 60, 16, 24, current_time, 0xFFFF, 0x0000)
        
        utime.sleep(1)

# 使用示例
lcd = MyLCD()
digital_clock(lcd)
```


显示传感器数据仪表盘
```python
def sensor_dashboard(lcd, temp, humi, press):
    # 清屏
    lcd.Clear(0xFFFF)
    
    # 显示标题
    lcd.lcd_show_chinese_str(80, 10, 24, 24, "环境监测", 0x0000, 0xFFFF)
    
    # 温度显示
    lcd.lcd_show_chinese_str(30, 50, 16, 16, "温度:", 0x0000, 0xFFFF)
    lcd.ShowAsciiStr(80, 50, 16, 24, "{:.1f}°C".format(temp), 0xF800, 0xFFFF)
    
    # 湿度显示
    lcd.lcd_show_chinese_str(30, 90, 16, 16, "湿度:", 0x0000, 0xFFFF)
    lcd.ShowAsciiStr(80, 90, 16, 24, "{:.1f}%".format(humi), 0x001F, 0xFFFF)
    
    # 压力显示
    lcd.lcd_show_chinese_str(30, 130, 16, 16, "气压:", 0x0000, 0xFFFF)
    lcd.ShowAsciiStr(80, 130, 16, 24, "{:.1f}hPa".format(press), 0x07E0, 0xFFFF)
    
    # 绘制分隔线
    lcd.DrawLine(20, 170, 220, 170, 0x0000)
    
    # 状态指示
    status = "正常" if 18 <= temp <= 28 and 40 <= humi <= 60 else "异常"
    color = 0x07E0 if status == "正常" else 0xF800
    lcd.lcd_show_chinese_str(80, 190, 16, 16, "状态:{}".format(status), color, 0xFFFF)

# 使用示例
sensor_dashboard(lcd, 25.5, 45.2, 1013.2)
```

## 常见问题排查
- 检查坐标是否超出屏幕范围
- 确保图片数据是RGB565格式
- 使用转换工具预处理图片