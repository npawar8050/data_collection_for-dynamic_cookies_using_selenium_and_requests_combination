'''######### Chip1stop_JP_Parser standalone #######'''
import time
import os
import html
from urllib.request import unquote
from lxml import html
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import requests
from chip1stop_parser import Chip1stop_JP_Parser
# from requests.auth import HTTPProxyAuth
# from random import randint
# import json
# import random
# import ssl
# import sys
# import re
# from bs4 import BeautifulSoup
# import sys


class Chipstop_JP(Chip1stop_JP_Parser):

    def __init__(self):
        '''__init__ function'''
        self.current_path = os.path.dirname(os.path.abspath(__file__)) + '/'
        self.s = None
        self.output_file = "Output"
        self.retries = 0
        self.input_url = None
        self.cur_page = None
        self.change_prox = 101
        self.driver = None
        self.total = None
        self.inputs = None
        self.output = []
        self.resume = ''

    i = 0
    def initiate(self):
        '''initiating scraper'''
        try:
            with open(self.current_path + "Input.txt", "r", encoding='utf-8') as f:
                self.inputs = f.readlines()

            global i
            i = 0
            self.total = len(self.inputs)

            try:
                with open(self.current_path + 'Resume.txt', 'r', encoding='utf-8') as f:
                    temp_data = f.readlines()
                self.resume = self.inputs.index(temp_data[0]) + 1
            except Exception as e:
                print(e)
                self.push_data_to_file(
                    "MarketId	comOrderCode	manPartId	manName	EAN_Number	comCurrency	comProductURL	comImageURL	comPromotion	inDateAdded	comStockLoc_1	comStockQty_1	comStockLoc_2	comStockQty_2	comBreak_1	comPrice_1	comBreak_2	comPrice_2	comBreak_3	comPrice_3Other_info1	Other_info2	UOM	Packaging	Order_multiple_quantity	Minimumorderquantity	CountryofOrigin	RoHsCompliance	CustomsTarrifNo	Weightkg	TechnicalDataSheetURL	comCategory_L1	comCategory_L2	comCategory_L3	comCategory_L4	manPartDesc	Specification\n")
                with open(self.current_path + "Resume.txt", "w",encoding='utf-8') as f:
                    pass
                self.resume = 0
            i = self.resume

            for data in self.inputs[self.resume:]:
                if data[0] != "#":
                    line = data.split("\t")
                    Url = line[0].replace('\ufeff', '')
                    if Url.strip() != "":
                        self.input_url = Url.strip().replace('\n', '')
                        self.cur_page = 0
                        self.retries = 0
                        print("\nList_page Url -", self.input_url)
                        # self.s = requests.session()
                        print(f'------------{i}/{len(self.inputs)-self.resume}/{self.total}----------------\n')
                        self.hitting_url(self.input_url, False)
                        self.push_data_to_resume(data)
                    i += 1

        except Exception as e:
            print(e, "Error code 000--- ")
            self.push_data_to_pnf(str(self.input_url) + "\t" + str(e) + "\n")

    def hitting_url(self, url, Main):
        '''Hitting url'''
        time.sleep(3)
        try:
            s = HTMLSession()
            print("---------Hitting Product URL---------------")

            if i % 100 == 0:
                try:
                    service = Service("E:\\chromedriver.exe")
                    chrome_options = webdriver.ChromeOptions()
                    driver = webdriver.Chrome(options=chrome_options, service=service)
                    driver.get(url)
                    driver.maximize_window()
                    wait = WebDriverWait(driver, 10)
                    button_1 = wait.until(
                        EC.presence_of_element_located((By.XPATH, '//*[@class="m-header-language-r"]/dl[2]/dt')))
                    button_1.click()
                    revealed_button_text = 'JPY'
                    button_2 = driver.find_element(By.XPATH, f"//*[text()='{revealed_button_text}']")
                    button_2.click()
                    time.sleep(7)

                    list_of_dict = driver.get_cookies()
                    # print(list_of_dict)
                    new_dict = {d['name']: d['value'] for d in list_of_dict}
                    with open("cookies.txt", 'w', encoding='utf-8') as cookie_file:
                        for key, value in new_dict.items():
                            cookie_file.write(f"{key}: {value}\n")
                            # cookie_file.write(str(new_dict))
                except Exception as e:
                    print("Cookies are not updated", e)
                    self.retries += 1
                    if self.retries < 4:
                        self.change_prox = 101
                        print('Bad Response - Retrying:', self.retries)
                        self.hitting_url(url, False)
                    else:
                        print(
                            "---Failed to Connect after max retries--- \n Error -> {} :----: Exiting with code 001".format(
                                e))
                        self.push_data_to_pnf(self.input_url + "\t" + str(e) + "\n")

            cookies = {}
            with open('cookies.txt', 'r', encoding='utf-8') as file:
                for line in file:
                    key, value = line.strip().split(': ')
                    cookies[key] = value

            headers = {
                'authority': 'www.chip1stop.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'max-age=0',
                'referer': str(url),
                'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            }

            # session = requests.Session()
            resp = s.get(url, headers=headers, cookies=cookies, timeout=60)
            print(resp)

            responseData1 = str(unquote(resp.text).encode('utf-8'))
            time.sleep(3)

            ###############
            tree3 = html.fromstring(responseData1)

            headers = {
                'authority': 'www.chip1stop.com',
                'accept': 'application/xml, text/xml, */*; q=0.01',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'faces-request': 'partial/ajax',
                'origin': 'https://www.chip1stop.com',
                'referer': url,
                'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }
            java = tree3.xpath('//input[@id="j_id1:javax.faces.ViewState:6"]/@value')[0]
            # print("-----java-----", java)

            data = {
                'javax.faces.partial.ajax': 'true',
                'javax.faces.source': 'detailPriceGet',
                'javax.faces.partial.execute': '@all',
                'javax.faces.partial.render': 'detailPrice',
                'detailPriceGet': 'detailPriceGet',
                'searchForm': 'searchForm',
                'j_idt151': '',
                'headerKeywordSearch': '',
                'suggestCategory': '',
                'javax.faces.ViewState': java,
            }

            cookies_new = s.cookies.get_dict()
            cookies_new['CK_010'] = 'Kd91wKeqMBU='
            cookies_new['CK_007'] = 'qLXsBfGNkCo='
            cookies_new['CK_005'] = 'm1OxtZzwqevpU4bRntvjbZNHrST7/LJR05VoKAixt4s='
            cookies_new['CK_009'] = 'YLPXl1Sp5i4='
            cookies_new['CK_002'] = '05VoKAixt4s='
            cookies_new['JSESSIONIDVERSION'] = '2f:110'
            # print(cookies_new)

            resp = requests.post(url, cookies=cookies_new, headers=headers, data=data, timeout=60)
            #############
            PricePage = str(unquote(resp.text).encode('utf-8'))
            print('Price URL response:------------- ', resp.status_code)

            if resp.status_code == 200:
                htmldata = responseData1 + PricePage

                self.push_data_to_html(htmldata)
                super().__init__(htmldata)
                self.parser(htmldata)
            else:
                self.push_data_to_pnf(str(url) + "\n")

        except Exception as e:
            print(e)
            self.retries += 1
            if self.retries < 4:
                self.change_prox = 101
                print('Bad Response - Retrying:', self.retries)
                self.hitting_url(url, False)
            else:
                print(f"---Failed to Connect after max retries--- \n Error -> {e}")
                self.push_data_to_pnf(self.input_url + "\t" + str(e) + "\n")

    def parser(self,htmldata):
        '''Parsing the data'''
        print('Parsing data from the source page ')
        out_list = []

        marketid = a.marketid().replace('\t', '').replace('\n', '').strip()
        comordercode = a.comordercode().replace('\t', '').replace('\n', '').strip()
        print('COC : ', comordercode)
        manName = a.manName().replace('\t', '').replace('\n', '').strip()

        out_list.append(marketid)
        out_list.append(comordercode)
        out_list.append(manName)

        out_list = '\t'.join(out_list) + '\n'
        self.push_data_to_file(out_list)
        self.push_data_to_log(self.input_url)
        print('Data successfully inserted')

    def push_data_to_file(self, data):
        '''Writes data to the output'''
        with open(self.current_path + self.output_file + ".txt", "a", encoding='utf-8') as f:
            f.write(data)

    def push_data_to_pnf(self, data):
        '''Adds urls to PNF folder if there is issue with response with data'''
        with open(self.current_path + "PNF.txt", "a", encoding='utf-8') as f:
            f.write(data)

    def push_data_to_log(self, data):
        '''Adds log file'''
        with open(self.current_path + "log.txt", "w", encoding='utf-8') as f:
            f.write(data)

    def push_data_to_html(self, data):
        '''Adds data to html page for reference'''
        with open(self.current_path + "Cache.html", "w", encoding='utf-8') as f:
            f.write(data)

    def push_data_to_resume(self, data):
        '''Adds current url to resume folder so as to resume crawl from any point'''
        with open(self.current_path + "resume.txt", "w", encoding='utf-8') as f:
            f.write(data)


if __name__ == "__main__":
    a = Chipstop_JP()
    a.initiate()
