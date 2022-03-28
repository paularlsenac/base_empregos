import scrapy
import re
import math
from datetime import datetime


class BneSpyder(scrapy.Spider):

    name = 'bne'
    allowed_domains = ['bne.com.br']
    start_urls = ['https://www.bne.com.br/vagas-de-emprego']

    def parse(self, response):

        title = response.xpath(".//h1[@class='joblist__title']/strong/text()").extract()[0]
        n_jobs = int(re.findall('\d+', title)[0])
        n_pages = int(math.ceil(n_jobs/10))
        print("Existem {} empregos publicados no site hoje. Será necessário visitar {} páginas para extrair a info.".
              format(n_jobs, n_pages))

        base_url = 'https://www.bne.com.br/vagas-de-emprego/'
        for page in range(1, n_pages + 1):
            yield scrapy.Request(base_url + "?page={}".format(page), encoding='latin-1', callback=self.parse_job)

    def parse_job(self, response):

        joblist = response.css(".job")

        if not joblist:
            print("no response")
            print(response)
            raise ValueError

        for job in joblist:

            link = job.xpath(".//a[@class='linkDesktop is-link']/@href").get()
            code = [x.rstrip() for x in job.xpath(".//div[@class='tag']/text()").getall()]
            code = list(filter(lambda x: x != "", code))[0]
            name = job.xpath(".//a[@class='linkDesktop is-link']/text()").get()

            data = {"datade_extração": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                    "link": link,
                    "code": code,
                    "name": name}

            if link is not None:
                new_url = "https://www.bne.com.br" + link
                print(new_url)
                request = scrapy.Request(new_url, callback=self.parse_jobdetails)
                request.cb_kwargs['data'] = data
                yield request

    def parse_jobdetails(self, response, data):

        cargo = response.xpath(".//h2[@class='job__detail']/text()").extract_first().strip()

        loc = response.xpath(".//div[@class='job']//dl/dd/text()").extract()
        if len(loc) > 1:
            loc = loc[-1].strip()
        else:
            loc = loc[0].strip()

        salario = response.xpath(
            ".//div[@class='job']//h3[@class='job__detail']/span[contains(text(), 'Salário')]/ancestor::h3/text()") \
            .extract_first().strip()

        empresa = response.xpath(
            ".//div[@class='job']//h3[@class='job__detail']/span[contains(text(), 'Empresa')]/following-sibling::span/text()") \
            .extract_first().replace(".", "").replace("-", "").strip()

        if len(response.xpath(".//span[@id='tag-releaseDate']").extract()) > 0:
            recente = True
        else:
            recente = False

        descricao = response.xpath(
            ".//div[@class='job__description']/h2[contains(text(), 'Descrição Geral')]/following-sibling::h3/text()") \
            .extract_first().strip()

        other_data = dict()
        for term in ["Requisitos", "Atribuições", "Tipo de Vínculo", "Benefícios"]:
            other_data[term] = response.xpath(".//div[@class='job__description']/h2[contains(text(), '%s')]\
                                                /following-sibling::h3[preceding-sibling::h2[1][contains(text(), '%s')]]\
                                                /text()" % (term, term)).extract()
            other_data[term] = " ".join([r.strip().replace("\n", "").replace("\r", "") for r in other_data[term]]).strip()

        data["cargo"] = cargo
        data["localização"] = loc
        data["salário"] = salario
        data["empresa"] = empresa
        data["recente"] = recente
        data["descrição"] = descricao
        for k, v in other_data.items():
            data[k.lower()] = v

        yield data
