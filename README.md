# 作者：朱江奇 - 2017212685

## web文件夹

web文件夹内内容是本次爬虫的主要代码
本次爬虫作业基于scrapy框架爬取知乎相关数据，因此在运行前需要确认安装好scrapy框架以及相关插件
同时本次作业将爬取到的数据存储到了MongoDB数据库中，因此爬取前也需先配置好本地MongoDB数据库相关环境

在确定环境安装好后，在该目录下打开命令行并输入以下代码即可进行爬取

```shell script
scrapy crawl zhihuSpider
```

## ProxyPool文件夹

由于知乎本身具有非常强大的反爬虫能力，如果只是单纯的运行爬虫的话很快IP地址就会被拒绝访问
因此本人借鉴了一个开源的代理池的设计，即ProxyPool文件夹
运行该代码需要Python环境和Redis环境
安装好这些环境后，进入ProxyPool文件夹
在命令行输入指令安装好所有的库

```shell script
pip3 install -r requirements.txt
```
随后运行run.py程序

```shell script
python run.py
```
此时访问[http://localhost:5555/random]，即可以看到我们随机获得的proxy代理地址，即代理池设立完毕

## 联合使用

首先进入ProxyPool文件夹

运行run.py程序
```shell script
python run.py
```

随后打开另一个命令行窗口，进入web文件夹
运行zhihu_spider.py
```shell script
scrapy crawl zhihuSpider
```

现在我们的代码就可以无限爬取了！