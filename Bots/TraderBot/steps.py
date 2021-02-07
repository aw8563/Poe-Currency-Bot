import os

from Utils.gameUtils import *
from Bots.TraderBot.Currency import Currency
from Bots.TraderBot.PriceManager import priceManager

processed = set()

def test():
    trade = Trade(pollMsg())

class Trade:
    def __init__(self, msg):
        self.msg = msg[msg.find('@'):]
        self.name = self.msg[:self.msg.find(":")].split(" ")[-1]

        s = msg[msg.find("your ") + 5:]
        self.buyAmount = int(s[:s.find(" ")])
        s = s[s.find(" ") + 1:]
        self.buyCurrency = s[:s.find(" for my")]

        s = s[s.find("for my ") + 7:]
        self.sellAmount = int(s[:s.find(" ")])

        s = s[s.find(" ") + 1:]
        self.sellCurrency = s[:s.find(" in ")]

        # true if we are trading our currency for chaos
        # false if we are trading our chaos for currency
        self.side = CURRENCY_NAME == self.buyCurrency

    def attemptToTrade(self):
        print("%s: buying %s (%d) for %s (%d)" %
              (self.name, self.buyCurrency, self.buyAmount, self.sellCurrency, self.sellAmount))

        if not self.validatePrices():
            return False

        if not self.inviteParty():
            emptyInventory()
            return False

        if not self.requestTrade():
            emptyInventory()
            return False

        if not self.performTrade():
            cancelTrade()
            return False

        # wait for them to hover
        time.sleep(3)

        acceptTrade() # accept the trade
        cancelTrade() # in case they don't accept, we want to cancel trade

        return True

    def validatePrices(self):
        x, y = (CURRENCY_X, CURRENCY_Y) if self.side else (CHAOS_X, CHAOS_Y)
        currencyInStash = Currency(readItem(x, y))

        return currencyInStash.total >= self.buyAmount and \
               priceManager.validate(self.side, self.buyAmount, self.sellAmount)

    # invite to party and wait until he joins hideout
    def inviteParty(self):
        # invite
        invite(self.name)

        # in the meantime, grab the currency
        self.getFromStash()

        start = time.time()
        while True:
            if "%s has joined the area" % (self.name) in pollMsg(10):
                return True

            # if the person takes too long
            if time.time() - start > WAIT_TIME:
                break

        return False

    # initiate trade request and wait for him to accept
    def requestTrade(self):
        # wait a bit
        time.sleep(2)

        # trade req
        trade(self.name)

        # wait to accept
        start = time.time()
        while True:
            if readItem(INVENTORY_X, INVENTORY_Y) != "":
                return True

            if time.time() - start > WAIT_TIME:
                break

        return False

    # do the trade
    def performTrade(self):
        for x, y in inventoryCells():
            # stop if we have put everything in already
            if readItem(x,y) == "":
                break

            click(x, y, secondary='ctrl')

        total = 0
        for x, y in vendorCells():
            text = readItem(x,y)

            currency = Currency(text)
            if currency.type == self.sellCurrency:
                total += currency.total

            if total >= self.sellAmount:
                return True

        # do it again just in case they are slow as fuck
        total = 0
        for x, y in vendorCells():
            text = readItem(x,y)

            currency = Currency(text)
            if currency.type == self.sellCurrency:
                total += currency.total

            if total >= self.sellAmount:
                return True

        return False

    # TODO: handle currency
    # assume alcs for now
    def getFromStash(self):
        x, y = (CURRENCY_X, CURRENCY_Y) if self.side else (CHAOS_X, CHAOS_Y)
        currency = Currency(readItem(x, y))

        # get the "leftover" bits
        click(x, y, secondary='shift')
        type(str(self.buyAmount%currency.stack))
        click(x + AMOUNT_BUTTON_OFFSET_X, y + AMOUNT_BUTTON_OFFSET_Y)
        click(INVENTORY_X, INVENTORY_Y)

        click(x, y, secondary='ctrl', amount=self.buyAmount//currency.stack)

def updateCurrencyPrices():
    sell, buy = priceManager.getCurrencyToChaosRatio()
    updatePrice(CURRENCY_X, CURRENCY_Y, sell, buy)

    sell, buy = priceManager.getChaosToCurrencyRatio()
    updatePrice(CHAOS_X, CHAOS_Y, sell, buy)

    return True

# tab must be set to public and the chosen opposite buy currency pre selected
def updatePrice(x, y, sell, buy):
    # bring up the sell price ui
    click(x, y, button="secondary")

    # delete old sell price
    click(x + PRICE_INPUT_OFFSET_X, y + PRICE_INPUT_OFFSET_Y, amount=2)
    backspace()

    # set new sell price
    type("%d/%d" % (buy, sell))
    click(x + PRICE_ACCEPT_OFFSET_X, y + PRICE_ACCEPT_OFFSET_Y)

def emptyInventory():
    print("emptying...")

    for x, y in inventoryCells():
        click(x, y, secondary='ctrl')
        break

    return True

def waitForTrade():
    print("waiting for trade")
    while True:
        msg = pollMsg()

        if not isTradeMsg(msg):
            continue

        trade = Trade(msg)

        if trade.msg in processed:
            continue

        processed.add(trade.msg)
        time.sleep(1)
        if not trade.attemptToTrade():
            continue

        return True

def pollMsg(amount=1):
    with open('E:\Path of Exile\logs\Client.txt', 'rb') as file:
        file.seek(-300*amount, os.SEEK_END)
        return file.readlines()[-1].decode("utf-8") if amount == 1 else \
            [line.decode("utf-8") for line in file.readlines()[-1*amount:]]

def isTradeMsg(msg):
    return "Hi, I'd like to buy your" in msg and "@From" in msg
