import scrapy
import re
BASE_URL = 'http://en.wikipedia.org'

class NWinnerItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    mini_bio = scrapy.Field()
    image_urls = scrapy.Field()
    bio_image = scrapy.Field()
    images = scrapy.Field()

class NWinnerSpiderBio(scrapy.Spider):
    name = 'nwinners_minibio'
    allowed_domains = ['en.wikipedia.org']
    
    start_urls = [
        'https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country'
    ]

    custom_settings = {
        'ITEM_PIPELINES': {'nobel_winners.pipelines.NobelImagesPipeline': 1},
        'IMAGES_STORE': 'images'
    }

    def parse(self, response):
        h2s = response.xpath('//h2')
        for h2 in list(h2s)[2:]:
            country = h2.xpath('span[@class="mw-headline"]/text()').extract()
            if country:
                winners = h2.xpath('following-sibling::ol[1]')[0]
                for w in winners.xpath('li'):
                    wdata = {}
                    wdata['link'] = BASE_URL + w.xpath('a/@href').extract()[0]
                    request = scrapy.Request(wdata['link'],
                        callback=self.get_mini_bio)
                    request.meta['item'] = NWinnerItem(**wdata)
                    yield request

    def get_mini_bio(self, response):
        item = response.meta['item']
        item['image_urls'] = []
        img_src = response.xpath('//table[contains(@class,"infobox")]//img/@src')
        if img_src:
            item['image_urls'] = ['https:' + img_src.extract()[0]]
        mini_bio = ''
        paras = response.xpath('//*[@id="mw-content-text"]/div/p[text() or normalize-space(.)=""]').extract()
        for p in paras:
            if p == '<p></p>':
                break
            mini_bio += p

        mini_bio = mini_bio.replace('href="/wiki', 'href="' + BASE_URL + '/wiki')
        mini_bio = mini_bio.replace('href="#', item['link'] + '#')

        item['mini_bio'] = mini_bio
        yield item
    