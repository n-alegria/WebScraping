from scrapy.item import Item, Field
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess


# Creo una nueva clase la cual sera el ItemLoader
class Hotel(Item):
    nombre = Field()
    score = Field()
    descripcion = Field()
    amenities = Field()


# Clase nucleo (spider)
# Al ser scraping dinamico no hereda de 'Spider'
class TripAdvisor(CrawlSpider):
    name = 'Hoteles'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      'Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    # Defino la url semilla
    start_urls = ['https://www.tripadvisor.com.ar/Hotels-g312741-Buenos_Aires_Capital_Federal_District-Hotels.html']

    # Ahora debo definir varios parametros nuevos

    '''
    download_delay: 
    Tiempo de espera entre cada requerimiento que se haga a cada pagina a la que vaya a partir de la URL semilla
    '''
    # espera 2 segundos antes de ir a la pagina nueva
    download_delay = 2

    '''
    rules:
    es una tupla (lista inmutable)
    Son el orquestador de mi CrawlSpider. Son reglas que definen a cuales links dentro de la URL semilla mi Spider
    tiene o no que in en busqueda de informacion.
    '''
    # Las reglas van a ser escritas basadas en patrones que yo encuentr dentro de la URLs a las cuales quiero dirigirme
    # Debo analizar las URL del Scraping Horizontal para encontar el patron
    rules = (
        Rule(
            # Clase que permite extraer los links (URLs) de una pagina
            # Con este extractor solo extraer links que tnegan dentro la cadena expresada
            # -->> LinkExtractor() extraer links de la pagina semilla que encajan con el patron.
            # -->> Rule() es la que dictamina si sigo o no estos links extraidos por el LinkExtractor()
            LinkExtractor(
                # Recibe como parametro 'allows' el cual recibe una expresion regular la cual me indica a cual pagina
                # tengo permitido redirigirme
                allow=r'/Hotel_Review-'
            ),
            # 'follow' define si tiene que seguir los links
            follow=True,
            # Tambien debo definir una funcion 'callback' la cual sera invocada cada vez que se infrese a estas URLs
            callback='parse_hotel'
        ),
    )

    def parse_hotel(self, response):
        sel = Selector(response)
        item = ItemLoader(Hotel(), sel)

        item.add_xpath('nombre', '//h1[@id="HEADING"]/text()')
        item.add_xpath('score', '//div[@class="kVNDLtqL"]/span/text()')
        item.add_xpath('descripcion', '//div[contains(@class, "_2-hMril5")]/div[@class="cPQsENeY"]/div/p/text()')
        item.add_xpath('amenities', '//div[@class="_1nAmDotd"][1]/div[@class="_2rdvbNSg"]/text()')

        yield item.load_item()


process = CrawlerProcess({
    'FEED-FORMAT': 'json',
    'FEED-URI': 'resultado39.json'
})
process.crawl(TripAdvisor)
process.start()

