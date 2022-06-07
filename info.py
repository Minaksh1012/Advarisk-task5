# from scrapy import Request, FormRequest
# from uuid import uuid4
# import csv
# import scrapy
# import pytesseract
# from PIL import Image
# from pytesseract import image_to_string
# import io
# from twocaptcha import TwoCaptcha
# import urllib3
# from urllib.parse import urlencode
# from files.utils import get_cookies
# from direct import ScrapeAspx
# import sys
# from pdf2image import convert_from_path
# import os
# import re
# import json

# pip install 2captcha-python

# class state_data(scrapy.Spider):
#     name="Epic_Info"
#     urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#     def start_requests(self):
#         yield Request('https://electoralsearch.in/Home/GetStateList',
#             meta={'cookiejar':str(uuid4)},
#             callback=self.parse) 
#     def parse(self,response):
#         # import pdb;pdb.set_trace()
#         # state_name[2]['state_code']
#         state_name=json.loads(response.text)
#         for i in state_name:
#             for j in i:
#                 print(i['state_code'])

        # s=state_name[state_code]
#         # print(state_name,"+++++++++++++++++")
# from webdriver_manager.chrome import ChromeDriverManager
# driver=webdriver.Chrome(ChromeDriverManager().install())
# driver.get("https://electoralsearch.in/##resultArea")
# driver.implicitly_wait(10)
# state_name=driver.find_elements("//*[@id='epicStateList']/option")
# print(state_name)

from bs4 import BeautifulSoup 
from os import getcwd
from twocaptcha import TwoCaptcha
from playwright.sync_api import sync_playwright 
from pymongo import MongoClient 
# def start_browser():
start_ply = sync_playwright().start()
browser = start_ply.chromium.launch(headless=False)
page =  browser.new_page()
# epic_no=collection.find_one(epics_no)
# epic_no='YPE1901305'
connection = MongoClient("mongodb://scraperDev:0mtNHqMELizgmHkp@dev-mongo-db.advarisk.com:27711/?ssl=false")
collection = connection['Land_Records']['TamilNadu_Epic_No']

# import pdb;pdb.set_trace()
page.goto('https://electoralsearch.in/##resultArea')
page.click("text='जारी रखें Continue'")
page.click('//*[@id="mainContent"]/div[2]/div/div/ul/li[2]')
page.click('//*[@id="name"]')

# for epic_no in collection:
epic_nos=collection.find()
for epic_no in epic_nos:
        print(epic_no['epics_no'])
        page.fill('//input[@id="name"]',epic_no['epics_no'])
                        
        cap=page.locator('//*[@id="captchaEpicImg"]')
        # import pdb ;pdb.set_trace()
        cap.screenshot(path='Captcha.jpg')
        Key_=TwoCaptcha('a0422b85d3ebe3b06bd34545dceb528e')
        # import pdb ;pdb.set_trace()
        page.click('//*[@id="txtEpicCaptcha"]')
        captcha_text=Key_.normal(getcwd()+'/Captcha.jpg',caseSensitive=1)
        print(captcha_text)

        url = 'https://electoralsearch.in/Home/searchVoter?epic_no={}&page_no=1&results_per_page=10&reureureired=ca3ac2c8-4676-48eb-9129-4cdce3adf6ea&search_type=epic&txtCaptcha={}'.format(epic_no['epics_no'], captcha_text['code'])
        print(url)
        import pdb; pdb.set_trace()

        # page.fill('//input[@id="txtEpicCaptcha"]',captcha_text['code'])
        # page.click('//*[@id="btnEpicSubmit"]')

        page.wait_for_load_state('networkidle')
        # page.s

        html_data = page.content()
        soup=BeautifulSoup(html_data,'html.parser')
        print(soup)
        # data=open('ka_12.html','w').write(page.content())
        # print(html_data)
        table=[i.text for i in soup.find_all('th')][1:]
        print(table)
        # print(table)
        # with open('Voter_list_data_{}.csv','a') as f:
        #     wr=csv.writer(f)
        #     for tr in table.xpath('.//thead/tr'):
        #         _tdata=[]
                        
        #         for td in tr.xpath('//td'):
        #             _text=(td.xpath('.//text()').extract())
        #             _tdata.append(_text)
        #         wr.writerow(_tdata)
        #         print(_tdata)
        # import pdb;pdb.set_trace()




        # soup = BeautifulSoup(html_data,'html.parser')
        # tableTag=soup.find_all('table',id='esultsTable')
        # print(tableTag)
        
        # Epic_no=response.xpath('//*[@id="resultsTable"]/thead/tr/text()').extract()
        # print(Epic_no)
        # open('ka_12.html','w').write(page.content())
        # with open ('ka_12.html')as f:
        #         soup=BeautifulSoup(f,'html.parser')
                                
        #         tableTag=soup.find("table",class_='resultsTable')
        #         td=tableTag.findAll("tr")
        # table_data=html_data.xpath('//*[@id="resultsTable"]/tbody/tr/td[2]').extract()
        # print(table_data)


                # print(td)


        # TAMIL_INFO=html_data.find("table")
        # for row in TAMIL_INFO.findall('tr'):
        #         col=row.findall('td')
        #         print(col[0])
        # import pdb;pdb.set_trace()
        # break
        # info={"information":}
        # collection.insert_one(info)
        # print(All_Epics_no)
                








        # def mongo_connect(collection_name):
        # connection = MongoClient("mongodb://scraperDev:0mtNHqMELizgmHkp@dev-mongo-db.advarisk.com:27711/?ssl=false")
        # collection = connection['Land_Records'][collection_name]
                # return collection
                # print(captcha_text)
                # import pdb ;pdb.set_trace()        
        
                