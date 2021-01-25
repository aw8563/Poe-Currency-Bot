#!/usr/bin/python3

import json
import subprocess

from Models.Item import Item, ItemType

SESS_ID = "171a88b7cfdf0d09d50666729a4d559f"
CHARACTER = "kwoktopus"
LEAGUE = "Ritual"

itemMap = {}
for enum in ItemType:
    itemMap[enum] = set()


for tab in (7,8,9,10,11):

    url = "https://www.pathofexile.com/character-window/get-stash-items?accountName=%s&realm=pc&league=%s&tabs=0&tabIndex=%d" \
        %(CHARACTER, LEAGUE, tab)

    commands = [
        'curl',
        '--cookie',
        "POESESSID=" + SESS_ID,
        url
    ]

    response = subprocess.check_output(commands)

    items = json.loads(response)['items']

    for i in items:
        try:
            item = Item(i)
            itemMap[item.type].add(item)
        except:
            print("error")
            pass # just skip unparsable garbage


for key,value in itemMap.items():
    print(key, len(value))
