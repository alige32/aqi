利用scrapy+scrapy-redis+selenium爬取aqi天气网全国所有城市的天气信息近50W条
[aqistudy](https://www.aqistudy.cn/historydata/)
scrapy主要用来做并发，非selenium渲染页面下的请求和存储io操作

redis可以做增量（城市链接不做指纹）或分布式（继承scrapyredis爬虫类），本次只做断点续爬（利用redis保存url指纹——集合、请求队列——有序集合）

selenium做month和day页面的渲染，这两个页面做了JS加密，selenium渲染完美解决。下载中间件重写process_request方法写入selenium操作，配合PhantomJS（此网页渲染对比chrome要快），取得数据重新封装response返回，引擎交给spider做解析。

数据保存为json格式，后续数据分析处理可以用csv模块。。。

