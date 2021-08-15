# importo las librerias
from scrapy.item import Field, Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader


# creo mi prime clase que sera la abstraccion de lo que deseo extraer
# la clase debe heredar de 'Item'
class Pregunta(Item):
    # ahora defino las propiedades que voy a extraer
    id = Field()
    pregunta = Field()
    descripcion = Field()


# defino la clase principal la cual heredara de 'Spider'
class StackOverflowSpider(Spider):
    name = 'MiPrimerSpider'
    # debo definir el 'user-agent' para evitar el baneo
    custom_settings = {
        "USER-AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/80.0.3987.149 Safari/537.36"
    }

    # defino la 'url' semilla
    start_urls = ['https://stackoverflow.com/questions/']

    # creo la funcion que me permitira parsear el arbol
    def parse(self, response):
        sel = Selector(response)
        preguntas = sel.xpath('//div[@id="questions"]//div[@class="question-summary"]')
        i = 0
        for pregunta in preguntas:
            item = ItemLoader(Pregunta(), pregunta)
            item.add_xpath('pregunta', './/h3/a/text()')
            item.add_xpath('descripcion', './/div[@class="excerpt"]/text()')
            item.add_value('id', i)
            i += 1
            
            yield item.load_item()