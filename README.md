利用scrapy+scrapy-redis+selenium爬取aqi天气网全国所有城市的天气信息近50W条

[aqistudy](https://www.aqistudy.cn/historydata/)

scrapy主要用来做并发，非selenium渲染页面下的请求和存储io操作

redis可以做增量（城市链接不做指纹）或分布式（继承scrapyredis爬虫类），本次只做断点续爬（利用redis保存url指纹——集合、请求队列——有序集合）

selenium做month和day页面的渲染，这两个页面做了JS加密，selenium渲染完美解决。下载中间件重写process_request方法写入selenium操作，配合PhantomJS（此网页渲染对比chrome要快），取得数据重新封装response返回，引擎交给spider做解析。

数据保存为json格式，利用数据分析三件套：numpy、pandas、matplotlib进行数据清洗、展示。

深圳6月份的aqi走势图，深圳不愧是一线中空气质量最好的，六月份的不良天数仅为一天


![6月份深圳AQI指数走势](images/6%E6%9C%88%E4%BB%BD%E6%B7%B1%E5%9C%B3AQI%E6%8C%87%E6%95%B0%E8%B5%B0%E5%8A%BF.png)

和之前工作的广州做了下对比，生活之都的广州在空气质量上略逊一筹


![广深空气质量对比](images/%E5%B9%BF%E6%B7%B1%E7%A9%BA%E6%B0%94%E8%B4%A8%E9%87%8F%E5%AF%B9%E6%AF%94.png)


后续会更新其他分析图表展示，jupyter数据分析代码一并上传

