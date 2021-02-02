#!/usr/bin/env python3

import hmac
import hashlib
import json
import time
import requests
import sys

# To get valid keys:
#   1. Go to https://main.southxchange.com/Account/Manage
#   2. Click on Private API keys
#   3. Create a key with only the first permission (place order)
key = "yourkeyhere"
secret = "yoursecrethere"

# Change these constants to customize the bot!
ticker = "ALIAS" # currency to trade
action = "buy" # buy or sell
amount = 0.25 # amount of coins to buy/sell in each trade
waitTime = 60 # time between trades, in seconds

# Main loop
netErrors = 0
statusErrors = 0
while True:
	# setup API call:
	call = {
		"key": key,
		"nonce": int(time.time()),
		"listingCurrency": ticker,
		"referenceCurrency": "BTC",
		"type": action,
		"amount": amount,
	}

	# convert to JSON & encode as UTF-8
	m = json.dumps(call).encode('utf-8')

	# calculate signature
	s = hmac.new(bytes(secret, 'utf-8') , msg=m, digestmod=hashlib.sha512).hexdigest()

	# make HTTP request
	url = 'https://www.southxchange.com/api/placeOrder'
	header = {'Hash': s}
	try:
		x = requests.post(url, json=call, headers=header)
		if x.status_code == 200:
			print(x.text)
			netErrors = 0
			statusErrors = 0
		else:
			print("Warning: HTTP status ", x.status_code)
			statusErrors += 1
	except requests.exceptions.ConnectionError:
		print("Connection error")
		netErrors += 1

	# Give up after 10 failed attempts
	if statusErrors == 10:
		break

	# slow down if we are getting errors continuously
	time.sleep(waitTime + 60 * netErrors)

sys.exit("Request rejected by SouthXchange")
