import scrapy


class CovidSpiderSpider(scrapy.Spider):
    name = "covid_spider"
    allowed_domains = ["salud.edomex.gob.mx"]
    start_urls = ["https://salud.edomex.gob.mx/salud/covid19_municipio"]

    def parse(self, response):
        tabla = response.css("table")
        filas = tabla.css("tr")
        nombres_columnas = []
        columnas = filas[0].css("th")
        for columna in columnas:
            nombre = columna.css('::text').get()
            nombres_columnas.append(nombre.strip())  
        
        for fila in filas[1:]:
            cabeza_fila = fila.css("th")
            campos = fila.css("td")

            valores = []

            valor = cabeza_fila.css("::text").get()
            valor.strip()
            valor= ' '.join(valor.split())
            valores.append(valor)

            for campo in campos:
                valor = campo.css("::text").get(default='')
                valor.strip()
                valor= ' '.join(valor.split())
                valores.append(valor)
            
            res = {nombres_columnas[i]: valores[i] for i in range(len(nombres_columnas))}
            yield res

