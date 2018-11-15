import scrapy

class itemspider(scrapy.Spider):
    name = 'item'
    start_urls = [
        'http://lab.scrapyd.cn'
    ]

    def parse(self, response):
        allContent=response.css('div.quote')

        for content in allContent:    
            text=content.css('.text::text').extract_first()
            author=content.css('.author::text').extract_first()
            tags=content.css('.tag::text').extract()
            tags=','.join(tags)
            
            filename='%s 语录.txt' % author
            with open(filename, 'a+') as f:
                f.write(text)
                f.write('\n')
                f.write('tags:'+tags)
                f.write('\n-------\n')
                f.close()