#!/usr/bin/python3
import time

from ChaosBot.config import *
from ChaosBot.commands import *
from ChaosBot.ItemFilter import *

class Bot:
    def __init__(self, test=False, debug=False):
        self.debug = debug
        self.test = test
        self.running = True

        self.commands = [
            self.moveToStashAndOpen,
            self.getFromStash,
            self.moveToShopAndOpen,
            self.sellToVendor
        ]

    def run(self):
        self.focusGame()

        # Initial character position should be at vendor
        while True:
            for step in self.commands:
                if not step():
                    return

    # switch focus to the game
    def focusGame(self):
        click(GAME_X, GAME_Y)
        time.sleep(0.5)

    # initial position is at vendor
    def moveToStashAndOpen(self):
        # move and open
        click(STASH_X, STASH_Y, True, double=True)

        # give it some time to move
        time.sleep(2)
        return not checkExit()

    # assumes we are in default position next to our stash
    def moveToShopAndOpen(self):
        # move to vendor
        click(VENDOR_X, VENDOR_Y)

        # give it some time to move
        time.sleep(2)

        # open shop
        click(SHOP_BUTTON_X, SHOP_BUTTON_Y)

        return not checkExit()

    # assumes we are in the stash screen
    def getFromStash(self):
        if self.test:
            closeWindow()
            return True

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
            if not self.getItemFromStashTab(requirements):
                return False

        # exit stash
        closeWindow()
        return True

    # switches to tab(x,y)
    # item must satisfies accept(item text)
    # grabs items up to count inclusive
    def getItemFromStashTab(self, requirements):
        # move to correct tab
        click(requirements.tabX, requirements.tabY)

        prev = ""
        count = 0

        # iterate through the tab
        for j in range(STASH_COLS):
            for i in range(STASH_ROWS):
                if checkExit():
                    return False

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
                    count += 1

                    if self.debug:
                        print("item found")

                    # CLICK TWICE JUST IN CASE
                    click(x, y, ctrl=True, double=True)

                if count == requirements.count:
                    return True

        return False


    # assumes we are in the sell screen
    def sellToVendor(self):
        if self.test:
            self.sell()
            closeWindow()
            return True

        # iterate through each cell in shop
        for j in range(INVENTORY_COLS):
            for i in range(INVENTORY_ROWS):
                if checkExit():
                    return False

                x = INVENTORY_X + j*CELL_SIZE
                y = INVENTORY_Y + i*CELL_SIZE

                # skip non unid rares
                if not self.isChaosRecipeItem(x, y):
                    continue

                click(x, y, ctrl=True, double=True)

                # recipe is complete
                if self.isRecipeFinished():
                    self.sell()
                    closeWindow()
                    return True

        return False

    # assumes we are in sell screen
    # checks if current item is part of chaos recipe
    def isChaosRecipeItem(self, x, y):
        text = readItem(x, y)
        return "Rarity: Rare" in text and "Unidentified" in text

    # assumes we are in sell screen
    # returns true if chaos recipe is done, false otherwise
    # checks if the top left cell in vendor is a chaos orb
    def isRecipeFinished(self):
        return "Chaos Orb" in readItem(SHOP_CELL_X, SHOP_CELL_Y)

    # TODO: just moves mouse to sell, doesn't actually click it yet
    # sells our items
    def sell(self):
        click(SELL_BUTTON_X, SELL_BUTTON_Y)
        time.sleep(0.5)
