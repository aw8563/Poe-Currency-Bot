class ItemFilter:
    def __init__(self, itemType, amount):
        self.amount = amount
        self.itemType = itemType

    def accept(self, item):
        return item.itemType == self.itemType