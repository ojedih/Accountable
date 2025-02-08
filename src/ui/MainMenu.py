import os
from pathlib import Path
from model.Ledger import Ledger
from ui.LedgerMenu import LedgerMenu

msg_welcome = """
Welcome to Accountable!
v0.1"""

msg_options = """
Select an option:
    [s] Display ledgers
    [o] Open ledger
    [n] New ledger
    [e] Exit
"""

LEDGER_DIR = "ledger/"

class MainMenu:
    def entry(self):
        os.system('clear')
        print(msg_welcome)
        self.select_option()

    def select_option(self):
        while True:
            print(msg_options)
            
            entry = input(":: ")
            entry = entry.split()
            
            match entry[0]:
                case "s":
                    self.displayLedgers()
                case "o":
                    self.openLedger(entry[1])
                case "n":
                    return
                case "d":
                    return
                case "e":
                    return
                case _:
                    pass

    def displayLedgers(self):
        try:
            print([folder.name for folder in Path(LEDGER_DIR).iterdir() if folder.is_dir()])
        except FileNotFoundError:
            print(f"Error: The {LEDGER_DIR} directory doesn't exist.")

    def openLedger(self, name):
        if os.path.isdir(LEDGER_DIR + name):
            LedgerMenu(LEDGER_DIR + name + "/")
        else:
            print(f"Ledger {name} doesn't exist")

    def newLedgers(self, name):
        pass

    def deleteLedger(self, name):
        pass

#welcome()
#print("All changes are saved. Bye Bye")