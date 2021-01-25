from enum import Enum

class ItemType(Enum):
    AMULET = "Amulet"
    RING = "Ring"
    BELT = "Belt"
    BOOT = "Boot"
    GLOVE = "Glove"
    HELMET = "Helmet"
    ARMOUR = "Body Armour"
    WEAPON = "Weapon"
    UNKNOWN = "Unknown"

def parseItemType(itemType, w, h, properties):
    try:
        n = len(itemType)
        if h == 1: # jewelry
            if n >= 4 and itemType[-4:] == "Ring":
                return ItemType.RING

            if n >= 6 and itemType[-6:] == "Amulet":
                return ItemType.AMULET

            if "Belt" in itemType or "Sash" in itemType:
                return ItemType.BELT

            return ItemType.UNKNOWN

        if h == 2 and w == 2: # glove, boot, helmet. We are ignoring non large weapons
            if "Gauntlets" in itemType or "Gloves" in itemType or "Mitts" in itemType:
                return ItemType.GLOVE

            if "Greaves" in itemType or "Boots" in itemType or "Shoes" in itemType or "Slippers" in itemType:
                return ItemType.BOOT

            # too many helmets i ceebs
            return ItemType.HELMET

        # weapons and armour
        if h < 3 or w != 2:
            return ItemType.UNKNOWN

        # check properties
        property = properties[0]['name']

        # only armour have amorour/es/evasion
        if property == "Armour" or property == "Energy Shield" or property == "Evasion Rating":
            return ItemType.ARMOUR

        # ceebs checking every weapon just assume it's a weapon
        return ItemType.WEAPON

    except:
        return ItemType.UNKNOWN

class Item:
    def __init__(self, json):
        self.name = json['name']
        self.ilvl = json['ilvl']
        self.identified = json['identified']
        self.x = json['x']
        self.y = json['y']
        self.w = json['w']
        self.h = json['h']
        self.typeName = json['typeLine']
        self.type = parseItemType(self.typeName, self.w, self.h, json['properties'] if 'properties' in json else [])
        self.stash = int(json['inventoryId'][5:]) - 1 # -1 if inventory

    # json doesn't contain rarity???
    def validForChaosRecipe(self):
        return self.ilvl >= 60 and not self.identified and self.type != ItemType.UNKNOWN

    def __str__(self):
        return "%s: %s (ilvl %d) [%d, %d] in stash %d" % \
               (self.type, self.typeName, self.ilvl, self.x, self.y, self.stash)
