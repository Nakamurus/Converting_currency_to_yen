import requests
import lxml.html
import re
import mojimoji
from googletrans import Translator


def fcur(currency, tril=0, bil=0, mil=0, thous=0):
  """
  Convert forreign currency to full_width japanese yen
  """
  
  translator = Translator()
  currency = translator.translate(currency, dest='ja').text # translate to ja
  translated = mojimoji.han_to_zen(currency)
  
  currency = re.sub(r'ドル', ' USD', currency) # replace with currency code
  currency = re.sub(r'ルーブル', ' RUB', currency)
  currency = re.sub(r'元', ' CNY', currency)
  currency = re.sub(r'ポンド', ' GBP', currency)
  currency = re.sub(r'ユーロ', ' EUR', currency) 
  currency = re.sub(r',', '', currency) # get rid of commma
  
  cur_name = currency.split()[-1] # get currency name
  if '兆' in currency: # convert to number, multiplying by powers of 10
    tril = int(re.findall(r'\d{1,4}(?=兆)', currency)[0]) * (10 ** 12)
  if '億' in currency:
    bil = int(re.findall(r'\d{1,4}(?=億)', currency)[0]) * (10 ** 8) 
  if '万' in currency:
    mil = int(re.findall(r'\d{1,4}(?=万)', currency)[0]) * (10 ** 4)
  if '千' in currency:
    thous = int(re.findall(r'\d(?=千)', currency)[0]) * (10 ** 3)
  ammount = tril + bil + mil + thous 
  
  url = 'https://keisanki.me/calculator/index/{}/{}'.format(cur_name, ammount)
  response = requests.get(url)
  content = lxml.html.fromstring(response.content)
  yen = content.xpath('/html/body/section[1]/div/div/div[1]/h1/span/text()')[0]
  date  = content.xpath('/html/body/section[1]/div/div/div[1]/h3/text()')
  # retrieve date to check whether currency data are actuall
  
  table = str.maketrans('','',',') # get rid of comma
  yen = yen.translate(table)
  yen_fullwidth = mojimoji.han_to_zen(yen) # convert to fullwidth
  return translated, yen_fullwidth, date


fcur(input())
