import scrapy
from scrapy.http import Request, FormRequest


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['example.webscraping.com']
    start_urls = ['http://example.webscraping.com/user/profile']

    def parse(self, response):
        # 解析登录后的下载页面
        keys = response.css('table label::text').re('(.+):')
        values = response.css('table td.w2p_fw::text').extract()
        yield dict(zip(keys, values))

    # 登录页面的url
    login_url = 'http://example.webscraping.com/places/default/user/login'

    # 覆写基类方法
    def start_requests(self):
        yield Request(self.login_url, callback=self.login)

    def login(self, response):
        # 登录页面的解析函数，构造FormRequest对象提交表单
        fd = {'email': '18273711329@163.com', 'password': 'hlz18273711329'}
        yield FormRequest.from_response(response, formdata=fd, callback=self.parse_login)

    def parse_login(self, response):
        # 登录成功后，继续爬取　start_url的页面
        if 'Welcome' in response.text:
            yield from super().start_requests()  # 成功后再调用基类方法
