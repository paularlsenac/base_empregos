import scrapy
import time
import re
import math
from datetime import datetime


class BneSpyder(scrapy.Spider):

    name = 'infojobs'
    allowed_domains = ['infojobs.com.br']

    provincias = [64, 184, 182, 176, 172, 187, 179, 171, 190, 174, 175, 189, 173, 181, 170, 183, 178, 180, 166, 188,
                  165, 185, 169, 168, 186, 177, 167]
    start_urls = ['https://www.infojobs.com.br/empregos.aspx?provincia={}'.format(str(p)) for p in provincias]

    def parse(self, response):

        jobs = response.xpath("//div[@id='filterSideBar']//div[starts-with(@id, 'vacancy')]")
        for job in jobs:

            link = job.xpath("@data-href").extract()
            data = job.css(".js_date::attr(data-value)").extract()
            print(link, data)

        next_page = response.xpath(".//ul[@class='pagination justify-content-center']/li/a[@title='Próxima']/@href").get()
        if next_page is not None:
            yield response.follow(next_page, encoding='latin-1', callback=self.parse)

    def parse_job(self, response, data):

        job = response.xpath("//div[@id='vacancylistDetail']")
        job_title = job.xpath("//h2[@class='font-weight-bolder mb-4']/text()").extract_first()
        empresa = job.xpath("//div[@class='h4']/text()").extract_first()
        cidade = job.xpath("//div[@class='text-medium mb-4']/text()").extract()[0].strip()
        salario = job.xpath("//div[@class='text-medium mb-4']/text()").extract()[-1].strip().strip().replace(" ","").replace("\n","")
        descrip = job.xpath("//p[@class='mb-16 text-break']/text()").extract()[0].strip().replace("\n", "").replace("\r","")
