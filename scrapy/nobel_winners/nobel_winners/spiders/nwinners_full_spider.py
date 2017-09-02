import scrapy
import re
import logging

logging.basicConfig(filename='nobel_full.log', level=logging.WARN)
logger = logging.getLogger('nobel_full')

BASE_URL = 'https://en.wikipedia.org'

class NWinnerItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    year = scrapy.Field()
    catagory = scrapy.Field()
    country = scrapy.Field()
    gender = scrapy.Field()
    born_in = scrapy.Field()
    date_of_birth = scrapy.Field()
    date_of_death = scrapy.Field()
    place_of_birth = scrapy.Field()
    place_of_death = scrapy.Field()
    text = scrapy.Field()

def process_winner_li(w, country=None):
    wdata = {}
    wdata['link'] = BASE_URL + w.xpath('a/@href').extract()[0]
    text = ' '.join(w.xpath('descendant-or-self::text()').extract())
    wdata['name'] = text.split(',')[0].strip()

    year = re.findall('\d{4}', text)
    if year:
        wdata['year'] = int(year[0])
    else:
        wdata['year'] = 0
        logger.warn('Oops, no year in ' + text)

    catagory = re.findall('Physics|Chemistry|Physiology or Medicine|Literature|Peace|Economic', text)
    if catagory:
        wdata['catagory'] = catagory[0]
    else:
        wdata['catagory'] = ''
        logger.warn('Oops, no catagory in ' + text)

    if country:
        if text.find('*') != -1:
            wdata['country'] = ''
            wdata['born_in'] = country
        else:
            wdata['country'] = country
            wdata['born_in'] = ''
            
    wdata['text'] = text
    return wdata

class NWinnerSpider(scrapy.Spider):
    name = 'nwinners_full'
    allowed_domains = ['en.wikipedia.org']
    start_urls = [
        'https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country'
    ]

    def parse(self, response):
        h2s = response.xpath('//h2')
        for h2 in list(h2s)[2:]:
            country = h2.xpath('span[@class="mw-headline"]/text()').extract()
            if country:
                winners = h2.xpath('following-sibling::ol[1]')[0]
                for w in winners.xpath('li'):
                    wdata = process_winner_li(w, country[0])
                    request = scrapy.Request(
                        wdata['link'],
                        callback=self.parse_bio,
                        dont_filter=True)
                    request.meta['item'] = NWinnerItem(**wdata)
                    yield request

    def parse_bio(self, response):
        item = response.meta['item']
        href = response.xpath("//li[@id='t-wikibase']/a/@href").extract()
        if href:
            request = scrapy.Request(href[0],
                callback=self.parse_wikidata,
                dont_filter=True)
            request.meta['item'] = item
            yield request

    def parse_wikidata(self, response):
        item = response.meta['item']
        property_code = [
            {'name': 'date_of_birth', 'code': 'P569'},
            {'name': 'date_of_death', 'code': 'P570'},
            {'name': 'place_of_birth', 'code': 'P19', 'link': True},
            {'name': 'place_of_death', 'code': 'P20', 'link': True},
            {'name': 'gender', 'code': 'P21', 'link': True}
        ]

        p_template = '//*[@id="{code}"]/div[2]/div/div/div[2]' \
                     '/div[1]/div/div[2]/div[2]{link_html}/text()'

        for prop in property_code:
            link_html = ''
            if prop.get('link'):
                link_html = '/a'
            xp = p_template.format(code=prop['code'], link_html=link_html)
            sel = response.xpath(xp)
            if sel:
                item[prop['name']] = sel[0].extract()
            
        yield item
