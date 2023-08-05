# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 19:21:08 2022

@author: 01412322
"""
import os
import sys
import asyncio
import aiohttp
import platform
import multiprocessing
import nest_asyncio
nest_asyncio.apply()


"""
初始化：
urls:传入要爬的地址列表
core_num:进程数，默认核数一半
sem_num:协程数，默认100
sleep_time:限制多长时间并发数，默认不限制（s）
"""
class Multicoro():
    def __init__(self, urls, core_num=None, sem_num=None, sleep_time=None):
        self.res_list = []
        self.retry = 3
        self.sleep_time = sleep_time 
        self.urls = [(urls[i], i) for i in range(len(urls))] 
        if core_num:
            self.core_num = core_num
        else:
            self.core_num = max(1,int(os.cpu_count()/2))
        if sem_num:
            self.sem_num = sem_num
        else:
            self.sem_num = 100
    
    ###headers：调用头   callback：调用函数  **params：callback的其他参数
    ###这里callback只接受.text()的返回结果
        
    async def getpage(self, url, headers=None, callback=None, **params):
        sem = asyncio.Semaphore(self.sem_num)
        async with sem:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url[0], headers = headers) as response:
                        response.raise_for_status()   
                        res = await response.text(errors='ignore')
                        res = res.encode('utf-8').decode('utf-8','ignore')
                        if callback:
                            self.res_list.append((callback(res, **params),url[1]))
                        else:
                            self.res_list.append((res, url[1]))
                #若有异常则重试，每次递减重试次数
                except Exception as e:
                    if self.retry > 0:
                        self.retry -= 1
                        return await self.getpage(url, headers, callback, **params)
                    print(e)
                    pass
        if self.sleep_time:
            await asyncio.sleep(self.sleep_time)
        
    async def amain(self, urls, callback=None, headers=None, **params):
        tasks = [self.getpage(url, headers, callback, **params) for url in urls]
        res = await asyncio.gather(*tasks)
        return res


    def main(self, urls, callback=None, headers=None, **params):
        urls = [(urls[i], i) for i in range(len(urls))] 
        try:
            ###判断python版本
            if float(sys.version[:3]) >= 3.7:
                asyncio.run(self.amain(urls, callback, headers, **params))
            else:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(self.amain(urls, callback, headers, **params))
            self.res_list = sorted(self.res_list, key = lambda x: x[1])
            self.res_list = [i[0] for i in self.res_list]
            return self.res_list
        except  Exception as e:
            print(e)  #python版本不支持
            
    ###执行多进程，callback为调用函数
    def multicoro(self, urls, callback=None, headers=None, **params):
        #callback为解析网页的函数，返回list结果
        #**params为callback函数的参数
        
        task_num = len(urls)
        if task_num <= self.core_num:
            split_lists = [urls]
        else:   
            spcount = self.core_num if task_num % self.core_num == 0 else self.core_num+1
            index = int(task_num / self.core_num)
            split_lists = [urls[i*index : i*index+index] for i in range(spcount)]
        ##任务分割
        pool = multiprocessing.Pool(min(self.core_num, task_num))
        res = []
        for item, lists in enumerate(split_lists):
            res.append(pool.apply_async(self.main, args=(lists, callback, headers,), kwds = params))
        pool.close()
        pool.join()
        
        #保存结果，在这里调用.get()
        res_list = []
        for i in res:
            res_list.extend(i.get())
            
        return res_list

##调用函数
def getspyder(urls, callback=None, headers=None, core_num=None, sem_num=None, sleep_time=None, **params):
    enginee = Multicoro(urls, core_num, sem_num, sleep_time)

    try:
        if platform.system() == 'Linux':
            res = enginee.multicoro(urls, callback, headers, **params)
        else:
            res = enginee.main(urls, callback, headers, **params)
        return res
    except Exception as e:
        print(e)


if __name__ == '__main__':
    pass


