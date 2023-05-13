import scrapy
from urllib.parse import urlencode
from ..items import BezrealitkyItem

class SearchFlatsSpider(scrapy.Spider):
    name = "search_flats"
    allowed_domains = ["bezrealitky.cz"]
    params = [
        ('offerType', 'PRONAJEM'),
        ('estateType', 'BYT'),
        ('disposition', 'DISP_2_KK'),
        ('disposition', 'DISP_2_1'),
        ('equipped', 'VYBAVENY'),
        ('regionOsmIds', 'R439840'),
        ('osm_value', 'Praha, okres Hlavní město Praha, Hlavní město Praha, Praha, Česko')
    ]
    len_params = len(params)
    start_urls = ["https://bezrealitky.cz/vyhledat?" + urlencode(params)]

    def parse(self, response):
        yield from self.for_page(response)
        for i in range(2, int(response.xpath("//a[@class='page-link']//text()")[1].get()) + 1):
            if len(self.params) == self.len_params:
                self.params.append(('page', i))
            else:
                self.params[self.len_params] = ('page', i)
            yield scrapy.Request("https://bezrealitky.cz/vyhledat?" + urlencode(self.params))

    def for_page(self, response):
        links = response.xpath("//h2[contains(@class, 'PropertyCard_propertyCardHeadline__y3bhA') and contains(@class, 'mt-4')]/a/@href").getall()
        for link in links:
            yield scrapy.Request(link, callback=self.filter_flats)

    def filter_flats(self, response):
        return BezrealitkyItem(penb=response.xpath(
                "//div[@class='ParamsTable_paramsTableGroup__IIJ_u']//tr[th='PENB']/td/text()").get(),
                               url=response.url,
                               location=response.xpath("//h1/span/text()").get(),
                               price=response.xpath(
            "(//div[contains(@class, 'mb-lg-9') and contains(@class, 'mb-6')])[1]//strong[contains(@class, 'h4') and contains(@class, 'fw-bold')]/text()")
            .get().replace('\xa0', ' ')
                                )