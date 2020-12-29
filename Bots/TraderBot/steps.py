import os

from Bots.Utils import *
from Bots.TraderBot.Currency import Currency

processed = set()

def test():
    pass

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

    # TODO: checks prices against poeninja to make sure we are not getting scammed
    # TODO: also check we have enough
    def validatePrices(self):
        return True

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
    # assume alts for now
    def getFromStash(self):
        x = ALTERATION_X
        y = ALTERATION_Y
        currency = Currency(readItem(x, y))

        # get the "leftover" bits
        click(x, y, secondary='shift')
        type(str(self.buyAmount%currency.stack))
        click(x + BUTTON_OFFSET_X, y + BUTTON_OFFSET_Y)
        click(INVENTORY_X, INVENTORY_Y)

        # for i in range(self.buyAmount//currency.stack):
        click(x, y, secondary='ctrl', amount=self.buyAmount//currency.stack)


def updatePrice():
    # TODO: set prices to poe.ninja prices
    return True

def emptyInventory():
    print("emptying...")

    for x, y in inventoryCells():
        click(x, y, secondary='ctrl')
        break

    return True

def waitForTrade():
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

        processed.remove(trade.msg)

        return True

def pollMsg(amount=1):
    with open('E:\Path of Exile\logs\Client.txt', 'rb') as file:
        file.seek(-300*amount, os.SEEK_END)
        return file.readlines()[-1].decode("utf-8") if amount == 1 else \
            [line.decode("utf-8") for line in file.readlines()[-1*amount:]]

def isTradeMsg(msg):
    return "Hi, I'd like to buy your" in msg and "@From" in msg
