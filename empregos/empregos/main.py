from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import postproc


process = CrawlerProcess(get_project_settings())

process.crawl('bne')
process.start()

# open file

postproc.pos_proc("C:\\Users\\paula\\Projects\\senac\\empregos\\empregos\\empregos\\bne.json")
