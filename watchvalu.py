#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib3
import urllib
import json

VALU_KEYWORD = u''
VALU_TOKEN = ''
VALU_COOKIE = ''

SLACK_WEBHOOK_URL = ''
SLACK_CHANNEL = ''

if __name__ == "__main__":
  valu_url = 'https://valu.is/search'
  valu_headers = {
    'Pragma': 'no-cache', 
    'Origin': 'https://valu.is', 
    'Accept-Encoding': 'gzip, deflate, br', 
    'Accept-Language': 'ja,en-US;q=0.8,en;q=0.6', 
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36', 
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 
    'Accept': '*/*', 
    'Cache-Control': 'no-cache', 
    'X-Requested-With': 'XMLHttpRequest', 
    'Cookie': VALU_COOKIE, 
    'Connection': 'keep-alive', 
    'Referer': 'https://valu.is/?search_box=%s' % VALU_KEYWORD, 
    'DNT': '1', 
  }
  valu_body = 'keyword=%s&_token=%s' %(VALU_KEYWORD, VALU_TOKEN)

  http = urllib3.PoolManager()
  r = http.request(
    'POST', 
    valu_url, 
    headers=valu_headers, 
    body=valu_body
  )
  response_headers = r.headers

  if 'Content-Type' in response_headers and response_headers['Content-Type'] != 'text/html; charset=UTF-8':
    result = r.data
    if result and result != b'[]':
      slack_url = SLACK_WEBHOOK_URL
      slack_headers = {'Content-Type': 'application/json'}
      text = '''
Content-Type: %s
keyword: %s
result: %s
'''
      slack_body = json.dumps({
          "text": text % (response_headers['Content-Type'], urllib.parse.unquote(VALU_KEYWORD), result), 
          "username": "webhookbot", 
          "channel": SLACK_CHANNEL, 
          "icon_emoji": ":ghost:",
        })

      http = urllib3.PoolManager()
      r = http.request(
        'POST', 
        slack_url, 
    		headers=slack_headers,
    		body=slack_body)

      r.read()

