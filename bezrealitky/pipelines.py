# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exceptions import DropItem
import logging
from bezrealitky.settings import is_passing

class BezrealitkyPipeline:
    log = {'Nice': 0, 'Bad': 0}
    def process_item(self, item, spider):
        if is_passing(item):
        # if (item['penb'] is None or item['penb'] in ['A', 'B', 'C']) and item['has_washer']:
        # if cadastral in good_cadastrals:
            self.log['Nice'] += 1
            return item
        else:
            self.log['Bad'] += 1
            raise DropItem("not needed")

    def close_spider(self, spider):
        logging.info(f"We got {self.log['Nice']} nice flats and {self.log['Bad']} bad")
