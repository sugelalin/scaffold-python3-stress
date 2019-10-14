# scaffold-python3-stress
Python3 压测 Scaffold

### 安装和使用
1、介绍
- 本项目实现了post和get两种请求方式的接口压测demo，可通过修改参数满足高并发压测需求。
- 使用 asyncio 创建协程，从asyncio模块中直接获取一个EventLoop的引用，然后把需要执行的协程扔到EventLoop中执行，从而实现异步IO（实现了TCP、UDP、SSL等协议），使用 aiohttp基于asyncio实现的HTTP请求。


2、安装依赖库
```
pip3 install -r requirements.txt
```

3、使用
- 修改 processcount 和 threadcount 值，调整进程数和协程数，满足不同的并发需求。  
- 参考：
4c8g的云主机，可设置 processcount=20，threadcount=1000，根据实际情况调整。
```
processcount = 20
threadcount = 1000
```

