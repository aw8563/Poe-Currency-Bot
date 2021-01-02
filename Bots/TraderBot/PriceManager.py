import requests
from fractions import Fraction
from Bots.Utils.config import PRICE_DELTA, CURRENCY_NAME

class PriceManager:
    def __init__(self):
        # just alcs for now
        self.currencyToChaos = (0, 0)
        self.chaosToCurrency = (0, 0)

    def convertRatio(self, ratio):
        ratio = round(ratio, 1)
        fraction = Fraction(str(ratio))

        # calculate sell and buy from the ratio
        return fraction.numerator, fraction.denominator

    def getCurrencyToChaosRatio(self):
        ratio = self.getRatio(True)*(1 - PRICE_DELTA)
        sell, buy = self.convertRatio(ratio)

        self.currencyToChaos = (sell, buy)
        return sell, buy

    def getChaosToCurrencyRatio(self):
        ratio = 1/self.getRatio(False)*(1 + PRICE_DELTA)
        sell, buy = self.convertRatio(ratio)

        self.chaosToCurrency = (sell, buy)
        return sell, buy

    # currency : chaos if side == True other wise chaos : currency
    def getRatio(self, side):
        URL = 'https://poe.ninja/api/data/CurrencyOverview?league=Flashback%20(DRE007)&type=Currency&language=en'

        while True:
            try:
                response = requests.get(URL)
                for line in response.json()['lines']:
                    if (CURRENCY_NAME not in line['currencyTypeName']):
                        continue

                    return (1/float(line['receive']['value'])) if side else \
                        (float(line['pay']['value']))

                # should never get here
                return -1

            except:
                pass

    # if side is true then currency : chaos, other wise chaos : currency
    # buyAmount = how much they are buying
    # sellAmount = how much we are selling
    def validate(self, side, buyAmount, sellAmount):
        return self.getRatio(side) >= buyAmount/sellAmount if side else\
            self.getRatio(side) <= sellAmount/buyAmount

priceManager = PriceManager()