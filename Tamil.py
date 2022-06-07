from scrapy import Request, FormRequest
from uuid import uuid4
import csv
import scrapy
import pytesseract
from PIL import Image
from pytesseract import image_to_string
import io
from twocaptcha import TwoCaptcha
import urllib3
from urllib.parse import urlencode
import sys
from pdf2image import convert_from_path
import os
import re
import pymongo 
from playwright.sync_api import sync_playwright 
from pymongo import MongoClient    
                
connection=pymongo.MongoClient('mongodb://scraperDev:0mtNHqMELizgmHkp@dev-mongo-db.advarisk.com:27711/?ssl=false')
mydb=connection['Land_Records']['TamilNadu_Epic_No']

class colony_data(scrapy.Spider):
    name="TamilNadu"
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    def start_requests(self):
        yield Request('https://www.elections.tn.gov.in/Rollpdf/SSR2021_20012021.aspx',
            meta={'cookiejar':str(uuid4)},
            callback=self.parse) 

    def parse(self,response):
        data=response.xpath('//*[@id="ddl_District"]/option/@value')[1:].extract()
        for District_no in data:
            yield FormRequest.from_response(response,'https://www.elections.tn.gov.in/Rollpdf/SSR2021_20012021.aspx',
                formdata = {
                    '__EVENTTARGET': 'ddl_District',
                    '__EVENTARGUMENT': '',
                    '__LASTFOCUS':'' ,
                    '__VIEWSTATEGENERATOR': 'EF53B686',
                    'ddl_District': District_no},
                    meta={'cookiejar':str(uuid4),'dist':District_no},
                    callback=self.next_data)
            # break

    def next_data(self,response):
        dist_no = response.meta['dist']
        Assembly= response.xpath('//*[@id="ddl_Assembly"]/option/@value')[1:].extract()
        for Assembly_no in Assembly:
            yield FormRequest.from_response(response,'https://www.elections.tn.gov.in/Rollpdf/SSR2021_20012021.aspx',
            formdata={
                '_EVENTTARGET':"" ,
                '__EVENTARGUMENT':"", 
                '__LASTFOCUS': "",
                'ddl_District': dist_no,
                'ddl_Assembly': Assembly_no,
                'btn_Login': 'சமர்ப்பிக்க'},
                meta={'cookiejar':str(uuid4)},
                callback=self.pages_data)
            # break
  
    def pages_data(self,response):
        link=response.xpath('//*[@id="form1"]/table//tr/td[2]/p/a/@href').extract()[1:]
        for b in link:
            # print(b)
            yield Request(b,
            meta={'cookiejar':str(uuid4),'url_no':b},
            callback=self.captcha_reader)
            break

    def captcha_reader(self,response):
        url_ = response.meta['url_no']
        img = response.xpath('//*[@id="Image2"]/@src').extract()
        yield Request('https://www.elections.tn.gov.in/rollpdf/{}'.format(img[0]),
        meta={'cookiejar':str(uuid4),'url_':url_},
        callback=self.captcha_resp)

    def captcha_resp(self,response): 
        url = response.meta['url_']   
        # print('++++++++++++',response.meta['url_'])
        with open("tamil.jpeg", "wb") as imageFile:
            imageFile.write (response.body)
        api_key = 'a0422b85d3ebe3b06bd34545dceb528e'
        # this is api_key for captcha
        solve = TwoCaptcha(api_key)
        result = solve.normal("/home/minakshi/Desktop/Advarisk Task5/TamilNadu/data/tamil.jpeg",caseSensitive=1)
        # print("yes")
        body = {'__EVENTTARGET':'',
                '__EVENTARGUMENT':'',
                'txt_Vcode': result["code"],
                'btn_Login': 'சமர்ப்பிக்க'}
        x=yield Request(url,
            method='POST',
            body=urlencode(body),
            meta={'cookiejar':str(uuid4),'url':url},
            callback=self.captcha_solved)

    def captcha_solved(self,response):
        # cookies=
    
        # import pdb;pdb.set_trace()
        for cat in ['ac029']:
            for doc_no in range(20,100):
                pdf_url = f'https://www.elections.tn.gov.in/SSR2021_20012021/dt3/{cat}/{cat}{str(doc_no).zfill(3)}.pdf'
                yield Request(pdf_url,
                meta={'cookiejar':str(uuid4), 'filename':f'{cat}{str(doc_no).zfill(3)}'},
                callback=self.result)

    def result(self,response):
        # import pdb; pdb.set_trace()
        with open(response.meta['filename'], 'wb') as _f:
            _f.write(response.body)
        list_ = ['ac0290']
        EPIC_NO_all=[]
        for c_ in list_:
            for files_no in range(70,100):
                PDF_file = f"/home/minakshi/Desktop/Advarisk Task5/TamilNadu/TamilNadu/{c_}{files_no}"
                pages = convert_from_path(PDF_file, 150)
                image_counter = 1
                for page in pages:
                    filename = "page_"+str(image_counter)+".jpg"
                    page.save(filename, 'JPEG')
                    image_counter = image_counter + 1
                # Variable to get count of total number of pages
                filelimit = image_counter-1
                # Creating a text file to write the output
                outfile = "out_text.txt"
                f = open(outfile, "a")
                # Iterate from 1 to total number of pages
                for i in range(3, filelimit):
                    # for j in range(1,len(filelimit)):
                    # import pdb;pdb.set_trace()
                    filename = "page_"+str(i)+".jpg"
                    text = str(((pytesseract.image_to_string(Image.open(filename)))))
                    EPIC_NO = re.findall("[A-Z]{3}[0-9]{7}",text)
                    # for j in range(len(EPIC_NO)):

                    # EPIC.append(EPIC_NO)
                        # print(EPIC_NO[j])
                    text = text.replace('-\n', '')	
                    f.write(text)
                    # EPIC_NO_all.append(EPIC_NO)  
                    # Numbers={"Epic_No":EPIC_NO_all}
                    for j in range(len(EPIC_NO)):
                        # import pdb;pdb.set_trace()
                        epic_no={"epics_no":EPIC_NO[j]}
                        All_Epics_no=mydb.insert_one(epic_no)
                        print(All_Epics_no)
                

    # def mongo_connect(collection_name):
    #     connection = MongoClient("mongodb://scraperStage:DkTj7TPMBp0oiEQL@dev-mongo-db.advarisk.com:27712/?ssl=false")
    #     collection = connection['Land_Records']['TamilNadu_Epic_No']
    #     for j in range(len(EPIC_NO)):
    #         collection.insert_one(Epic_No[j])
    #         return collection    

            #     EPIC_NO_all.append(EPIC_NO)  
            # Numbers={"Epic_No":EPIC_NO_all}
            # All_Epics_no=mydb.insert_one(Numbers)
                
