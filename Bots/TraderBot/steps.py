import os

from Bots.Utils import *
from Bots.TraderBot.Currency import Currency

processed = set()
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
            return False

        if not self.requestTrade():
            return False

        if not self.performTrade():
            return False

        # trade done
        return True

    # checks prices against poeninja to make sure we are not getting scammed
    # also check we have enough
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
            if "%s has joined the area" % (self.name) in pollMsg():
                return True

            # if the person takes too long
            if time.time() - start > WAIT_TIME:
                break

        emptyInventory()
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

        emptyInventory()
        return False

    # do the trade
    def performTrade(self):
        # start from the leftover bit
        click(INVENTORY_LAST_X, INVENTORY_LAST_Y, ctrl=True)

        for x, y in inventoryCells():
            click(x, y, ctrl=True)

            # stop if we have put everything in already
            if readItem(x,y) == "":
                break

        total = 0
        for x, y in vendorCells():
            text = readItem(x,y)
            if text == "":
                continue

            currency = Currency(text)
            if currency.type == self.sellCurrency:
                total += currency.total

            if total == self.sellAmount:
                return True

        # do it again just in case they are slow as fuck
        total = 0
        for x, y in vendorCells():
            text = readItem(x,y)
            if text == "":
                continue

            currency = Currency(text)

            # TODO: handle this
            if currency.type == self.sellCurrency or currency.type == "":
                total += currency.total

        return total == self.sellAmount

    # TODO: handle currency
    # assume alts for now
    def getFromStash(self):
        x = ALTERATION_X
        y = ALTERATION_Y

        # s = text[text.find("Stack Size: ") + 12:]
        # stack = int(s[:s.find('\r')].split("/")[-1])
        currency = Currency(readItem(x, y))

        total = 0
        for i in range(self.buyAmount//currency.stack):
            click(x, y, ctrl=True)
            total += currency.stack

        if total < self.buyAmount:
            click(x, y, shift=True)
            type(str(self.buyAmount - total))
            click(x + BUTTON_OFFSET_X, y + BUTTON_OFFSET_Y)

            # put into top left if it's single
            # this is to ensure we always have a stack of currency top left corner
            click(INVENTORY_X, INVENTORY_Y) if total == 0 else \
                click(INVENTORY_LAST_X, INVENTORY_LAST_Y)

    def parseCurrency(self, text):
        text = text[text.find("Stack Size: ") + 12:]
        total, stack = text[:text.find('\r')].split("/")

        return int(total), int(stack)

def updatePrice():
    # TODO: set prices to poe.ninja prices
    return True

def emptyInventory():
    print("emptying...")

    for x, y in inventoryCells():
        click(x, y, ctrl=True)
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

def pollMsg():
    with open('E:\Path of Exile\logs\Client.txt', 'rb') as file:
        file.seek(-300, os.SEEK_END)
        return file.readlines()[-1].decode("utf-8")

def isTradeMsg(msg):
    return "Hi, I'd like to buy your" in msg and "@From" in msg
