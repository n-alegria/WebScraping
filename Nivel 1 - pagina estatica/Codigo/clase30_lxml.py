# importo las librerias
# -> para los requerimientos
import requests
# -> para parsear de texto a html
from lxml import html

'''
Antres de realizar el requerimiento debo modificar los encabezados (datos adicionales que sirven al servidor
para saber quien esta haciendo el requerimiento o como lo esta haciendo)
La que usaremos es "user-agent" la cual no me bloqueara la ip
'''
encabezados = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/80.0.3987.149 Safari/537.36"
}

# defino la 'url' semilla
url = 'https://wikipedia.org/'

# realizo el requerimiento a la url, añadiendo el encabezado
respuesta = requests.get(url, headers=encabezados)
# para no tener caracteres raros puedo hacer un 'encoding' de la respuesta
# -> ojo que no todos los programas pueden almacenar bien los datos (ejemplo: excel)
respuesta.encoding = 'UTF-8'

# parseo el texto en html
parser = html.fromstring(respuesta.text)

# comienzo a obtener los datos que quiero desde el parser
'''
hay muchos metodos disponibles:
parser.get_elements_by_id('valor del id que deseo obtener')
parser.xpath('expresion del elemento')
parser.find_class('valor de la clase')
'''

'''
# almaceno el elemento que coicide con mi busqueda en la variable
elemento = parser.get_element_by_id('js-link-box-en')

# para imprimirla debo usar el metodo '.text_content()' de lo contrario me imprimira el tipo
print(elemento.text_content())
'''

'''
elemento = parser.xpath("//a[@id='js-link-box-en']/strong/text()")
print(elemento)
'''

# OBTENGO TODOS LOS IDIOMAS
idiomas = parser.xpath('//div[contains(@class, "central-featured-lang")]/a/strong/text()')
for idioma in idiomas:
    print(idioma)