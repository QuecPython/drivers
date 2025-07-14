# GNSS 定位模块驱动

**类引用**
```python
from gnss_driver import Gnss
```

**实例化参数：**

| 名称 | 必填 | 类型 | 说明 |
|----|----|----|----|
| uartn | 是 | int | UART端口号 |
|baudrate|	是|	int|	波特率|
|databits|	是|	int|	数据位|
|parity	|是	|int	|校验位|
|stopbits|	是|	int|	停止位|
|flowctl|	是|	int|	流控|

**接口函数：**

l read_gnss(retry=1, debug=0)

读取GNSS原始数据。

​​**参数：**​​

| 名称	| 类型 | 默认值 |	说明 |
|----|----|----|----|
| retry | int | 1 | 重试次数 |
|debug|	int|	0	|调试模式|

​​返回值：​​

-1：失败

(data_valid, data)：成功

data_valid：数据有效位（0x01-0x07）

data：原始GNSS数据

l isFix()

检查是否定位成功

​​返回值：​​

1：定位成功

0：定位失败

l getUtcTime()

获取定位的UTC时间

​​返回值：​​

成功：UTC时间字符串

失败：-1

l getLocationMode()

获取定位模式

​​返回值：​​

-1：获取失败

0：定位不可用

1：GPS/SPS模式

2：DGPS/DSPS模式

6：估算模式

l getUsedSateCnt()

获取定位使用的卫星数量

​​返回值：​​


成功：卫星数量

失败：-1

l getLocation()

获取经纬度信息

​​返回值：​​

成功：(经度, 经度方向, 纬度, 纬度方向)

失败：-1

getViewedSateCnt()

获取可见卫星数量

​​返回值：​​


成功：卫星数量

失败：-1

l getGeodeticHeight()

获取海拔高度

​​返回值：​​

成功：海拔高度（米）
失败：-1
getCourse()
获取卫星方位角

​​返回值：​​

字典：{卫星编号: 方位角}
getSpeed()
获取对地速度

​​返回值：​​

成功：速度（KM/h）
失败：-1