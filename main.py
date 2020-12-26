#!/usr/bin/python3
import time

from config import *
from commands import *
from ItemFilter import *

def main():
    # focusGame()
    # moveToStashAndOpen()
    # getFromStash()
    # moveToShopAndOpen()
    sellToVendor()

# switch focus to the game
def focusGame():
    click(GAME_X, GAME_Y)
    time.sleep(1)

# initial position is at vendor
def moveToStashAndOpen():
    # move and open
    click(STASH_X, STASH_Y, True, double=True)

    # give it some time to move
    time.sleep(2)

# assumes we are in default position next to our stash
def moveToShopAndOpen():
    # move to vendor
    click(VENDOR_X, VENDOR_Y)

    # give it some time to move
    time.sleep(2)

    # open shop
    click(SHOP_BUTTON_X, SHOP_BUTTON_Y)

# assumes we are in the stash screen
def getFromStash():
    # switch to chaos folder
    click(FOLDER_X, FOLDER_Y)

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
            return

    # exit stash
    closeWindow()

# switches to tab(x,y)
# item must satisfies accept(item text)
# grabs items up to count inclusive
def getItemFromStashTab(requirements):
    # move to correct tab
    click(requirements.tabX, requirements.tabY)

    prev = ""
    count = 0

    # iterate through the tab
    for j in range(STASH_COLS):
        for i in range(STASH_ROWS):
            x = STASH_CELL_X + j * CELL_SIZE
            y = STASH_CELL_Y + i * CELL_SIZE

            # get the item there
            text = readItem(x, y)

            # same item as before (item takes multiple cells)
            if text == prev:
                continue

            prev = text

            # the correct item type we are looking for
            if requirements.accept(text):
                print("found")
                count += 1

                # CLICK TWICE JUST IN CASE
                click(x, y, ctrl=True, double=True)

            if count == requirements.count:
                return True

    return False


# assumes we are in the sell screen
def sellToVendor():
    for j in range(INVENTORY_COLS):
        for i in range(INVENTORY_ROWS):
            x = INVENTORY_X + j*CELL_SIZE
            y = INVENTORY_Y + i*CELL_SIZE

            click(x, y, ctrl=True, double=True)

            if isChaos():
                sell()
                closeWindow()
                return True

    return False

# assumes we are in sell screen
# returns true if chaos recipe is done, false otherwise
# checks if the top left cell in vendor is a chaos orb
def isChaos():
    return "Chaos Orb" in readItem(SHOP_CELL_X, SHOP_CELL_Y)

# TODO: just moves mouse to sell, doesn't actually click it yet
# sells our items
def sell():
    pyautogui.moveTo(SELL_BUTTON_X, SELL_BUTTON_Y)
    # pyautogui.click(SELL_X, SELL_Y)

# ctrl + c
def copy():
    pyautogui.hotkey('ctrl', 'c')

if __name__ == "__main__":
    main()