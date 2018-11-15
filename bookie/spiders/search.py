# -*- coding: utf-8 -*-

import scrapy
from bookie.items import BookieItem

class itemspider(scrapy.Spider):
    name = 'search'

    def start_requests(self):
        url = 'https://search.jd.com/Search?keyword='
        keyword = getattr(self, 'keyword', None)
        if keyword is not None:
            url= url + keyword + '&enc=utf-8&wq=' + keyword
        self.log('----------------'+url)
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        skus = response.css('li.gl-item')
        # self.log('----------------'+response.body)
        for sku in skus:
            isSelf = sku.css('.p-icons i::text').extract_first() == '自营'
            if isSelf:
                title = sku.css('.p-name font::text').extract_first() + sku.css('.p-name em::text').extract_first()
                price = sku.css('.p-price em::text').extract_first() + sku.css('.p-price i::text').extract_first()
                link = sku.css('.p-name a::attr(href)').extract_first()
                img = sku.css('.p-img img::attr(source-data-lazy-img)').extract_first()
                self.log('----------------'+title+price+link)
            
                with open('test.txt', "a+") as f:
                    f.write(title+'\t'+price+'\t'+link+'\n')
                    f.close()

        #     tags = ','.join(tags)
        #     fileName = '%s-语录.txt' % tags
        #     with open(fileName, "a+") as f:
        #         f.write(text)
        #         f.write('\n')
        #         f.write('标签：' + tags)
        #         f.write('\n-------\n')
        #         f.close()
        # next_page = response.css('li.next a::attr(href)').extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)


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
