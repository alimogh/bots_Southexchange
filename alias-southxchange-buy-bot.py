#!/usr/bin/env python3

import hmac
import hashlib
import json
import time
import requests

# constants
key = "yourkeyhere"
secret = b'yoursecrethere'
amount = 1
waitTime = 60 # time between each trade, in seconds

while True:
	# setup API call:
	call = {
		"key": key,
		"nonce": int(time.time()),
		"listingCurrency": "ALIAS",
		"referenceCurrency": "BTC",
		"type": "buy",
		"amount": amount,
	}

	# convert to JSON & encode as UTF-8
	m = json.dumps(call).encode('utf-8')

	# calculate signature
	s = hmac.new(secret, msg=m, digestmod=hashlib.sha512).hexdigest()

	# make HTTP request
	url = 'https://www.southxchange.com/api/placeOrder'
	header = {'Hash': s}
	x = requests.post(url, json=call, headers=header)

	# print result
	if x.status_code != 200:
		break
	else:
		print(x.text)
	
	time.sleep(waitTime)

sys.exit("Request rejected by SouthXchange")
