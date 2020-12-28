#!/usr/bin/python3

import requests

URL = 'https://poe.ninja/api/data/CurrencyOverview?league=Flashback%20(DRE007)&type=Currency&language=en'
req = requests.get(URL)


lines = req.json()['lines']

for line in lines:
	# print(line['currencyTypeName'], "=", line['chaosEquivalent'], "chaos")
	if ("Alteration" not in line['currencyTypeName']):
		continue


	print(line['pay'])
	print('=========================')
	print(line['receive'])