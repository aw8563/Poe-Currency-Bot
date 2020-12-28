from Bots.Bot import Bot
from Bots.ChaosBot.steps import moveToShopAndOpen, getFromStash, moveToStashAndOpen, sellToVendor

steps = [
    moveToStashAndOpen,
    getFromStash,
    moveToShopAndOpen,
    sellToVendor
]

bot = Bot(steps)
