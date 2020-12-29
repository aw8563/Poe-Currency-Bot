from Bots.Bot import Bot
from Bots.TraderBot.steps import updatePrice, waitForTrade, emptyInventory, test

steps = [
    updatePrice,
    waitForTrade,
    emptyInventory
]

bot = Bot(steps)