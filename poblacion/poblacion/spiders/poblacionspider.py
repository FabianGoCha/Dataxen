import scrapy
from poblacion.items import PoblacionItem


class PoblacionspiderSpider(scrapy.Spider):
    name = "poblacionspider"
    allowed_domains = ["cuentame.inegi.org.mx"]
    start_urls = ["https://cuentame.inegi.org.mx/monografias/informacion/mex/poblacion/default.aspx?tema=me"]

    def parse(self, response):
        
        columnas = response.xpath('//*[@id="keywords"]/thead//th')
        nombres_columnas = []
        for columna in columnas:
            nombre = columna.css('strong::text').get()
            nombres_columnas.append(nombre.strip())            

        filas = response.xpath('//*[@id="keywords"]/tbody//tr')

        for fila in filas:
            campos = fila.css("td")
            valores = []
            for campo in campos:
                valor = campo.css("::text").get()
                valor.strip()
                valor= ' '.join(valor.split())
                valores.append(valor)
            
            res = {nombres_columnas[i]: valores[i] for i in range(len(nombres_columnas))}
            yield res
    