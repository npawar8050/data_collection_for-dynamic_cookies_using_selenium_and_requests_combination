from datetime import datetime
import os
import urllib3, ssl
import random
from codecs import escape_decode
import re, string
import sys
import requests
import json
import math
from lxml import html


class Chip1stop_JP_Parser:
    htmlElementNew = ''
    tempPage = ''

    def __init__(self, htmlElements):
        htmlElements = escape_decode(htmlElements)[0].decode('utf-8')
        self.html_Element = html.document_fromstring(htmlElements)

    def check_Rubbish(self, input):
        input = input.replace('\\xc2\\xa1', '¡')
        input = input.replace('\\n', '')
        input = input.replace('\\r', '')
        input = input.replace('\\t', '')
        input = input.replace('\\xc2\\xa2', '¢')
        input = input.replace('\\xc2\\xa3', '£')
        return input


    def marketid(self):
        '''add country code'''
        return 'JP'

    def comordercode(self):  # Completed
        '''add coc'''
        try:
            result = self.html_Element.xpath(
                '//li[@class="m-mr-1em"]/text()|//li[@class="m-mr-1em"]/p[@class="js-clickableCopy"]/text()')
        except Exception as e:
            print(e)
            result = ''

        if not result:
            comOrderCode = ''
        else:
            comOrderCode = result[0].strip()
        comordercode = self.check_Rubbish(comOrderCode)
        return comordercode

    def manName(self):
        '''add brand name'''
        try:
            result = self.html_Element.xpath('(//ul[@class="m-text-16"]//a/text())[1]')
        except Exception as e:
            print(e)
            result = ''

        if not result:
            manName = ''
        else:
            manName = result[0].strip()
            manName = self.check_Rubbish(manName)
        return manName
        
    def prices(self):
        '''price data'''
        try:
            pass
            '''
            To get the prices from the URL you provided, you can use the `requests` library to send a GET request to the URL and then parse the JSON response to extract the prices. Here's an example of how you could do this:
            ```python
            import requests
            import json
            from bs4 import BeautifulSoup

            url = 'https://www.chip1stop.com/JPN/en/view/dispDetail/DispDetail?partId=IFNO-0104540&mpn=BCR602XTSA1'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the prices from the JSON response
            json_data = json.loads(soup.find('script', {'type': 'application/ld+json'}).getText())
            prices = []
            for item in json_data['offers']:
                if item['priceCurrency'] == 'JPY':
                    prices.append({
                        'name': item['itemOffered']['name'],
                        'price': float(item['price']) / 100,
                        'salesPrice': float(item['price']) / 100,
                    })
            print(prices)
            ```
            The `requests` library is used to send a GET request to the URL and retrieve the HTML response. The `BeautifulSoup` library is then used to parse the HTML response and extract the JSON response.

            The `json_data = json.loads()` method loads the JSON data from the script element with the type attribute set to `'application/ld+json'`. This element contains the prices of the product, so we can use the `prices` variable to store the extracted prices.

            The `for item in json_data['offers']:` loop iterates over the offers in the JSON response and extracts the price for each offer that has a price currency of 'JPY'. The price is then stored in the `prices` list, along with the name of the product.

            Finally, the `print(prices)` statement prints out the extracted prices.'''
        except:
            pass