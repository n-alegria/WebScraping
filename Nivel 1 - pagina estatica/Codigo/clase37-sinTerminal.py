from scrapy.item import Field, Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess

class Noticia(Item):
    id = Field()
    titular = Field()
    descripcion = Field()

class ElUniversoSpider(Spider):
    name = 'MiSegundoSpider'
    custom_settings = {
                'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
                'FEED_EXPORT_FIELDS': ['id', 'descripcion', 'titular'],  # Como ordenar las columnas en el CSV?
                'CONCURRENT_REQUESTS': 1,  # numero de requerimientos concurrentes
                'FEED_EXPORT_ENCODING': 'utf-8'
    }
    start_urls = ['https://eluniverso.com/deportes']
    def parse(self, response):
        # -> con SCRAPY
        sel = Selector(response)
        # obtengo el contenedor y de este un listado de noticias
        noticias = sel.xpath('//div[contains(@class, "content-feed")]/ul/li')
        i = 0
        for noticia in noticias:
            item = ItemLoader(Noticia(), noticia)
            item.add_value("id", i)
            item.add_xpath("titular", ".//h2/a/text()")
            item.add_xpath("descripcion", ".//p/text()")
            i += 1
            yield item.load_item()


process = CrawlerProcess({
    'FEED-FORMAT': 'csv',
    'FEED-URI': 'resultado37.csv'
})
process.crawl(ElUniversoSpider)
process.start()


