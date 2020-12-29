class Currency:
    def __init__(self, text):
        if text == "":
            self.type = ""
            self.total = 0
            self.stack = 0
            return

        text = text[text.find("\n") + 1:]
        self.type = text[0:text.find("\r")]

        text = text[text.find("Stack Size: ") + 12:]
        total, stack = text[:text.find('\r')].split("/")

        self.total = int(total)
        self.stack = int(stack)

    def __str__(self):
        return "%s: (%d/%d)" % (self.type, self.total, self.stack)