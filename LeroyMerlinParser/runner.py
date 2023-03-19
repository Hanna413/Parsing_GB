from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from LeroyMerlinParser.spiders.leroymerlin import LeroymerlinSpider
from LeroyMerlinParser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    query = input('Введите категорию: ')
    process.crawl(LeroymerlinSpider, query=query)
    process.start()