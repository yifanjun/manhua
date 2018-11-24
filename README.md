scrapy简单实例-爬某个动漫，后续应该会更新其他部分  
如何运行  
git clone https://github.com/yifanjun/scrapy_kukudm.git  
cd scrapy_kukudm  
cd manhua  
scrapy crawl comic  
博客地址：https://blog.csdn.net/zyf2333/article/details/84405034  

-----------更新------------  
依据kukudm.py的思路，爬取了所有的日本动漫，只需要运行
scrapy crawl comic2即可  
且kukudm2.py比kukudm.py简洁了一些  
关于items.py、pipelines.py的修改请看代码部分的注释