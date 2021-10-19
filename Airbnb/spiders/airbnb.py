import scrapy
from scrapy_splash import SplashRequest


class AirbnbSpider(scrapy.Spider):
    name = 'airbnb'
    allowed_domains = ['airbnb.com']
    start_urls = ['https://www.airbnb.com/s/California--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&date_picker_type=calendar&query=California%2C%20United%20States&place_id=ChIJPV4oX_65j4ARVW8IJ6IJUYs&source=structured_search_input_header&search_type=autocomplete_click']

    def parse(self, response):
        urls = response.xpath('//*[@class="_8s3ctt"]/a/@href').getall()
        for url in urls:
            absolute_url = response.urljoin(url)
            yield scrapy.Request(absolute_url, callback=self.parse_items)
    
    def parse_items(self, response):
        filters_script = """function main(splash, args)
                                headers = {
                                    ['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
                                }
                                splash:set_custom_headers(headers)
                                assert(splash:go(args.url))
                                assert(splash:wait(5))
                                return splash:html()
                                end"""
        yield SplashRequest(url=response.url,
                            callback=self.parse_product,
                            endpoint='execute',
                            args={'lua_source': filters_script})
            
            
    def parse_product(self, response):
        name = response.xpath('//*[@class="_mbmcsn"]/h1/text()').get()
        # for img_url in response.xpath('//*[@class="_4626ulj"]/picture/img/@src'):
        #     if img_url:
        #         continue
        yield {
            'Nmae': name
            #'Img': img_url
        }
    
            
