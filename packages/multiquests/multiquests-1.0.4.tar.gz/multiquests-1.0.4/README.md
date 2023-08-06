
# 什么是 multiquests

multiquests是一个通用的、高效的、可以自动返回get请求结果的爬虫请求模块。用于需要爬取大量具有相同格式框架的网页内容的情况。

multiquests是一个基础的处理爬虫请求结果的模块。使用者可以通过传入url列表，请求头、自定义处理函数以及并发数、多进程数、并发数时间等参数，获得爬虫结果。该模块主要封装了异步协程模块和多进程模块以达到提高爬取网页效率的目的。



### 安装
```py

pip3 install multiquests
```


## 使用方法

### 导入

```py

import multiquests
```

### 返回text响应对象(不传入处理函数callback)
```py

url_list = ['http://www.baidu.com'] * 10
headers = {'User-Agent':'apifox/1.4.15 (https://www.apifox.cn)',
            'Accept':'*/*',
            'Cache-Control':'no-cache',
            'Host':'www.baidu.com',
            'Accept-Encoding':'gzip, deflate, br',
            'Connection':'keep-alive'}
			
res = multiquests.getspyder(url_list) # default: callback=None, headers=None, core_num=None, sem_num=None, sleep_time=None
print(res)
		
res1 = multiquests.getspyder(url_list, callback = None, headers = headers, core_num = 5, sem_num = 200, sleep_time = 60) 
print(res1)
```

![default](img/default.png)

**url_list**: 需要爬取的url列表，必传参数\
**headers**: 请求头\
**core_num**：多进程数，默认为操作系统核数的一半\
**sem_num**：协程数，默认为100\
**sleep_time**：并发时间限制，单位为秒，限制时长并发数

### 返回处理请求的结果(传入处理函数)
```py

from bs4 import BeautifulSoup
url_list = ['http://www.baidu.com'] * 100
headers = {'User-Agent':'apifox/1.4.15 (https://www.apifox.cn)',
            'Accept':'*/*',
            'Cache-Control':'no-cache',
            'Host':'www.baidu.com',
            'Accept-Encoding':'gzip, deflate, br',
            'Connection':'keep-alive'}
			
def analysis(text):
    bs = BeautifulSoup(text, 'lxml')
    return [bs.meta.attrs['content']]  
			
res = multiquests.getspyder(url_list, callback=analysis, headers=headers, sem_num = 100, sleep_time = 2)
print(res)
```

![callback](img/callback.png)

**callback**：处理响应结果函数。示例中的callback为analysis，必须传入响应text参数

## Issues

### 关于多进程和多协程
由于在Windows系统中执行直接调用multiprocessing.Process多进程，会无限递归创建子进程报错。因此在调用该模块时会对操作系统进行判断，如果操作系统是Windows系统则只执行多协程爬虫，如果是Linux操作系统则会执行多进程+多协程的操作。

### 关于响应结果
由于该模块是为了批量、快速处理网页响应，为了避免繁杂的请求参数，只支持get请求。返回的响应结果为text类型，以list结果存储返回。如果传入callback函数对响应结果进行处理，则返回的处理结果也会以list形式返回。

### 关于异常处理
对于每次请求，如果响应结果报错，则会进行3次重试操作，如果3次都请求失败则抛出异常。

asyncio模块只支持python3.5及以上版本，如果版本过低则无法进行异步操作，抛出异常。

如果callback函数对响应text结果不能正确处理也会引发异常或者返回结果为空。

对于一些网站如果并发数太多可能会触发反爬机制导致请求失败，因此设置sleep_time参数可以限制一段时间内的并发数，控制请求速度防止同时发送过多请求。


