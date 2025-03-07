import os
from ui.LedgerMenu import LedgerMenu
from control.MainFileManager import MainFileManager

msg_welcome = """
Welcome to Accountable!
v0.1"""

msg_options = """
Select an option:
    - Di[s]play ledgers
    - [o]pen ledger [ledger_name]
    - [n]ew ledger [ledger_name]
    - [e]xit
"""

class MainMenu:
    def __init__(self, file_manager):
        self.fm: MainFileManager = file_manager
    
    def run(self):
        os.system('clear')
        print(msg_welcome)
        self.show_and_select_options()

    def show_and_select_options(self):
        while True:
            print(msg_options)
            
            entry = input(":: ")
            entry = entry.split()
            
            match entry[0]:
                case "s":
                    print(self.fm.get_ledger_names())
                case "o":
                    self.open_ledger(entry[1]) # will fail if no second argument is given
                case "n":
                    self.new_ledger(entry[1]) # will fail if no second argument is given
                case "e":
                    return
                case _:
                    pass

    def open_ledger(self, name):
        if name in self.fm.get_ledger_names():
            ledger_menu = LedgerMenu(self.fm.get_ledger_dir() + name + "/")
            ledger_menu.run()
        else:
            print(f"Couldn't open ledger. Ledger {name} doesn't exist")

    def new_ledger(self, name):
        try:
            self.fm.create_new_ledger(name)
            print(f"New ledger {name} created")
        except Exception as e:
            print(f"Error while creating ledger: {e}")