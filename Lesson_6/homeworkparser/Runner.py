from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from Lesson_6.homeworkparser.spiders.labirint import LabirintSpider
from Lesson_6.homeworkparser.spiders.book24 import book24Spider
from Lesson_6.homeworkparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LabirintSpider)
    # process.crawl(book24)

    process.start()