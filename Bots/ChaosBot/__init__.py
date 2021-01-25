from Bots.Bot import Bot
from Bots.ChaosBot.steps import test, moveToShopAndOpen, getFromStash, moveToStashAndOpen, sellToVendor

steps = [
    moveToStashAndOpen,
    getFromStash,
    moveToShopAndOpen,
    sellToVendor
]

bot = Bot(steps)
