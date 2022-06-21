# -----------------------------------------------------------------------------------------------------------
#                     Tamilnadu voter_List information based on Epic_number
#-----------------------------------------------------------------------------------------------------------
#   Execution sample commond:
#                     >>>   python info.py
#        
#   [Created on 21-June-2022 by Minakshi Dhangare]
#-----------------------------------------------------------------------------------------------------------


import json
import os
from os import getcwd

import requests
from bs4 import BeautifulSoup
from lxml.html import fromstring
from PIL import Image
from pymongo import MongoClient
from scrapy import FormRequest, Request
from selenium import webdriver
from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha
from webdriver_manager.chrome import ChromeDriverManager

driver=webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
driver.get("https://electoralsearch.in/##resultArea")
driver.implicitly_wait(10)
driver.find_elements(By.XPATH,'//*[@id="continue"]')[0].click()
driver.find_elements(By.XPATH,'//*[@id="mainContent"]/div[2]/div/div/ul/li[2]')[0].click()
driver.find_elements(By.XPATH,'//*[@id="name"]')[0].click()
connection = MongoClient("mongodb://scraperDev:0mtNHqMELizgmHkp@dev-mongo-db.advarisk.com:27711/?ssl=false")
collection = connection['Land_Records']['TamilNadu_Epic_No']


mydb=connection['Land_Records']['Voter_list_information']
epic_nos=collection.find()
for epic_no in epic_nos[:11]:
        epic_box=driver.find_element_by_xpath('//*[@id="name"]')
        epic_box.send_keys(u'\ue009' + u'\ue003')   # clt+backspace to clear the epic_no
        driver.find_element(By.XPATH,'//*[@id="name"]').send_keys(epic_no['epics_no'])
        Key_=TwoCaptcha('a0422b85d3ebe3b06bd34545dceb528e')
        cap=driver.find_element_by_xpath('//*[@id="captchaEpicImg"]')
        cap.screenshot("tamil_captcha.png")
        captcha_text=Key_.normal(getcwd()+'/tamil_captcha.png',caseSensitive=1)
        html_data=driver.page_source
        cookies = driver.get_cookies()
        id_=driver.session_id
        cookies_ =  {
        "Electoral": cookies[3]['value'],
        "cookiesession1": cookies[2]['value'],
        "__RequestVerificationToken": cookies[4]['value'],
        "runOnce": "true",
        "electoralSearchId": cookies[0]['value']}
        url_ = 'https://electoralsearch.in/Home/searchVoter?epic_no={}&page_no=1&results_per_page=10&reureureired={}&search_type=epic&txtCaptcha={}'.format(epic_no['epics_no'], id_,captcha_text['code'])
        data=requests.get(url_,cookies=cookies_, verify=False)
        if data.status_code == 200:
                y = json.loads(data.text)
                final_details = {
                'epic_no':epic_no['epics_no'],
                'name':y['response']['docs'][0]['name'],
                'name_in_regional':y['response']['docs'][0]['name_v1'],
                'age':y['response']['docs'][0]['age'],
                'relative_name':y['response']['docs'][0]['rln_name'],
                'relative_name_in_regional':y['response']['docs'][0]['rln_name_v1'],
                'state':y['response']['docs'][0]['st_name'],
                'district':y['response']['docs'][0]['dist_name'],
                'polling_station':y['response']['docs'][0]['ps_name'],
                'assembly_constituency':y['response']['docs'][0]['ac_name'],
                'parliament_constituency':y['response']['docs'][0]['pc_name'] }
                voter_list=mydb.insert_one(final_details)
driver.close()
