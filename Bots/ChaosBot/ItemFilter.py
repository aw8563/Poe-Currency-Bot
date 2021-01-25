class ItemFilter:
    def __init__(self, itemType, amount):
        self.amount = amount
        self.itemType = itemType

    def accept(self, item):
        return item.itemType == self.itemType

# regex match from text
def isRing(text):
    return "Ring" in text

def isAmulet(text):
    return "Amulet" in text

def isBelt(text):
    return "Belt" in text or "Sash" in text

# since gloves/boots/helmets are in their own separate tab, we can probably just return true always

def isGlove(text):
    return "Gauntlets" in text or "Gloves" in text or "Mitts" in text

def isBoot(text):
    return "Greaves" in text or "Boots" in text or "Shoes" in text or "Slippers"

def isHelmet(text):
    # there's too many names so I ceebs
    return "" in text

def isBodyArmour(text):
    return "Armour:" in text or "Evasion Rating:" in text or "Energy Shield:" in text

def isWeapon(text):
    return "Physical Damage:" in text and \
           "Critical Strike Chance:" in text and \
           "Attacks per Second:" in text
