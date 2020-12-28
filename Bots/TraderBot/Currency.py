class Currency:
    def __init__(self, text):
        text = text[text.find("Stack Size: ") + 12:]
        total, stack = text[:text.find('\r')].split("/")

        self.total = int(total)
        self.stack = int(stack)
        self.type = ""