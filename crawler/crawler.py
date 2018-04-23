from scrapy.crawler import CrawlerProcess

from .adafruit import AdafruitSpider


def get_crawler(init=False):
    process = CrawlerProcess({
        'ITEM_PIPELINES': {
            'crawler.pipelines.CrawlerPipeline': 300,
        },
        'LOG_LEVEL': 'WARNING',
        'IS_INITIALIZE': init
    })
    process.crawl(AdafruitSpider)
    return process
