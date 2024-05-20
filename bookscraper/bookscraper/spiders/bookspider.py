from wsgiref import headers
import scrapy
import random
from bookscraper.items import BookItem

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    custom_settings = {
        "FEEDS": {"booksdata.json": {"format": "json", 'overwrite': True}},
    }

    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    ]

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            relative_url = book.css('h3 a::attr(href)').get()

            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
                
            yield response.follow(book_url, callback=self.parse_book_page, headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list)-1)]})
        
        
        next_page = response.css('li.next a::attr(href)').get()

        if next_page:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page

            yield response.follow(next_page_url, callback=self.parse, headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list)-1)]})

    # def parse_book_page(self, response):
    #     table_rows = response.css("table tr")

    #     yield {
    #         "url": response.url,
    #         "title": response.css(".product_main h1::text").get(),
    #         "product_type": table_rows[1].css("td ::text").get(),
    #         "price_excl_tax": table_rows[2].css("td ::text").get(),
    #         "price_incl_tax": table_rows[3].css("td ::text").get(),
    #         "price": response.css("p.price_color::text").get(),
    #         "tax": table_rows[4].css("td ::text").get(),
    #         "availability": table_rows[5].css("td ::text").get(),
    #         "num_reviewa": table_rows[6].css("td ::text").get(),
    #         # "image_url": response.css(".item img::attr(src)").get(),
    #         "stars": response.css("p.star-rating").attrib["class"],
    #         "category": response.xpath("//ul[@class='breadcrumb']/li[1]/a/text()").get(),
    #         "description": response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
    #     }
    def parse_book_page(self, response):
        table_rows = response.css("table tr")
        book_item = BookItem()

        book_item['url'] = response.url,
        book_item['title'] = response.css(".product_main h1::text").get(),
        book_item['upc'] = table_rows[0].css("td ::text").get(),
        book_item['product_type'] = table_rows[1].css("td ::text").get(),
        book_item['price_excl_tax'] = table_rows[2].css("td ::text").get(),
        book_item['price_incl_tax'] = table_rows[3].css("td ::text").get(),
        book_item['price'] = response.css("p.price_color::text").get(),
        book_item['tax'] = table_rows[4].css("td ::text").get(),
        book_item['availability'] = table_rows[5].css("td ::text").get(),
        book_item['num_reviews'] = table_rows[6].css("td ::text").get(),
        book_item['stars'] = response.css("p.star-rating").attrib["class"],
        book_item['category'] = response.xpath("//ul[@class='breadcrumb']/li[1]/a/text()").get(),
        book_item['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()

        yield book_item
