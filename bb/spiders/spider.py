import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import BbItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class BbSpider(scrapy.Spider):
	name = 'bb'
	start_urls = ['https://www.bb.com.br/portalbb/page120,3366,3367,1,0,1,0.bb?codigoNoticia=0&pk_vid=bc39be207bf881101618837721b1d3b2']

	def parse(self, response):
		post_links = response.xpath('//a[@class="linkChamada_5"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//div[@class="data"]/text()').get()
		if not date:
			date = "Date is not stated in article"
		title = response.xpath('//h2/text()').get()
		content = response.xpath('//div[@class="grade_78 chamadaNoticia"][position()>1]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=BbItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
