from Bots.Utils import *
from Bots.ChaosBot.ItemFilter import *
from Models.Item import ItemType

items = {}
for type in ItemType:
    items[type] = set()

chaosRecipeItemRequirements = [
    ItemFilter(ItemType.GLOVE, 1),
    ItemFilter(ItemType.BOOT, 1),
    ItemFilter(ItemType.BELT, 1),
    ItemFilter(ItemType.HELMET, 1),
    ItemFilter(ItemType.ARMOUR, 1),
    ItemFilter(ItemType.AMULET, 1),
    ItemFilter(ItemType.RING, 2),
    ItemFilter(ItemType.WEAPON, 1)
]

# gets all our items in stash
for idx in CHAOS_STASHES:
    for item in queryItemsFromStash(idx):
        if not item.validForChaosRecipe():
            continue

        items[item.type].add(item)

def test():
    import random
    random.shuffle(chaosRecipeItemRequirements)
    res = checkRequirements(chaosRecipeItemRequirements)
    for item in res:
        print(item)

# initial position is at vendor
def moveToStashAndOpen():
    # move and open
    click(STASH_X, STASH_Y, amount=2)

    # give it some time to move
    time.sleep(2)

    # dump currency
    click(INVENTORY_X, INVENTORY_Y, secondary='ctrl')
    return not checkExit()

# assumes we are in default position next to our stash
def moveToShopAndOpen():
    # move to vendor
    click(VENDOR_X, VENDOR_Y)

    # give it some time to move
    time.sleep(2)

    # open shop
    click(SHOP_BUTTON_X, SHOP_BUTTON_Y)

    return not checkExit()

# assumes we are in the stash screen
def getFromStash():
    # switch to chaos folder
    click(FOLDER_X, FOLDER_Y)
    time.sleep(0.5)

    if checkExit():
        return False

    itemsRequired = checkRequirements(chaosRecipeItemRequirements)

    # if we didn't find the required items
    if not itemsRequired or len(itemsRequired) != 9:
        return False

    if not getItemsFromStashTab(itemsRequired):
        return False

    # exit stash
    closeWindow()

    return not checkExit()

def checkRequirements(requirements):
    # this ordering ensures everything is always in the same spot

    under75 = False
    result = []

    for requirement in requirements:
        # if we don't have enough return false
        if not hasItem(requirement):
            return []

        for _ in range(requirement.amount):
             # make sure we have at least one under 75 so we can actually chaos recipe
            target = None
            if not under75:
                for item in items[requirement.itemType]:
                    if item.ilvl < 75:
                        under75 = True
                        target = item
                        break
            else: # if we do have under 75, then we want to prioritize items over i75 first.
                for item in items[requirement.itemType]:
                    if item.ilvl > 75 and (not result or item != result[-1]):
                        target = item

            if not target:
                for item in items[requirement.itemType]:
                    if not result or item != result[-1]:
                        target = item
                        break
            result.append(target)
    return result if under75 else []


def hasItem(requirement):
    return len(items[requirement.itemType]) >= requirement.amount

# grabs items up to count
def getItemsFromStashTab(itemsRequired):
    for item in itemsRequired:
        if checkExit():
            return False

        tabX = CHAOS_STASHES[item.stash]
        tabY = TAB_Y
        # move to correct tab
        click(tabX, tabY)

        # get x,y coordinate of item
        x, y = stashCoordToXY(item.x, item.y)

        # grab item
        time.sleep(0.15)
        click(x, y, secondary='ctrl', amount=2)
        time.sleep(0.15)

        try:
            items[item.type].remove(item)
        except:
            print("item doesn't exist somehow?")
            return False

    return not checkExit()

# assumes we are in the sell screen
def sellToVendor():
    # iterate through each cell in inventory
    # hardcoded chaos recipe slots
    for x, y in CHAOS_INVENTORY_CELLS:
        if checkExit():
            return False

        x, y = inventoryCoordToXY(x, y)

        # skip items that are not unid rares
        if not isChaosRecipeItem(x, y):
            return False

        click(x, y, secondary='ctrl')

    # recipe is complete
    if isRecipeFinished():
        acceptTrade()
        closeWindow()
        return not checkExit()

    return False

# assumes we are in sell screen
# checks if current item is part of chaos recipe
def isChaosRecipeItem(x, y):
    text = readItem(x, y)
    return "Rarity: Rare" in text and "Unidentified" in text

# assumes we are in sell screen
# returns true if chaos recipe is done, false otherwise
# checks if the top left cell in vendor is a chaos orb
def isRecipeFinished():
    return "Chaos Orb" in readItem(SHOP_CELL_X, SHOP_CELL_Y)
