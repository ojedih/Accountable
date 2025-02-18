import os
from pathlib import Path
from ui.LedgerMenu import LedgerMenu
import json

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
    def __init__(self, dir: str):
        self.dir = dir
    
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
                    self.display_ledgers()
                case "o":
                    self.open_ledger(entry[1]) # will fail if no second argument is given
                case "n":
                    self.new_ledger(entry[1]) # will fail if no second argument is given
                case "e":
                    return
                case _:
                    pass

    def display_ledgers(self):
        try:
            print([folder.name for folder in Path(self.dir).iterdir() if folder.is_dir()])
        except FileNotFoundError:
            print(f"Error: The {self.dir} directory doesn't exist.")

    def open_ledger(self, name):
        if os.path.isdir(self.dir + name):
            LedgerMenu(self.dir + name + "/")
        else:
            print(f"Ledger {name} doesn't exist")

    def new_ledger(self, name):
        if not os.path.isdir(self.dir + name): # check if directory exists
            try:
                os.makedirs(self.dir + name) # create directory
                
                with open(self.dir + name + "/config.json", mode="w", newline='') as file: # create file
                    init_config = { # base config structure
                        'name': name,
                        'accounts': {}
                    }
                    json.dump(init_config, file, indent=4)
                
                print(f"New ledger {name} created")
            except Exception as e:
                print(f"Error while creating ledger: {e}")
        else:
            print(f"Cannot create ledger. Ledger {name} already exists")