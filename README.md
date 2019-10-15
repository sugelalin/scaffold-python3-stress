# scaffold-python3-stress
基于Python3 压测脚手架

## 压测工具介绍
### 总览
- AB 压测工具
- Navive 是原生Python3异步压测脚本
- Locust 是分布式压测工具
- Siege 功能类似于ab wrk之类的工具，但它可以直接压测批量接口数据，无需安装插件。使用也很简单，只要把批量生成好的接口和数据放到数据文件中即可


#### AB 压测工具
1、介绍
- AB压测工具是最常用的几种压测工具之一（wrk/jenkins等）
- 使用场景：使用简单，方便 用于对静态页面或单一接口做性能压测

2、安装 ab
```
sudo yum install httpd-tools
```

3、使用示例：
```
ab -n 10 -c 2 -T application/json http://domain.com/uri
ab -n 10 -c 2 -p postdata -T application/json http://domain.com/uri
```

ab 不支持直接压测多个接口，可以安装插件 apachebench-for-multi-url  wiki  

示例：
```
ab -c 100 -n 2000 -L urls.txt
ab -c 100 -n 2000 -C "token=xxxxx" -L urls.txt
```

#### Navive 压测脚本
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

#### Locust 压测脚本
1、介绍  
- locust是Python的开源性能测试框架
- 使用场景：
可编程，应用场景比较丰富。比如：a、持续施压情况下，测试目标机器性能和架构高可用性；b、模拟并压测，完整且复杂的业务场景，比如提交作业-判题-推送通知；获取商品信息-加入购物车-生成订单-支付；

2、安装：  
2.1 安装Python3  

安装依赖：

    yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
    
    ./configure --prefix=/opt/python3
    
    make && make install

设置环境变量 PATH  

2.2. 安装Locust  
文档：https://docs.locust.io/en/stable/  
    
    python3 -m pip install locustio（推荐）  
或者

    python3 -m pip install -e git://github.com/locustio/locust.git@master#egg=locustio
    
    locust --help

3、使用lucust做模拟用户持续请求，测试高并发下的架构高可用  

- 架构：可单机使用，也可以部署分布式结构master-slaver模式
示例：
- 单机：locust -f test_locustfile.py 
- 分布式：
    
    locust -f test_locustfile.py --master  
    locust -f test_locustfile.py --slave --master-host=192.168.0.1

UI界面: 

    http://localhost:8089

#### Siege 压测脚本
1、介绍
- 使用场景：
siege功能类似于ab wrk之类的工具，但它可以直接压测批量接口数据，无需安装插件。使用也很简单，只要把批量生成好的接口和数据放到数据文件中即可

2、下载&安装：
   
    a.官网下载地址：http://download.joedog.org/siege/  
    b.解压安装
    
    ./configure
    
    sudo make && make install
    
    siege -V

3、使用
3.1 单接口压测：

    siege -c 20 -r 10 http://www.baidu.com
    
3.2 多接口压测：

    demo-urls:
    http://domain.com/uri POST mobile=18010000000&password=123456
    http://domain.com/uri POST mobile=18010000001&password=123456
    
    siege -c 20 -r 10 -f demo-urls
    
Tips: 可提前通过脚本批量生产demo-urls

返回值介绍：

    Transactions: 访问次数
    Availability: 成功次数
    Elapsed time: 测试用时
    Data transferred: 测试传输数据量
    Response time: 平均响应时间
    Transaction rate:每秒事务处理量
    Throughput: 吞吐率
    Concurrency: 并发用户数
    Successful transactions: 成功传输次数
    Failed transactions: 失败传输次数
    Longest transaction: 最长响应时间
    Shortest transaction: 最短响应时间
    
PS：可以通过修改系统参数提高并发。比如，有时会受到 max user processes 限制，查看 ulimit -a，设置 ulimit -u unlimited
