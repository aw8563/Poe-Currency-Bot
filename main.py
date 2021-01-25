#!/usr/bin/python3
from Bots import chaosBot, traderBot

def main():
    # this will indefinitely run until chaos recipe fails
    # to exit early, move mouse to the top
    chaosBot.run()
    # traderBot.run()

if __name__ == "__main__":
    main()