import requests
import json
from bs4 import BeautifulSoup

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/80.0.3987.149 Safari/537.36"
}

url = 'https://stackoverflow.com/questions'
respuesta = requests.get(url, headers=headers)

# instancio un nuevo objeto del tipo BeautifulSoup pasando como argumento el texto de la respuesta y el parseador
soup = BeautifulSoup(respuesta.text, "html.parser")

# obtengo el contenedor global de las preguntas (id='questions')
contenedor_de_preguntas = soup.find(id='questions')

# ahora buscare dentro de este contenedor, no dentro del 'soup'
# buscare las preguntas utilizando el metodo '.find_all()'
lista_de_preguntas = contenedor_de_preguntas.find_all(class_='question-summary')

dic = dict()

# en 'pregunta' tendre el elemento el cual tendre que volver a filtrar para obtener lo que deseo
# titulo de la pregunta y su descripcion
for pregunta in lista_de_preguntas:
    texto_pregunta = pregunta.find('h3').text
    descripcion_pregunta = pregunta.find(class_='excerpt').text
    # elimina cualquier espacio al inicio o al final de una cadena
    descripcion_pregunta = descripcion_pregunta.strip()
    # .replace() reemplaza el primer parametro por el segundo
    descripcion_pregunta = descripcion_pregunta.replace('\n', '').replace('\t', '').replace('\r', '')
    dic[texto_pregunta] = descripcion_pregunta
    # print(texto_pregunta)
    # print(descripcion_pregunta + '\n')

try:
    ar = open('stackOverflow.json', 'w')
    ar.write(json.dumps(dic))
    ar.close()
    print('Archivo generado con exito')
except Exception as e:
    print(e)