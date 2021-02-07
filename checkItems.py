#!/usr/bin/python3

from Utils.apiUtils import queryItemsFromStash
from Utils.config import CHAOS_STASHES

from Models.Item import ItemType

SESS_ID = "171a88b7cfdf0d09d50666729a4d559f"
CHARACTER = "kwoktopus"
LEAGUE = "Ritual"

itemMap = {}
for enum in ItemType:
    itemMap[enum] = set()


for tab in CHAOS_STASHES:
    for item in queryItemsFromStash(tab):
        itemMap[item.type].add(item)

for key,value in itemMap.items():
    print(key, len(value))

for item in itemMap[ItemType.OTHER]:
    print(item)