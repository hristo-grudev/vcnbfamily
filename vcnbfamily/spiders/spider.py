import scrapy

from scrapy.loader import ItemLoader

from ..items import VcnbfamilyItem
from itemloaders.processors import TakeFirst


class VcnbfamilySpider(scrapy.Spider):
	name = 'vcnbfamily'
	start_urls = ['https://vcnbfamily.me/2014/01/07/new-year-new-blog-for-vcnb/']

	def parse(self, response):
		title = response.xpath('//header/h1/text()').get()
		description = response.xpath('//div[@class="entry-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//time[@class="entry-date"]/text()').get()

		item = ItemLoader(item=VcnbfamilyItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		yield item.load_item()

		next_page = response.xpath('//span[@class="nav-next"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)
