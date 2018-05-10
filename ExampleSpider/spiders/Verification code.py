import scrapy
from scrapy import Request, FormRequest
import json
from PIL import Image
from io import BytesIO
import pytesseract
from scrapy.log import logger


class CaptchaLoginSpider(scrapy.Spider):
    name = 'login_captcha'
    start_urls = ['']

    def parse(self, response):
        # X 网站登录页面的url（ 虚构的）
        login_url = 'http://XXX.com/login'
        user = 'liushuo@XXX.com'
        password = '12345678'

    def start_requests(self):
        yield Request(self.login_url, callback=self.login, dont_filter=True)

    def login(self, response):
        login_response = response.meta.get('login_response')

        if not login_response:
            # Step 1:
            # 此时response 为登录页面的响应， 从中提取验证码图片的url， 下载验证码图
            captchaUrl = response.css('label.field.prepend-icon img::attr()').extract_first()

            captchaUrl = response.urljoin(captchaUrl)
            # 　构造Request　时，将当前response　保存到meta 字典中
            yield Request(captchaUrl, callback=self.login, meta={'login_response': response},
                          dont_filter=True)

        else:
            # 　此时 response为验证码图片响应， reponse.body是图片
            # login_response 为登录页面的响应，用其构造表单请求并且发送登录
            formdata = {
                'email': self.user,
                'pass': self.password,
                # 　使用OCR 识别
                'code': self.get_captcha_by_OCR(response.body),
            }
            yield FormRequest.from_response(login_response, callback=self.parse,
                                            formdata=formdata, )

        # 处理表单请求而的响应
        def parse_login(self, response):
            # 根据响应判断是否登录成功
            info = json.loads(response.text)
            if info['error'] == '0':
                logger.info('登录成功')
                return super().start_requests()
            logger.info('登录失败')
            return self.start_requests()

        def get_captcha_by_OCR(self, data):
            # OCR 识别
            img = Image.open(BytesIO(data))
            img = img.convert('L')
            captcha = pytesseract.image_to_string(img)
            img.close()
            return captcha