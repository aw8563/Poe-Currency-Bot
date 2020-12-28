from Bots.Bot import Bot
from Bots.TraderBot.steps import waitForTrade, emptyInventory

steps = [
    waitForTrade,
    emptyInventory
]

bot = Bot(steps)