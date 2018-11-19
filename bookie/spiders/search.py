# -*- coding: utf-8 -*-

import scrapy
from bookie.items import BookieItem

class itemspider(scrapy.Spider):
    name = 'search'

    def start_requests(self):
        urls = {
            'jd': 'https://search.jd.com/Search?keyword={}&enc=utf-8&wq={}'
            # 'dd': 'http://search.dangdang.com/?key={}&act=input'
        }
        keyword = getattr(self, 'keyword', None)
        if keyword is not None:
            for key, value in urls.items():
                if key == 'jd':
                    url = value.format(keyword, keyword)
                    yield scrapy.Request(url, self.parsejd)
                elif key == 'dd':
                    url = value.format(keyword)
                    yield scrapy.Request(url, self.parsedd)

    def parsejd(self, response):
        skus = response.css('li.gl-item')
        # self.log('----------------'+response.body)
        for sku in skus:
            isSelf = sku.css('.p-icons i::text').extract_first() == '自营'
            if isSelf:
                skuid = sku.css('.gl-item::attr(data-sku)').extract_first()
                author = sku.css('.p-bi-name a::text').extract_first()
                title = ''.join(sku.css('.p-name em *::text').extract())  #sku.css('.p-name font::text').extract_first() + sku.css('.p-name em::text').extract_first()
                price = sku.css('.p-price em::text').extract_first() + sku.css('.p-price i::text').extract_first()
                publisher = sku.css('.p-bi-store a::text').extract_first()
                link = sku.css('.p-name a::attr(href)').extract_first()
                img = sku.css('.p-img img::attr(source-data-lazy-img)').extract_first()
                self.log('----------------'+title+price+link)
            
                with open('test.txt', "a+") as f:
                    f.write(title+'\t'+price+'\t'+link+'\n')
                    f.close()

    def parsedd(self, response):
        skus = response.css('li.gl-item')
        # self.log('----------------'+response.body)
        for sku in skus:
            isSelf = sku.css('.p-icons i::text').extract_first() == '自营'
            if isSelf:
                skuid = sku.css('.gl-item::attr(data-sku)').extract_first()
                author = sku.css('.p-bi-name a::text').extract_first()
                title = sku.css('.p-name font::text').extract_first() + sku.css('.p-name em::text').extract_first()
                price = sku.css('.p-price em::text').extract_first() + sku.css('.p-price i::text').extract_first()
                publisher = sku.css('.p-bi-store a::text').extract_first()
                link = sku.css('.p-name a::attr(href)').extract_first()
                img = sku.css('.p-img img::attr(source-data-lazy-img)').extract_first()
                self.log('----------------'+title+price+link)
            
                with open('test.txt', "a+") as f:
                    f.write(title+'\t'+price+'\t'+link+'\n')
                    f.close()


        # item = BookieItem()
        # item['title'] = response.xpath('//head/title/text()').extract()[0].replace('【图片 价格 品牌 报价】-京东','').replace('【行情 报价 价格 评测】-京东','')
        # item['link'] = response.url
        # #价格抓包
        # ture_id = re.findall(r'https://item.jd.com/(.*?).html',item['link'])[0]
        # price_url = "https://p.3.cn/prices/mgets?skuIds=J_" + str(ture_id)
        # price_txt = urllib.request.urlopen(price_url).read().decode('utf-8', 'ignore')
        # item['price'] = re.findall(r'"p":"(.*?)"',price_txt)[0]
        # #评论抓包
        # comment_url = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds=" + str(ture_id)
        # comment_txt = urllib.request.urlopen(comment_url).read().decode('utf-8', 'ignore')
        # item['comment'] = re.findall(r'"CommentCount":(.*?),"',comment_txt)[0]
        # return item
