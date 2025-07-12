# ESP8266 SLIP 网络接口模块
**类引用**
```python
from esp8266 import Esp8266_ap
```

**实例化参数：**

|名称 |	必填 |类型|说明|
|----|----|----|----|
|uart|	是|	UART对象	|用于连接ESP8266的UART接口|


**接口函数：**

l **set_ap(name=None, pwd=None, project_name='wifi_setap', project_version='1.0.0')**

配置ESP8266模块的AP模式参数。

**​​参数：**​​

| 名称 | 必填 | 类型 | 说明 |
|----|----|----|----|
| name | 否	|str	| WiFi网络名称|
| pwd	| 否|	str|	WiFi密码|
| project_name|	否|	str|	网络检查项目名称，默认'wifi_setap'|
|project_version	|否	|str|	网络检查项目版本，默认'1.0.0'|

​​返回值：​​

0：成功
-1：失败
l **wifi_on()**
启用ESP8266模块并配置SLIP网络接口

​​返回值：​​

0：成功
-1：失败
l **wifi_off()**
关闭ESP8266模块并释放资源

​​返回值：​​ 无