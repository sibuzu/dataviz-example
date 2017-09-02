import scrapy
import re
BASE_URL = 'http://en.wikipedia.org'

class NWinnerItem(scrapy.Item):
    name = scrapy.Field()
    link_text = scrapy.Field()
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
        print('Oops, no year in ', text)

    catagory = re.findall('Physics|Chemistry|Physiology or Medicine|Literature|Peace|Ecomics', text)
    if catagory:
        wdata['catagory'] = catagory[0]
    else:
        wdata['catagory'] = ''
        print('Oops, no catagory in ', text)

    if country:
        if text.find('*') != -1:
            wdata['country'] = ''
            wdata['burn_in'] = country
        else:
            wdata['country'] = country
            wdata['burn_in'] = ''
            
    wdata['text'] = text
    return wdata

class NWinnerSpider(scrapy.Spider):
    name = 'nwinners_list'
    allowed_domains = ['en.wikipedia.org']
    start_urls = [
        'https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country'
    ]

    def parse(self, response):
        h2s = response.xpath('//h2')
        for h2 in h2s:
            country = h2.xpath('span[@class="mw-headline"]/text()').extract()
            if country and country[0]!="Summary":
                winners = h2.xpath('following-sibling::ol[1]')[0]
                for w in winners.xpath('li'):
                    wdata = process_winner_li(w, country[0])
                    yield NWinnerItem(
                        country = wdata['country'], 
                        name = wdata['name'],
                        link_text = wdata['text']
                    )
