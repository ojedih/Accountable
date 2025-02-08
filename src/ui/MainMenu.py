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
    [o] Open ledger [ledger_name]
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
                    self.display_ledgers()
                case "o":
                    self.open_ledger(entry[1]) # will fail if no second argument is given
                case "n":
                    return
                case "e":
                    return
                case _:
                    pass

    def display_ledgers(self):
        try:
            print([folder.name for folder in Path(LEDGER_DIR).iterdir() if folder.is_dir()])
        except FileNotFoundError:
            print(f"Error: The {LEDGER_DIR} directory doesn't exist.")

    def open_ledger(self, name):
        if os.path.isdir(LEDGER_DIR + name):
            LedgerMenu(LEDGER_DIR + name + "/")
        else:
            print(f"Ledger {name} doesn't exist")

    def new_ledger(self, name):
        pass