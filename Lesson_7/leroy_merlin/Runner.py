from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings


from Lesson_7.leroy_merlin.spiders.Leroy_the_spider import LeroyTheSpiderSpider
from Lesson_7.leroy_merlin.spiders.Leroy_the_spider2 import LeroyTheSpiderSpider2
from Lesson_7.leroy_merlin.spiders.Leroy_the_spider3 import LeroyTheSpiderSpider3
from Lesson_7.leroy_merlin import settings

if __name__ == '__main__':  # Создал 3 одинаковых паука для проверки работоспособности обработчика
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    search = 'зеркало'
    search2 = 'ковер'
    search3 = 'люстры'
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroyTheSpiderSpider, search)
    process.crawl(LeroyTheSpiderSpider2, search2)
    process.crawl(LeroyTheSpiderSpider3, search3)

    process.start()