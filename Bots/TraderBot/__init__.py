from Bots.Bot import Bot
from Bots.TraderBot.steps import updateCurrencyPrices, waitForTrade, emptyInventory, test

steps = [
    updateCurrencyPrices,
    waitForTrade,
    emptyInventory
]

bot = Bot(steps)