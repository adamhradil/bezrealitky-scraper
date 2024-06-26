from urllib.parse import urlencode
import json
import scrapy

from bezrealitky_scraper.bezrealitky.items import BezrealitkyItem


class SearchFlatsSpider(scrapy.Spider):
    name = "bezrealitky"
    allowed_domains = ["bezrealitky.cz"]

    def __init__(self, spider_settings: dict, *args, **kwargs):
        super(SearchFlatsSpider, self).__init__(*args, **kwargs)

        params_mapping = {
            "pronájem": "PRONAJEM",
            "prodej": "PRODEJ",
            "byt": "BYT",
            "dům": "DUM",
            "Praha": {
                "osm_value": "Hlavní město Praha, Praha, Česko",
                "regionOsmIds": "R435514",
            },
            "Brno": {
                "osm_value": "Brno, okres Brno-město, Jihomoravský kraj, Jihovýchod, Česko",
                "regionOsmIds": "R438171",
            },
            "Ostrava": {
                "osm_value": "Ostrava, okres Ostrava-město, Moravskoslezský kraj, Moravskoslezsko, Česko",
                "regionOsmIds": "R437354",
            },
        }

        self.params = [
            ("offerType", params_mapping[spider_settings["listing_type"]]),
            ("estateType", params_mapping[spider_settings["estate_type"]]),
            ("osm_value", params_mapping[spider_settings["location"]]["osm_value"]),
            (
                "regionOsmIds",
                params_mapping[spider_settings["location"]]["regionOsmIds"],
            ),
            ("order", "PRICE_ASC"),
            ("currency", "CZK"),
            ("location", "exact"),
        ]

        self.start_urls = ["https://www.bezrealitky.cz/vypis?" + urlencode(self.params)]
        self.len_params = len(self.params)

    def parse(self, response, **kwargs):
        yield from self.for_page(response)

        page_links = response.xpath("//a[@class='page-link']//text()")
        if len(page_links) == 0:
            return
        if len(page_links) == 2:
            if len(self.params) == self.len_params:
                self.params.append(("page", 2))
            else:
                self.params[self.len_params] = ("page", 2)
            yield scrapy.Request(
                "https://www.bezrealitky.cz/vyhledat?" + urlencode(self.params)
            )
            return

        for i in range(
            2, int(response.xpath("//a[@class='page-link']//text()")[1].get()) + 1
        ):
            if len(self.params) == self.len_params:
                self.params.append(("page", i))
            else:
                self.params[self.len_params] = ("page", i)
            yield scrapy.Request(
                "https://www.bezrealitky.cz/vyhledat?" + urlencode(self.params)
            )

    def for_page(self, response):
        links = response.xpath(
            "//h2[contains(@class, 'PropertyCard_propertyCardHeadline')]/a/@href"
        ).getall()
        for link in links:
            yield scrapy.Request(link, callback=self.filter_flats)

    def filter_flats(self, response):
        item = BezrealitkyItem()
        item["url"] = response.url
        item["price"] = response.xpath(
            "//span[contains(text(), 'Měsíční nájemné') or contains(text(), 'Cena')]/../../following-sibling::*/strong/span/text()"
        ).get()
        if item["price"]:
            item["price"] = item["price"].replace("\xa0", " ")
        item["service_fees"] = response.xpath(
            "//span[contains(text(), '+ Poplatky za služby')]/../../following-sibling::*/strong/span/text()"
        ).get()
        if item["service_fees"]:
            item["service_fees"] = item["service_fees"].replace("\xa0", " ")
        item["security_deposit"] = response.xpath(
            "//span[contains(text(), '+ Vratná kauce')]/../../following-sibling::*/strong/span/text()"
        ).get()
        if item["security_deposit"]:
            item["security_deposit"] = item["security_deposit"].replace("\xa0", " ")
        item["address"] = response.xpath(
            "//h1[contains(@class, 'mb-3')]/span[contains(@class, 'd-block')]/text()"
        ).get()
        item["description"] = response.xpath(
            "//div[contains(@class, 'box')]/p[contains(@class, 'text-perex-lg')]/text()"
        ).get()
        item["disposition"] = response.xpath(
            "//span[.='Dispozice']/../following-sibling::*/a/span/text()"
        ).get()
        item["id"] = int(
            response.xpath(
                "//span[.='Číslo inzerátu']/../following-sibling::*/text()"
            ).get()
        )
        item["available_from"] = response.xpath(
            "//span[.='Dostupné od']/../following-sibling::*/span/text()"
        ).get()
        item["floor"] = response.xpath(
            "//span[.='Podlaží']/../following-sibling::*/span/text()"
        ).get()
        item["type"] = response.xpath(
            "//span[.='Typ budovy']/../following-sibling::*/span/text()"
        ).get()
        item["area"] = response.xpath(
            "//span[.='Užitná plocha']/../following-sibling::*/span/text()"
        ).get()
        item["furnished"] = response.xpath(
            "//span[.='Vybaveno']/../following-sibling::*/span/text()"
        ).get()
        item["status"] = response.xpath(
            "//span[.='Stav']/../following-sibling::*/span/text()"
        ).get()
        item["ownership"] = response.xpath(
            "//span[.='Vlastnictví']/../following-sibling::*/span/text()"
        ).get()
        item["penb"] = response.xpath(
            "//span[.='PENB']/../following-sibling::*/span/text()"
        ).get()
        item["design"] = response.xpath(
            "//span[.='Provedení']/../following-sibling::*/span/text()"
        ).get()
        item["balcony"] = response.xpath(
            "//td/span[contains(text(), 'Balkón')]/text()"
        ).get()
        item["cellar"] = response.xpath(
            "//td/span[contains(text(), 'Sklep')]/text()"
        ).get()
        item["garden"] = response.xpath(
            "//td/span[contains(text(), 'Předzahrádka')]/text()"
        ).get()
        item["terrace"] = response.xpath(
            "//td/span[contains(text(), 'Terasa')]/text()"
        ).get()
        item["elevator"] = response.xpath(
            "//td/span[contains(text(), 'Výtah')]/text()"
        ).get()
        item["parking"] = response.xpath(
            "//td/span[contains(text(), 'Parkování')]/text()"
        ).get()
        item["garage"] = response.xpath(
            "//td/span[contains(text(), 'Garáž')]/text()"
        ).get()
        # item["pets"] = response.xpath("//td/span[contains(text(), 'Domácí mazlíčci vítáni')]/text()").get()
        item["loggie"] = response.xpath(
            "//td/span[contains(text(), 'Lodžie')]/text()"
        ).get()
        # item["public_transport"] = response.xpath("//td/span[contains(text(), 'MHD')]/text()").get()
        gps_object = (
            json.loads(response.xpath("//script[@id='__NEXT_DATA__']/text()").get())
            .get("props")
            .get("pageProps")
            .get("origAdvert")
            .get("gps")
        )
        item["gps_lat"] = gps_object.get("lat")
        item["gps_lon"] = gps_object.get("lng")
        yield item
