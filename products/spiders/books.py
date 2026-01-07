import scrapy


class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response, **kwargs):
        for product in response.css(".product_pod"):
            urls = product.css("h3 a::attr(href)").get()
            book_url = response.urljoin(urls)

            yield scrapy.Request(book_url, callback=self.parse_book)

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_book(self, response):
        yield {
            "title": response.css("h1::text").get(),
            "price": response.css(".price_color::text").get().replace("£", ""),
            "amount_in_stock": response.css(".instock::text").re_first(r'\d+'),
            "rating": response.css(".star-rating::attr(class)").get().split()[-1],
            "category": response.css("ul.breadcrumb li a::text")[-1].get(),
            "description": response.css("#product_description + p::text").get(),
            "upc": response.css(".table-striped tr:nth-child(1) td::text").get(),
        }
