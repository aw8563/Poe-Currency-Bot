import os

from Bots.Utils import *

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

        while True:
            if "%s has joined the area" % (self.name) in pollMsg():
                return True

        emptyInventory()
        return False

    # initiate trade request and wait for him to accept
    def requestTrade(self):
        # wait a bit
        time.sleep(2)

        # trade req
        trade(self.name)

        # wait to accept
        while True:
            return True

        return False

    # do the trade
    def performTrade(self):
        # TODO: check when trade req is accepted
        time.sleep(5)

        # start from the leftover bit
        click(INVENTORY_LAST_X, INVENTORY_LAST_Y, ctrl=True)

        # TODO: stop when we've put everything in
        for x, y in inventoryCells():
            click(x, y, ctrl=True)


        # TODO: check what they are giving me is actually legit
        for x, y in vendorCells():
            pyautogui.moveTo(x, y)

        return False

    # TODO: handle currency
    # assume alts for now
    def getFromStash(self):
        text = readItem(ALTERATION_X, ALTERATION_Y)
        s = text[text.find("Stack Size: ") + 12:]

        stack = int(s[:s.find('\r')].split("/")[-1])

        x = ALTERATION_X
        y = ALTERATION_Y
        total = 0
        for i in range(self.buyAmount//stack):
            click(x, y, ctrl=True)
            total += stack

        if total < self.buyAmount:
            click(x, y, shift=True)
            type(str(self.buyAmount - total))
            click(x + BUTTON_OFFSET_X, y + BUTTON_OFFSET_Y)
            click(INVENTORY_LAST_X, INVENTORY_LAST_Y)


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
