# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
from shanbay.items import ShanbayItem
import sys
import io
import json
import http.cookiejar as cookielib


class SbSpider(scrapy.Spider):
    name = 'sb'
    allowed_domains = ['www.shanbay.com']
    start_urls = 'https://www.shanbay.com/team/members/#p1'
    headers = {
        'host': "www.shanbay.com",
        'origin': "https://www.shanbay.com",
        'referer': "https://www.shanbay.com",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36",
        'x-csrftoken': "VZI1D6NFtrGJBIHQpWwULWJk53CMTqbq",
    }
    cookie_str='track_id=fe54020a-fe64-11e6-8101-00163e000154; _ga=GA1.2.1440727743.1482975767; __utmz=183787513.1524907053.1237.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utma=183787513.1440727743.1482975767.1527695758.1527740643.1342; __utmc=183787513; __utmt=1; _gat=1; csrftoken=tqFmuzwTKwVhVeObvXAsURxJ9WiyzayT; sessionid=".eJyrVopPLC3JiC8tTi2KT0pMzk7NS1GyUkrOz83Nz9MDS0FFi_UCUotyM4uLM_PznFJTnaBqdZANyATqNTQwtzAwMjY3qAUAR8Mg8A:1fOF8C:5MoGucPNTVkyTeV8Fi4soFrCewQ"; userid=107802370; auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImZlbmd5dWVyMjAxNyIsImRldmljZSI6MCwiaXNfc3RhZmYiOmZhbHNlLCJpZCI6MTA3ODAyMzcwLCJleHAiOjE1Mjg2MDQ2NDl9.Xnubfe9W_5fXpwBdndYv0hxiiA2BfH5db3zpaxkISog; __utmb=183787513.7.10.1527740643'
    cookies = {}
    for line in cookie_str.split(';'):
        key, value = line.split('=', 1)
        cookies[key] = value
    global listen_num,word_num,reading_num,sentence_num,course_num,training_num,study_time,i,speaking_num
    listen_num = 0
    word_num = 0
    reading_num = 0
    sentence_num = 0
    course_num = 0
    training_num = 0
    study_time = 0
    speaking_num= 0
    i = 2
    # 为了方便 暂时采用cookie登陆
    def start_requests(self):
        return [Request(self.start_urls, cookies=self.cookies, headers=self.headers, callback=self.parse)]
    # def start_requests(self):
    #     return [scrapy.Request('https://www.shanbay.com/web/account/login', headers=self.headers,callback=self.shanbay_login)]
    # def shanbay_login(self,response):
    #     captcha_url = 'https://www.shanbay.com/api/v1/account/captcha/'
    #     post_data = {'username': 'fengyuer2017',
    #                  'password': 'qgs1995',
    #                  'key': '',
    #                  'code': ''
    #                  }
    #     # 在发送get请求时带上请求头和cookies
    #     # post_data = json.dumps(post_data)
    #     yield scrapy.Request(captcha_url, headers=self.headers, meta={"post_data":post_data},callback=self.captcha)
    # def captcha(self,response):
    #     captcha_json = json.loads(response.text)
    #     post_data = response.meta.get("post_data", {})
    #     key = captcha_json["data"]["key"]
    #     post_data["key"] = key
    #     image_url = captcha_json["data"]["image_url"]
    #     yield scrapy.Request(image_url, headers=self.headers, meta={"post_data":post_data},callback=self.login_aftercaptcha)
    # def login_aftercaptcha(self,response):
    #     with open("captcha.jpg", "wb") as f:
    #         f.write(response.body)
    #         f.close()
    #     from PIL import Image
    #     try:
    #         im = Image.open('captcha.jpg')
    #         im.show()
    #         im.close()
    #     except:
    #         pass
    #     code = input("输入验证码：\n")
    #     post_data = response.meta.get("post_data", {})
    #     post_data["code"] = code
    #     post_url = 'https://www.shanbay.com/api/v1/account/login/web/'
    #     return [scrapy.FormRequest(post_url, method='PUT',body=json.dumps(post_data), headers={'Content-Type': 'application/json'},callback=self.check_login)]
    #     # 2018.4.30 注意扇贝网需要发送json数据 故采用上述格式

    # def check_login(self, response):
    #     # 验证服务器的返回数据判断是否成功
    #     text_json = json.loads(response.text)
    #     if "msg" in text_json and text_json["msg"] == "SUCCESS":
    #         for url in self.start_urls:
    #             yield scrapy.Request(url, dont_filter=True, headers=self.headers)

    # 登陆后解析页面
    def parse(self, response):
        # person_url = 'https://www.shanbay.com/checkin/user/27992611/'
        # yield scrapy.Request(person_url, cookies=self.cookies, meta={"user_name": 'user_name'}, headers=self.headers,
        #                      callback=self.parse_person)
        global i
        person_urls = response.css('.user a.nickname')
        for person_url in person_urls:
            user_name = person_url.css('::text').extract_first()
            person_url = person_url.css('::attr(href)').extract_first()
            person_url_p = 'https://www.shanbay.com'+person_url+'?page=1'
            yield scrapy.Request(person_url_p, cookies=self.cookies, meta={"user_name": user_name}, headers=self.headers, callback=self.parse_person)
        if i <= 3:
            next_url = 'https://www.shanbay.com/team/members/?page='+str(i)+'#p1'
            i = i+1
            yield scrapy.Request(next_url, cookies=self.cookies, callback=self.parse)

    def parse_person(self, response):
        global listen_num,sentence_num,word_num,course_num,training_num,reading_num,study_time,speaking_num
        model = ".*?(\d+).*([\u4E00-\u9FA5]{2})"
        learn_detail = response.xpath('//div[@class="note"]/text()').extract()
        for k in learn_detail:
            tag_list = re.split(r'[;|\，|；]', k.strip())
            for tag in tag_list:
                match_re = re.match(model, tag)
                if match_re:
                    # 统计学习情况
                    if match_re.group(2) == '听力':
                        listen_num = listen_num+int(match_re.group(1))
                    elif match_re.group(2) == '文章':
                        reading_num = reading_num+int(match_re.group(1))
                    elif match_re.group(2) == '单词':
                        word_num = word_num+int(match_re.group(1))
                    elif match_re.group(2) == '炼句':
                        sentence_num = sentence_num+int(match_re.group(1))
                    elif match_re.group(2) == '训练':
                        training_num = training_num+int(match_re.group(1))
                    elif match_re.group(2) == '课程':
                        course_num = course_num+int(match_re.group(1))
                    elif match_re.group(2) == '口语':
                        speaking_num = study_time+int(match_re.group(1))
                    elif match_re.group(2) == '分钟':
                        study_time = study_time+int(match_re.group(1))
                    else:
                        pass
        user_name = response.meta.get("user_name", "")
        word_url = response.css('.avatar.span1 a::attr(href)').extract_first()
        word_url = 'https://www.shanbay.com'+word_url
        yield scrapy.Request(word_url,meta={"user_name": user_name,"listen_num": listen_num,"word_num": word_num,"sentence_num":sentence_num,"training_num": training_num,"course_num": course_num,"reading_num": reading_num,"study_time": study_time,"speaking_num": speaking_num},cookies=self.cookies,headers=self.headers,callback=self.parse_word)
        listen_num = 0
        word_num = 0
        sentence_num = 0
        training_num = 0
        course_num = 0
        reading_num = 0
        study_time = 0
        speaking_num = 0

    def parse_word(self, response):
        vocabulary = response.css('span.label.label-info.highlight::text')
        voc_all = vocabulary.extract()[0]
        voc_grasp = vocabulary.extract()[1]
        user_name1 = response.meta.get("user_name", "")
        listen_num1 = response.meta.get("listen_num", "")
        word_num1 = response.meta.get("word_num", "")
        sentence_num1 = response.meta.get("sentence_num", "")
        training_num1 = response.meta.get("training_num", "")
        course_num1 = response.meta.get("course_num", "")
        reading_num1 = response.meta.get("reading_num", "")
        speaking_num1 = response.meta.get("speaking_num", "")
        study_time1 = response.meta.get("study_time", "")

        study_item = ShanbayItem()
        study_item['user_name'] = user_name1
        study_item['listen_num'] = listen_num1
        study_item['word_num'] = word_num1
        study_item['sentence_num'] = sentence_num1
        study_item['training_num'] = training_num1
        study_item['course_num'] = course_num1
        study_item['reading_num'] = reading_num1
        study_item['speaking_num'] = speaking_num1
        study_item['study_time'] = study_time1
        study_item['voc_all'] = int(voc_all)
        study_item['voc_grasp'] = int(voc_grasp)
        yield study_item
