from flask import Flask, request,jsonify
from flask_cors import CORS,cross_origin
import requests
import os
from module import CryptoScrapDriver

scrap_driver = CryptoScrapDriver()


app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def get_all_crypto_datas():

  return { "data": scrap_driver.get_all_price_by_exchange("ZIPMEX") }

@app.route('/arb/<ticker>', methods=['GET'])
def arbitrage(ticker):
  print(f'Ticker: {ticker}')

  return f"<h2>{ticker}</h2>"


# @app.route('/currency/map', methods=['GET'],)
# def currency_map():
#   symbol = request.args.get('symbol')
#   r = requests.get(f'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info?symbol={symbol}', headers={ 
#       "X-CMC_PRO_API_KEY": os.environ.get('CMC_API_KEY') 
#     })
#   print(r.json())
#   return r.json()

@app.route('/support_currencies', methods=['GET'],)
def support_currencies():
  req_symbols = ','.join(scrap_driver.get_all_support_symbols())
  req_symbols = req_symbols.replace('JFIN','JFC')
  req_symbols = req_symbols.replace('XZC','FIRO')
  
  res_cmc = requests.get(f'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info?symbol={req_symbols}', headers={ 
      # "X-CMC_PRO_API_KEY": os.environ.get('CMC_API_KEY') 
      "X-CMC_PRO_API_KEY": "f81e1b32-3b77-41dc-b680-40b780698f63"

  })

  res = []
  for symbol in res_cmc.json()['data'].keys():
    res.append({"symbol":symbol,"logo":res_cmc.json()['data'][symbol][0]['logo']})

  return {"data":res}

# @app.route('/get_all_cryptos', methods=['GET'],)
# def get_all_cryptos():
#   req_crypto_datas = scrap_driver.get_all_crypto_datas()

#   return {"data":req_crypto_datas}

@app.route('/arbitrage', methods=['GET'])
def get_all_crypto_data():

  return jsonify(scrap_driver.get_all_crypto_datas())

if __name__ == '__main__':
  app.run(port=5000, debug=True)