#!/usr/bin/python3

import pyautogui
import win32clipboard
import time

# uses 1278x948 game resolution at top left hand corner
# windows key + left arrow to adjust game window to appropriate position/size on 2550x1440 monitor

# These values will all change if anything is different!
CELL_SIZE = 45

SELL_BUTTON_X = 125
SELL_BUTTON_Y = 750

STASH_X = 765
STASH_Y = 340
STASH_CELL_X = 15 + CELL_SIZE//2
STASH_CELL_Y = 180 + CELL_SIZE//2
STASH_ROWS = 12
STASH_COLS = 12

INVENTORY_X = 710 + CELL_SIZE//2
INVENTORY_Y = 550 + CELL_SIZE//2
INVENTORY_ROWS = 5
INVENTORY_COLS = 12

FOLDER_X = 270
FOLDER_Y = 135

TAB_Y = 165
JEWELRY_TAB_X = 185
GLOVE_TAB_X = 240
BOOT_TAB_X = 295
HELMET_TAB_X = 345
ARMOUR_AND_WEAPON_TAB_X = 400

VENDOR_X = 465
VENDOR_Y = 500

SHOP_BUTTON_X = 630
SHOP_BUTTON_Y = 260

GAME_X = 1278//2
GAME_Y = 15

def main():
    focusGame()
    moveToStashAndOpen()
    getFromStash()
    moveToShopAndOpen()
    sellToVendor()

# switch focus to the game
def focusGame():
    click(GAME_X, GAME_Y)

# initial position is at vendor
def moveToStashAndOpen():
    # move and open
    click(STASH_X, STASH_Y)

    # give it some time to move
    time.sleep(2)

# assumes we are in default position next to our stash
def moveToShopAndOpen():
    # move
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

    # 1st page is jewelry
    getItemFromStashTab(JEWELRY_TAB_X, TAB_Y, isRing, 2)
    getItemFromStashTab(JEWELRY_TAB_X, TAB_Y, isAmulet, 1)
    getItemFromStashTab(JEWELRY_TAB_X, TAB_Y, isBelt, 1)

    # 2nd page is gloves
    getItemFromStashTab(GLOVE_TAB_X, TAB_Y, isGlove, 1)

    # 3rd page is boots
    getItemFromStashTab(BOOT_TAB_X, TAB_Y, isBoot, 1)

    # 4th page is helmet
    getItemFromStashTab(HELMET_TAB_X, TAB_Y, isHelmet, 1)

    # 5th page is armour + weapons (only big weapons for now)
    getItemFromStashTab(ARMOUR_AND_WEAPON_TAB_X, TAB_Y, isBodyArmour, 1)
    getItemFromStashTab(ARMOUR_AND_WEAPON_TAB_X, TAB_Y, isWeapon, 1)

    # exit stash
    pyautogui.press('esc')

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

# switches to tab(x,y)
# item must satisfies accept(item text)
# grabs items up to count inclusive
def getItemFromStashTab(x, y, accept, count=1):
    # move to correct tab
    click(x, y)

    prev = ""
    # iterate through the tab
    for j in range(STASH_COLS):
        for i in range(STASH_ROWS):
            x = STASH_CELL_X + j * CELL_SIZE
            y = STASH_CELL_Y + i * CELL_SIZE

            # get the item there
            pyautogui.moveTo(x, y)
            text = read()

            # same item as before (item takes multiple cells)
            if text == prev:
                continue

            prev = text

            # the correct item type we are looking for
            if accept(text):
                print("found")
                count -= 1

                # CLICK TWICE JUST IN CASE
                click(x, y, True)
                click(x, y, True)

            if count <= 0:
                return True

    return False

# move mouse and clicks
# the default pyautogui.click(x,y) is too fast sometimes
def click(x, y, ctrl=False):
    if ctrl:
        pyautogui.keyDown('ctrl')

    pyautogui.moveTo(x, y)
    pyautogui.click()

    if ctrl:
        pyautogui.keyUp('ctrl')

# assumes we are in the sell screen
def sellToVendor():
    for j in range(INVENTORY_COLS):
        for i in range(INVENTORY_ROWS):
            x = INVENTORY_X + j*CELL_SIZE
            y = INVENTORY_Y + i*CELL_SIZE

            click(x, y, True)
    sell()

# sells our items
def sell():
    pyautogui.moveTo(SELL_BUTTON_X, SELL_BUTTON_Y)
    # pyautogui.click(SELL_X, SELL_Y)

# ctrl + c
def copy():
    pyautogui.hotkey('ctrl', 'c')

# reads our current copied value
def read():
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    copy()
    win32clipboard.OpenClipboard()
    return win32clipboard.GetClipboardData() \
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_TEXT) else ""

if __name__ == "__main__":
    main()