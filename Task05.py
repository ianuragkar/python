FROM = "USD"
TO = "INR"

import datetime
import json
import requests
CURRENCIES = (FROM, TO)

rBTC = requests.get("https://blockchain.info/ticker")
BTCFROM = rBTC.json()[FROM]['last']
BTCTO = rBTC.json()[TO]['last']
viaBTC = (1/BTCFROM)*BTCTO

PAIRS = ["USD" + currency for currency in CURRENCIES]
pairs = ",".join(PAIRS)
rUSD = requests.get("https://www.freeforexapi.com/api/live?pairs=" + pairs)

USDFROM = rUSD.json()['rates']['USD'+FROM]['rate']
USDTO = rUSD.json()['rates']['USD'+TO]['rate']
viaUSD = (1/USDFROM)*USDTO

print("At the time: " + str(datetime.datetime.now().strftime("%d.%m.%Y,%H:%M:%S")))
print("Conversion rate from " + FROM + " to " + TO + "through USD: " + str(viaUSD))
print("Conversion rate from " + FROM + " to " + TO + "through BTC: " + str(viaBTC))
