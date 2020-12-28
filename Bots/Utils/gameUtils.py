import time

from Bots.Utils.keyboardMouseUtils import *
from Bots.Utils.config import  *

def invite(name):
    type("\n/invite %s\n" % name)

def trade(name):
    type("\n/tradewith %s\n" % name)

def sell():
    click(SELL_BUTTON_X, SELL_BUTTON_Y)
    time.sleep(0.5)

def focusGame():
    click(GAME_X, GAME_Y)
    time.sleep(0.5)

def vendorCells():
    for j in range(INVENTORY_COLS):
        for i in range(INVENTORY_ROWS):
            x = SHOP_CELL_X + j * CELL_SIZE
            y = SHOP_CELL_Y + i * CELL_SIZE

            yield x, y

def inventoryCells():
    for j in range(INVENTORY_COLS):
        for i in range(INVENTORY_ROWS):
            x = INVENTORY_X + j * CELL_SIZE
            y = INVENTORY_Y + i * CELL_SIZE

            yield x, y

def stashCells():
    for j in range(STASH_COLS):
        for i in range(STASH_ROWS):
            x = STASH_CELL_X + j * CELL_SIZE
            y = STASH_CELL_Y + i * CELL_SIZE

            yield x, y