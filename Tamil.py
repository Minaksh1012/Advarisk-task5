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
# from files.utils import get_cookies
# from direct import ScrapeAspx
import sys
from pdf2image import convert_from_path
import os
import re

# pip install 2captcha-python

class colony_data(scrapy.Spider):
    name="TamilNadu"
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    def start_requests(self):
        yield Request('https://www.elections.tn.gov.in/Rollpdf/SSR2021_20012021.aspx',
            meta={'cookiejar':str(uuid4)},
            callback=self.parse) 

    def parse(self,response):
        # import pdb;pdb.set_trace()
        data=response.xpath('//*[@id="ddl_District"]/option/@value')[1:].extract()
        # print(data,"+++++++++++++++++++/++++++++")
        for District_no in data:
            # import pdb;pdb.set_trace()
            # print(District_no,'***************************************************************')
            yield FormRequest.from_response(response,'https://www.elections.tn.gov.in/Rollpdf/SSR2021_20012021.aspx',
                formdata = {
                    '__EVENTTARGET': 'ddl_District',
                    '__EVENTARGUMENT': '',
                    '__LASTFOCUS':'' ,
                    '__VIEWSTATEGENERATOR': 'EF53B686',
                    'ddl_District': District_no},
                    meta={'cookiejar':str(uuid4),'dist':District_no},
                    callback=self.next_data)
            break

    def next_data(self,response):
        # import pdb;pdb.set_trace()
        dist_no = response.meta['dist']
        Assembly= response.xpath('//*[@id="ddl_Assembly"]/option/@value')[1:].extract()
        print(Assembly)
        for Assembly_no in Assembly:
            # print(Assembly_no,">>>>>>>>>>>>>>>>>>>>")
            print(dist_no,Assembly_no)
            yield FormRequest.from_response(response,'https://www.elections.tn.gov.in/Rollpdf/SSR2021_20012021.aspx',
            # print(dist_no,Assembly_no)              https://www.elections.tn.gov.in/Rollpdf/SSR2021_20012021.aspx
            #                                         https://www.elections.tn.gov.in/Rollpdf/SSR2021_20012021.aspx
            formdata={
                '_EVENTTARGET':"" ,
                '__EVENTARGUMENT':"", 
                '__LASTFOCUS': "",
                'ddl_District': dist_no,
                'ddl_Assembly': Assembly_no,
                'btn_Login': 'சமர்ப்பிக்க'},
                meta={'cookiejar':str(uuid4)},
                callback=self.pages_data)
            break
  
    def pages_data(self,response):
        # import pdb;pdb.set_trace()
        link=response.xpath('//*[@id="form1"]/table//tr/td[2]/p/a/@href').extract()[1:]
        # print(link,"MMMMMMMMMMMMMMMMMM")
        for b in link:
            print(b)
            yield Request(b,
            meta={'cookiejar':str(uuid4),'url_no':b},
            callback=self.captcha_reader)
            break

    def captcha_reader(self,response):
        # import pdb;pdb.set_trace()
        url_ = response.meta['url_no']
        img = response.xpath('//*[@id="Image2"]/@src').extract()
        print(img)
        # import pdb;pdb.set_trace()
        yield Request('https://www.elections.tn.gov.in/rollpdf/{}'.format(img[0]),
        meta={'cookiejar':str(uuid4),'url_':url_},
        callback=self.captcha_resp)
# action="./Captcha2.aspx?dt=dt16&ac=ac140&pt=ac140001"
# https://www.elections.tn.gov.in/SSR2021_20012021/dt16/ac140/ac140001.pdf

    def captcha_resp(self,response): 
        # import pdb;pdb.set_trace()
        # cookies = get_cookies(response.request,cookie_key='cookies')
        url = response.meta['url_']   
        print('++++++++++++',response.meta['url_'])
        with open("tamil.jpeg", "wb") as imageFile:
            imageFile.write (response.body)
        api_key = 'a0422b85d3ebe3b06bd34545dceb528e'
        # this is api_key for captcha
        solve = TwoCaptcha(api_key)
        result = solve.normal("/home/minakshi/Desktop/Advarisk Task5/TamilNadu/data/tamil.jpeg",caseSensitive=1)
        print("yes")
        body = {'__EVENTTARGET':'',
                '__EVENTARGUMENT':'',
                'txt_Vcode': result["code"],
                'btn_Login': 'சமர்ப்பிக்க'}
        x=yield Request(url,
            method='POST',
            body=urlencode(body),
            meta={'cookiejar':str(uuid4),'url':url},
            callback=self.captcha_solved)
        # c=x.cookies
        # print("?????????????????????",c)

    def captcha_solved(self,response):
        # cookies=
    
        # import pdb;pdb.set_trace()
        for cat in ['ac029', 'ac014']:
            for doc_no in range(1,10):
                pdf_url = f'https://www.elections.tn.gov.in/SSR2021_20012021/dt3/{cat}/{cat}{str(doc_no).zfill(3)}.pdf'
                print(pdf_url,"\\\\\\\\\\\\\\\\\\\\\\")
        # img = response.meta['img']
                yield Request(pdf_url,
                meta={'cookiejar':str(uuid4), 'filename':f'{cat}{str(doc_no).zfill(3)}'},
                callback=self.result)
            # break
    def result(self,response):
        # import pdb; pdb.set_trace()
        with open(response.meta['filename'], 'wb') as _f:
            _f.write(response.body)
        # import pdb;pdb.set_trace()
        # print("captcha found")   
        for c in['ac029','ac014']:
            for files_no in range(1,10) :
                PDF_file = "/home/minakshi/Desktop/Advarisk Task5/TamilNadu/TamilNadu/ac029001"
        
        '''
        Part #1 : Converting PDF to images
        '''
        # import pdb;pdb.set_trace()
        # Store all the pages of the PDF in a variable
        pages = convert_from_path(PDF_file, 150)

        # Counter to store images of each page of PDF to image
        image_counter = 1

        # Iterate through all the pages stored above
        for page in pages:
            filename = "page_"+str(image_counter)+".jpg"
                
                # Save the image of the page in system
            page.save(filename, 'JPEG')

                # Increment the counter to update filename
            image_counter = image_counter + 1

        '''
        Part #2 - Recognizing text from the images using OCR
        '''
        # Variable to get count of total number of pages
        filelimit = image_counter-1

        # Creating a text file to write the output
        outfile = "out_text.txt"
        f = open(outfile, "a")

        # Iterate from 1 to total number of pages
        for i in range(1, 100):
            # import pdb;pdb.set_trace()
            filename = "page_"+str(i)+".jpg"
            text = str(((pytesseract.image_to_string(Image.open(filename)))))
            EPIC_NO = re.findall("[A-Z]{3}[0-9]{7}",text)
            # EPIC.append(EPIC_NO)
            print(EPIC_NO)
            text = text.replace('-\n', '')	

            # Finally, write the processed text to the file.
            f.write(text)

        # Close the file after writing all the text.
        # f.close()


        # https://www.elections.tn.gov.in/rollpdf/Captcha2.aspx?dt=dt1&ac=ac001&pt=ac001002
        # https://www.elections.tn.gov.in/SSR2021_20012021/dt3/ac029/ac029005.pdf

# for cat in ['ac029', 'ac014']:
#     for doc_no in range(0,100):
#         url = f'https://www.elections.tn.gov.in/SSR2021_20012021/dt3/{cat}/{cat}{doc_no.zfill(3)}.pdf'
# {cat}{doc_no.zfill(3)}