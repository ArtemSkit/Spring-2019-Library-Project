#!/usr/bin/python3
################################################################################
# Program    : crawler.py
# Author     : Artem Skitenko, Harry Staley and David Velez
# Date       : 05/12/2019
# Description: Web Crawling through CivTech Site
################################################################################

# Imports
import requests
from bs4 import BeautifulSoup
from flask import Flask, make_response, jsonify
import json


###############################################################################
# Author and Version
###############################################################################
__author__ = "Artem Skitenko <artemskitenko93@gmail.com>, Harry Staley <staleyh@gmail.com> and David Velez <dveleztx@gmail.com>"
__version__ = "1.1"


###############################################################################
# Requests and Sessions
###############################################################################
app = Flask(__name__)

# GET Requests to San Antonio Public Library
req = requests.get('https://sapl.sat.lib.tx.us/patroninfo', headers={
        'Host': 'sapl.sat.lib.tx.us',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/'
                      '537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/'
                  'webp,image/apng,/;q=0.8,application/signed-exchange;v=b3',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    })

# Session ID
session_id = req.cookies.get(name='III_SESSION_ID')
#    print(session_id) # DEBUGGING PURPOSES


# POST Requests to San Antonio Public Library with Authentication
req = requests.post('https://sapl.sat.lib.tx.us/patroninfo',
                    headers={
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/'
                                  'webp,image/apng,/;q=0.8,application/signed-exchange;v=b3',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Cache-Control': 'max-age=0',
                        'Connection': 'keep-alive',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Cookie': 'SESSION_LANGUAGE=eng; SESSION_SCOPE=1; III_EXPT_FILE='
                                  'aa15476; III_SESSION_ID=' + session_id,
                        'Host': 'sapl.sat.lib.tx.us',
                        'Origin': 'https://sapl.sat.lib.tx.us/',
                        'Referer': 'https://sapl.sat.lib.tx.us/patroninfo',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                                      '537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
                    },
                    data={'code': 'SECRET',
                          'pin': 'SECRET',
                          'pat_submit': 'xxx'})
url_base = req.url[:-5]

###############################################################################
# Routes for Holds and Items Checked Out
###############################################################################
@app.route('/holds')
def holds():
    try:
        response = jsonify(Data=crawl_holds())
        return make_response(response, 201)
    except Exception as e:
        print(e)
        response = {'status': "Failed", 'reason': e}
        return make_response(json.dumps(response), 405)


@app.route('/items')
def items():
    try:
        response = jsonify(Data=crawl_items())
        return make_response(response, 201)
    except Exception as e:
        print(e)
        response = {'status': "Failed", 'reason': e}
        return make_response(json.dumps(response), 405)

###############################################################################
# Crawling through San Antonio Public Library to Retrieve Data
###############################################################################
def crawl_holds():
    req = requests.get(url_base + 'holds',
                       headers={
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/'
                                  ';q=0.8,application/signed-exchange;v=b3',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Cache-Control': 'max-age=0',
                        'Connection': 'keep-alive',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Cookie': 'SESSION_LANGUAGE=eng; SESSION_SCOPE=1; III_EXPT_FILE=aa15476; III_SESSION_ID='
                                  + session_id,
                        'Host': 'sapl.sat.lib.tx.us',
                        'Origin': 'https://sapl.sat.lib.tx.us/',
                        'Referer': 'https://sapl.sat.lib.tx.us/patroninfo',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                      ' Chrome/74.0.3729.131 Safari/537.36'
                       })
#    with(open('page.html', 'w')) as target:
#        target.write(x.text)
    soup = BeautifulSoup(req.text, "html.parser")
    rows = soup.findAll('tr', class_="patFuncEntry")
    data = []
    for row in rows:
        title = row.find('td', class_='patFuncTitle').find('a').text
        hold = {'title' : title[:title.find(' / ')],
                'status' : row.find('td', class_='patFuncStatus').text}
        data.append(hold)
    print(data)
    return data

def crawl_items():
    req = requests.get(url_base + 'items',
                       headers={
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/'
                                          'apng,*/*;q=0.8,application/signed-exchange;v=b3',
                                'Accept-Encoding': 'gzip, deflate, br',
                                'Accept-Language': 'en-US,en;q=0.9',
                                'Connection': 'keep-alive',
                                'Content-Type': 'application/x-www-form-urlencoded',
                                'Cookie': 'SESSION_LANGUAGE=eng; SESSION_SCOPE=1; III_EXPT_FILE=aa15476; '
                                          'III_SESSION_ID=' + session_id,
                                'Host': 'sapl.sat.lib.tx.us',
                                'Referer': 'https://sapl.sat.lib.tx.us/patroninfo',
                                'Upgrade-Insecure-Requests': '1',
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                              'like Gecko) Chrome/74.0.3729.131 Safari/537.36'
                                })
    soup = BeautifulSoup(req.text, "html.parser")
    rows = soup.findAll('tr', class_="patFuncEntry")
    data = []
    for row in rows:
        title1 = row.find('td', class_='patFuncTitle').find('a').text
        status1 = row.find('td', class_='patFuncStatus').text
        hold = {'title': title1[:title1.find(' / ')],
                'status': status1[:status1.find('\n')].strip()}
        data.append(hold)
    print(data)
    return data

###############################################################################
# Print the Header
###############################################################################
def header():
    print("---------------------")
    print("   Web Crawler App")
    print("---------------------")
    print()


###############################################################################
# Invoke Main
###############################################################################
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

