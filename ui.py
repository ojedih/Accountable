import os
from pathlib import Path

msg_welcome = """
Welcome to Accountable!
v0.1"""

msg_options = """
Select an option:
    [s] Display ledgers
    [o] Open ledger
    [n] New ledger
    [d] Delete ledger
    [e] Exit
"""

LEDGER_DIR = "ledger/"

def welcome():
    os.system('clear')
    print(msg_welcome)
    select_option()

def select_option():
    while True:
        print(msg_options)
        
        selected = input(":: ")
        selected = selected.split()
        
        match selected[0]:
            case "s":
                displayLedgers()
            case "o":
                return
            case "n":
                return
            case "d":
                return
            case "e":
                return
            case _:
                pass

def displayLedgers():
    try:
        print([folder.name for folder in Path(LEDGER_DIR).iterdir() if folder.is_dir()])
    except FileNotFoundError:
        print(f"Error: The {LEDGER_DIR} directory doesn't exist.")

def openLedger(name):
    pass

def newLedger(name):
    pass

def deleteLedger(name):
    pass

welcome()
print("All changes are saved. Bye Bye")