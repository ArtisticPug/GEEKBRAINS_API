from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings


from Lesson_7.leroy_merlin.spiders.Leroy_the_spider import LeroyTheSpiderSpider
from Lesson_7.leroy_merlin import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    search = 'ковер'
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroyTheSpiderSpider, search)

    process.start()