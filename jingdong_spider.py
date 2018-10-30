from scrapy import Spider, Request, FormRequest
from jingdong_scrapy.jingdong.items import JingdongItem
from jingdong_scrapy.jingdong.pipelines import JingdongPipeline

import json
import re
import scrapy
from lxml import etree
from scrapy import cmdline

flag = True

data_dict = {}
data_dict['stype'] = 'ChengYu'
data_dict['Submit'] = '+搜索+'



class JingdongSpider(Spider):
    name = 'jingdong'
    allowed_domains = []
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep - alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    }

    start_urls = 'http://chengyu.xiexingcun.com/search.asp'

    def start_requests(self):

        f = open("dict.txt", "r", encoding='utf-8')
        list1 = []
        lines = f.readlines()  # 读取全部内容
        for i in range(0, 100):  # (开始/左边界, 结束/右边界, 步长)
            # list = [] ## 空列表, 将第i行数据存入list中
            for word in lines[i].split():
                # print(word)
                if (re.search(r'[\u4e00-\u9fa5]', str(word))):
                    list1.append(word)
        print(list1)

        #
        #
        # for m in range(len(list)):
        #     data_dict['q'] =  list[m]
        #
        #     yield scrapy.FormRequest(url=self.start_urls, headers=self.headers,
        #                              formdata=data_dict, callback=self.parse,meta={'m': list[m]})
        # list1 = ['一分为二','一人之下']
        for m in range(len(list1)):
            data_dict['keyword'] = list1[m]

            yield scrapy.FormRequest(url=self.start_urls, headers=self.headers,
                                     formdata=data_dict, callback=self.parsebody, meta={'m': data_dict},dont_filter=True)


    def parse(self, response):
        data = response.meta['m']
        print(data_dict)

        selector = etree.HTML(response.text)

        # sel = json.loads(body)  # 转化为字典
        # total_pages = sel.get("totalPage")
        # print(str(selector))
        resultword = selector.xpath("//div[@class='read f14 p10']/center[1]/table[@id]/tr[3]/td[2]/a/font/text()")

        print(resultword[0])
        print(1)
        if (resultword[0] == data_dict['keyword']):
            print(2)
            yield scrapy.FormRequest(url=self.start_urls, headers=self.headers,
                                     formdata=data_dict, callback=self.parsebody, meta={'m': data_dict},dont_filter=True)


    def parsebody(self, response):
        meta = response.meta['m']
        selector = etree.HTML(response.text)
        # print(11)


        resultword = selector.xpath("//div[@class='read f14 p10']/center[1]/table[@id]/tr[3]/td[2]/a/font/text()")
        resultword2 = selector.xpath("//div[@class='read f14 p10']/center[1]/table[@id]/tr[3]/td[2]/a/text()")
        # print(resultword2)
        #
        # print(resultword)

        # resultcontent = selector.xpath("//div[@class='read f14 p10']/center[1]/table[@id]/tr[3]/td[3]/text()")


        # print(resultcontent)

        # resultprobe = selector.xpath("//div[@class='mcon bt noi f14'][1]/p[3]/a[1][@href]/text()")




        item = JingdongItem()
        # if(len(resultword) == 1):
        #
        #     if ( resultword[0] == data_dict['keyword']):
        #
        #
        #
        #         item['word'] = resultword
        #         item['content'] = resultcontent

        item['word'] = resultword+resultword2
        # item['content'] = resultcontent

        yield item




















