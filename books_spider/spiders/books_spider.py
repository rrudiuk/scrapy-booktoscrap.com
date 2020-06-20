import scrapy

class ToScrapeCSSSpider(scrapy.Spider):
    name = "books"
    start_urls = [
        'http://books.toscrape.com/',
    ]

    def parse(self, response):
        # Access book page for each book
        books_page_links = response.css('h3 a')
        yield from response.follow_all(books_page_links, self.parse_book)

        # Go through all pages
        pagination_links = response.css('.next a')
        yield from response.follow_all(pagination_links, self.parse)

    # Pasrse book page
    def parse_book(self, response):

        img = response.css('img').attrib['src']
        img = img.replace('../../','http://books.toscrape.com/')
        rating = response.xpath('//*[contains(@class, "star-rating")]/@class').extract_first()
        rating = rating.replace('star-rating ', '')

        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'name': extract_with_css('h1::text'),
            'price': extract_with_css('.price_color::text'),
            'image': img,
            'description': extract_with_css('#product_description + p::text'),
            'upc': extract_with_css('tr:nth-child(1) td::text'),
            'product_type': extract_with_css('tr:nth-child(2) td::text'),
            'price_without_tax': extract_with_css('tr:nth-child(3) td::text'),
            'price_with_tax': extract_with_css('tr:nth-child(4) td::text'),
            'in_stock': extract_with_css('tr:nth-child(6) td::text'),
            'reviews_number': extract_with_css('tr:nth-child(7) td::text'),
            'rating': rating
        }

    #scrapy crawl books -o books.jl