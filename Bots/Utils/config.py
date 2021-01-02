# uses 1278x948 game resolution at top left hand corner
# windows key + left arrow to adjust game window to appropriate position/size on 2550x1440 monitor

# These values will all change if anything is different!

# size of each item box
CELL_SIZE = 45

# sell button on vendor
ACCEPT_BUTTON_X = 125
ACCEPT_BUTTON_Y = 750

# cancel button on vendor
CANCEL_BUTTON_X = 575
CANCEL_BUTTON_Y = 750

# stash location
STASH_X = 1020
STASH_Y = 460

# top left box in stash
STASH_CELL_X = 15 + CELL_SIZE//2
STASH_CELL_Y = 180 + CELL_SIZE//2

# stash dimensions
STASH_ROWS = 12
STASH_COLS = 12

# top left box in inventory
INVENTORY_X = 710 + CELL_SIZE//2
INVENTORY_Y = 550 + CELL_SIZE//2

# inventory dimensions
INVENTORY_ROWS = 5
INVENTORY_COLS = 12

# folder location
FOLDER_X = 270
FOLDER_Y = 135

# location of each tab
TAB_Y = 165
JEWELRY_TAB_X = 185
GLOVE_TAB_X = 240
BOOT_TAB_X = 295
HELMET_TAB_X = 345
ARMOUR_AND_WEAPON_TAB_X = 400

# location of the vendor
VENDOR_X = 220
VENDOR_Y = 370

# "sell item" button on vendor
SHOP_BUTTON_X = 630
SHOP_BUTTON_Y = 260

# top left box in vendor
SHOP_CELL_X = 95
SHOP_CELL_Y = 220

# top game bar
GAME_X = 1278//2
GAME_Y = 15

# % off best ask/bid to price our currency at
PRICE_DELTA = 0.05

# name and location of trading currency tab
CURRENCY_NAME = "Orb of Alchemy"
CURRENCY_X = 430
CURRENCY_Y = 295

# location of chaos in currency tab
CHAOS_X = 480
CHAOS_Y = 290

# offset of currency shift click accept button relative to the currency box
AMOUNT_BUTTON_OFFSET_X = 90
AMOUNT_BUTTON_OFFSET_Y = -40

# offset of box where you enter how much you want to sell for relative to currency box
PRICE_INPUT_OFFSET_X = -30
PRICE_INPUT_OFFSET_Y = 65

# offset of currency price accept button relative to currency box
PRICE_ACCEPT_OFFSET_X = 190
PRICE_ACCEPT_OFFSET_Y = 105

# wait 15 seconds for pty invite/trade
WAIT_TIME = 10