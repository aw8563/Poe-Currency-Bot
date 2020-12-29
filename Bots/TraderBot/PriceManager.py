import requests
from fractions import Fraction

class PriceManager:
    def __init__(self):
        # just alcs for now
        self.currencies = {"Orb of Alchemy" : (0,0)}


    def getCurrencies(self):
        for currency in self.currencies:
            ratio = self.getRatio(currency)
            ratio *= .95 # lower it a bit

            ratio = round(ratio, 1)
            fraction = Fraction(str(ratio))

            # calculate sell and buy from the ratio
            sell = fraction.numerator
            buy = fraction.denominator

            self.currencies[currency] = (sell, buy)
            yield currency, sell, buy

    # this just returns the ratio for alcs : chaos
    # TODO: handle chaos : alc
    def getRatio(self, currency):
        URL = 'https://poe.ninja/api/data/CurrencyOverview?league=Flashback%20(DRE007)&type=Currency&language=en'

        while True:
            try:
                response = requests.get(URL)
                for line in response.json()['lines']:
                    # print(line['currencyTypeName'], "=", line['chaosEquivalent'], "chaos")
                    if (currency not in line['currencyTypeName']):
                        continue

                    return 1/float(line['receive']['value'])


                # should never get here
                return -1

            except:
                pass

    # buyAmount = how much they are buying
    # sellAmount = how much we are selling
    def validate(self, currency, buyAmount, sellAmount):
        return self.getRatio(currency) >= buyAmount/sellAmount

priceManager = PriceManager()