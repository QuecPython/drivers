# ESP8266 SLIP Network Interface Module
**Class Reference** 
```python
from esp8266 import Esp8266_ap
```


**Instantiation Parameters:** 

| Name | Required | Type | Description | 
|----|----|----|----|
|uart|	Is|	UART object|	Used to connect to the UART interface of ESP8266| 



**Interface Function:** 

l **set_ap(name=None, pwd=None, project_name='wifi_setap', project_version='1.0.0')** 

Configure the AP mode parameters of the ESP8266 module. 

**Parameters: ** 

| Name | Required | Type | Description | 
|----|----|----|----|
| name | No | str | WiFi network name |
| pwd | No | str | WiFi password |
| project_name | No | str | Network check project name, default 'wifi_setap' |
| project_version | No | str | Network check project version, default '1.0.0' | 

Return value: 

0: Success

-1: Failure 

l **wifi_on()**

Enable the ESP8266 module and configure the SLIP network interface 

Return value: 

0: Success

-1: Failure l **wifi_off()**

Turn off the ESP8266 module and release the resources 

Return value: None