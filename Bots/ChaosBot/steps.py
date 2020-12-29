from Bots.Utils import *
from Bots.ChaosBot.ItemFilter import *

# initial position is at vendor
def moveToStashAndOpen():
    # move and open
    click(STASH_X, STASH_Y, amount=2)

    # give it some time to move
    time.sleep(2)
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

    # get the stuff from each tab
    itemsRequired = [
        ItemFilter(JEWELRY_TAB_X, TAB_Y, isRing, 2),
        ItemFilter(JEWELRY_TAB_X, TAB_Y, isAmulet, 1),
        ItemFilter(JEWELRY_TAB_X, TAB_Y, isBelt, 1),
        ItemFilter(GLOVE_TAB_X, TAB_Y, isGlove, 1),
        ItemFilter(BOOT_TAB_X, TAB_Y, isBoot, 1),
        ItemFilter(HELMET_TAB_X, TAB_Y, isHelmet, 1),
        ItemFilter(ARMOUR_AND_WEAPON_TAB_X, TAB_Y, isBodyArmour, 1),
        ItemFilter(ARMOUR_AND_WEAPON_TAB_X, TAB_Y, isWeapon, 1)
    ]

    for requirements in itemsRequired:
        if not getItemFromStashTab(requirements):
            return False

    # exit stash
    closeWindow()

    return True

# switches to tab(x,y)
# item must satisfies accept(item text)
# grabs items up to count
def getItemFromStashTab(requirements):
    # move to correct tab
    click(requirements.tabX, requirements.tabY)

    prev = ""
    count = 0

    # iterate through the tab
    for x, y in stashCells():
        if checkExit():
            return False

        # get the item there
        text = readItem(x, y)

        # same item as before (item takes multiple cells)
        if text == prev:
            continue

        prev = text

        # the correct item type we are looking for
        if requirements.accept(text):
            count += 1

            # CLICK TWICE JUST IN CASE
            click(x, y, secondary='ctrl', amount=2)

        if count == requirements.count:
            return True

    return False


# assumes we are in the sell screen
def sellToVendor():
    # iterate through each cell in inventory
    for x, y in inventoryCells():
        if checkExit():
            return False

        # skip items that are not unid rares
        if not isChaosRecipeItem(x, y):
            continue

        click(x, y, secondary='ctrl')

        # recipe is complete
        if isRecipeFinished():
            acceptTrade()
            closeWindow()
            return True

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
