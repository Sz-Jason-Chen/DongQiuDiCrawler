# 懂球帝爬虫
## 数据来源
懂球帝的绝大部分数据都可以通过api.dongqiudi.com访问，使用requests.get访问这个api可以获取json格式的字符串，经过解析后可以直接用字典与列表结合的方式访问数据。
这极大简化了网页爬虫，不然就得用正则表达式或者beautifulsoup解析器去解析html文件，非常麻烦。

## 项目结构
该爬虫主要分为两层：
第一层connector.py负责获取网页信息，Connector所有方法均为静态方法，每个方法对应一个url；
第二层text.py负责将字符串按照json格式解析，并按要求返回格式化数据，Text的每一个子类都对应着Connector中每一个方法返回的字符串，也就是每一种url获取的文本。  

main.py是一些样例，简单调用了一些方法，并用multiprocessing.dummy的Pool进行多线程运行。如果未来有更复杂更频繁的调用，还可以再封装一层，结合多线程快速输出综合数据。

text.py里仅仅写了一些比较有代表性的数据的格式化输出，其他次要信息也类似，基本上都是一个模版，可自行增删。

## 引用与安利
许多网站都有设计自己的api，除了懂球帝，还有pixiv（二次元插图网站）。这些api可以在网页脚本源码中人肉查找，据说也可以通过一些黑科技抓包软件（charles）来获取。

这个爬虫的架构思路来源于[PixivCrawler](https://github.com/JasonChen2118/PixivCrawler)，这是个未完成的pixiv的爬虫，它也有类似的Connection和Text类。
