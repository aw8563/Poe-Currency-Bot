class ItemFilter:
    def __init__(self, tabX, tabY, fn, count):
        self.tabX = tabX
        self.tabY = tabY
        self.fn = fn
        self.count = count

    # TODO: check ilvl
    def isValidForChaosRecipe(self, text):
        return "Rarity: Rare" in text and "Unidentified" in text

    def accept(self, text):
        return self.isValidForChaosRecipe(text) and self.fn(text)

# regex match from text
def isRing(text):
    return "Ring" in text

def isAmulet(text):
    return "Amulet" in text

def isBelt(text):
    return "Belt" in text or "Sash" in text

def isGlove(text):
    return "Gloves" in text

def isBoot(text):
    return "Boot" in text

def isHelmet(text):
    return "Helmet" in text or "Mask" in text

def isBodyArmour(text):
    return "Armour" in text

# for now only 'large' weapons
def isWeapon(text):
    return "Sword" in text or "Axe" in text
