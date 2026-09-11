import scrapy
from scraper.items import ProductItem


class PriceSpider(scrapy.Spider):
    name = "price_spider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        products = response.css("article.product_pod")
        for product in products:
            item = ProductItem()
            item['title'] = product.css("h3 a::attr(title)").get()

            raw_price = product.css("p.price_color::text").get()
            item['price'] = float(raw_price.replace("£", "").replace("$", "")) if raw_price else 0.0

            item['availability'] = product.css("p.instock.availability::text").getall()[-1].strip()
            item['url'] = response.urljoin(product.css("h3 a::attr(href)").get())

            yield item