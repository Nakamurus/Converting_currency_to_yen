import requests
import lxml.html
import re
import mojimoji


def fcur(mon, tril=0, bil=0, mil=0, thous=0):
  mon = re.sub(r'ドル', ' USD', mon)
  mon = re.sub(r'ルーブル', ' RUB', mon)
  mon = re.sub(r'元', ' CNY', mon)
  mon = re.sub(r'ポンド', ' GBP', mon)
  mon = re.sub(r'ユーロ', ' EUR', mon)
  cur = mon.split()[-1]
  if '兆' in mon:
    tril = int(re.findall(r'\d{1,4}(?=兆)', mon)[0]) * (10 ** 12)
  if '億' in mon:
    bil = int(re.findall(r'\d{1,4}(?=億)', mon)[0]) * (10 ** 8) 
  if '万' in mon:
    mil = int(re.findall(r'\d{1,4}(?=万)', mon)[0]) * (10 ** 4)
  if '千' in mon:
    thous = int(re.findall(r'\d(?=千)', mon)[0]) * (10 ** 3)
    print(int(re.findall(r'\d{1,4}(?=千)', mon)[0]))
  num = tril + bil + mil + thous
  
  url = 'https://keisanki.me/calculator/index/{}/{}'.format(cur, num)
  response = requests.get(url)
  text = lxml.html.fromstring(response.content)
  currency = text.xpath('/html/body/section[1]/div/div/div[1]/h1/span/text()')[0]
  
  table = str.maketrans('','',',')
  currency = currency.translate(table)
  currency = mojimoji.han_to_zen(currency)
  return currency