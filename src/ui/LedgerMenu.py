from datetime import datetime
from decimal import Decimal
from model.Ledger import Ledger

msg_options = """
Select an option:
    - [s]ave changes

    - [n]ew transaction
    - [d]isplay accounts
    - [c]reate account [account_name] [account_type]

    - [e] Go back to main menu
"""

class LedgerMenu:
    def __init__(self, ledger_path):
        self.ledger = Ledger(ledger_path)
    
    def run(self):
        print(self.ledger)

        while True:
            print(msg_options)
            
            entry = input(":: ")
            entry = entry.split()
            
            match entry[0]:
                case "s":
                    self.save_changes()
                case "n":
                    self.new_transaction()
                case "d":
                    print(self.ledger)
                case "c":
                    self.create_account(entry[1], entry[2])
                case "e":
                    return
                case _:
                    pass

    def save_changes(self):
        try:
            self.ledger.save_changes()
            print("Changes saved successfully")
        except Exception as e:
            print(f"Error while saving changes: {e}")
    
    def new_transaction(self):
        # 1. input date
        date_string = input("Date (mm-dd-yyyy):: ")
        parsed_date = datetime.strptime(date_string, "%m-%d-%Y")

        # 2. input description
        description = input("Description:: ")

        # 3. input entries
        entries = []
        while True:
            entry = input("Entry [account] [amount]:: ")
            
            if entry == "":
                break

            split_entry = entry.split()
            
            acc_name = split_entry[0]
            amount = Decimal(split_entry[1])
            
            entries.append((acc_name, amount))

        # 4. Write Transaction
        try:
            self.ledger.write_transaction(parsed_date, description, entries)
            print("New transaction successfully recorded. Changes are NOT saved.")
        except Exception as e:
            print(f"Error while recording transaction: {e}")

    def create_account(self, name, acc_type):
        try:
            self.ledger.create_account(name, acc_type)
            print(f"Account '{name}' created and saved.")
        except Exception as e:
            print(f"Error while creating an account: {e}")