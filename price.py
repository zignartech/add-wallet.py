from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

def price_miota():

  url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
  parameters = {
    'slug':'iota'
  }
  headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '3ac8685e-d018-4421-8ae7-b50f3d26c7f0',
  }

  session = Session()
  session.headers.update(headers)

  try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)['data']['1720']['quote']['USD']['price']
    print(data)
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
  return data