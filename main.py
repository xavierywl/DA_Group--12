#To run scrappy command = scrapy runspider main.py -s USER_AGENT="Mobile"
# Use the Request library
import requests
import scrapy

url = 'https://www.whisky.sg/product-category/scotch-whisky/'
url2 = 'http://httpbin.org/headers'


# Set the target webpage
r = requests.get(url)

# This will get the full page
# print(r.text)
# This will get the status code
print("Status code:")
print("\t *", r.status_code)

# This will get just the headers
h = requests.head(url)
print("Header:")
print("**********")
# To print line by line
for x in h.headers:
    print("\t ", x, ":", h.headers[x])
print("**********")

# This will modify the headers user-agent
headers = {
    'User-Agent': "Mobile"
}
# Test it on an external site
r2 = requests.get(url2, headers=headers)
print(r2.text)

#Task 5
class Whiskyspider(scrapy.Spider):
    name = 'Whisky'
    start_urls = [url]

    def parse(self, response):
        SET_SELECTOR = '.product-wrap'
        for Whisky in response.css(SET_SELECTOR):
            IMG_SELECTOR = 'img ::attr(data-src-webp)'
            yield {
                'image': Whisky.css(IMG_SELECTOR).extract_first(),
            }
#For next page
        NEXT_PAGE_SELECTOR = '.woocommerce-pagination > ul.page-numbers > li > a.next.page-numbers ::attr("href")'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
