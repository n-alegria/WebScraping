import requests
from lxml import html

'''   Voy a obtener el titulo y las caracteristicas y sus redes   '''

encabezados = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/80.0.3987.149 Safari/537.36"
}

url = 'https://www.imuniapp.com/'

respuesta = requests.get(url, headers=encabezados)
respuesta.encoding = 'UTF-8'

parser = html.fromstring(respuesta.text)

# comienzo a obtener los datos que quiero desde el parser
'''
hay muchos metodos disponibles:
parser.get_elements_by_id('valor del id que deseo obtener')
parser.xpath('expresion del elemento')
parser.find_class('valor de la clase')
'''

# titulo y caracteristicas con xPath
titulo = parser.xpath("//h1/text()")
caracteristicas = parser.xpath("//h3/text()")
redes = parser.xpath("//ul[contains(@class, 'list-social')]//a/@href")

print(f"Titulo: {titulo[0]}\n")

textoCaracteristicas = "Caracteristicas: "
for caracteristica in caracteristicas:
    textoCaracteristicas += f"{caracteristica}, "

textoCaracteristicas = textoCaracteristicas[:-2]
textoCaracteristicas += '...'

print(textoCaracteristicas)

print("\nRedes:")
for red in redes:
    print(red)
