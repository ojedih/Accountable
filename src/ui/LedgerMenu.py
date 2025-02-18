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
        self.run()
    
    def run(self):
        print(self.ledger)

        while True:
            print(msg_options)
            
            entry = input(":: ")
            entry = entry.split()
            
            match entry[0]:
                case "s":
                    self.ledger.save_changes()
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

    def new_transaction(self):
        # 1. date
        date_string = input("Date (mm-dd-yyyy):: ")
        parsed_date = datetime.strptime(date_string, "%m-%d-%Y")

        # 2. description
        description = input("Description:: ")

        # 3. Entries
        entries = []
        while True:
            entry = input("Entry [account] [amount]:: ")
            
            if entry == "":
                break

            split_entry = entry.split()
            
            acc_name = split_entry[0]
            amount = Decimal(split_entry[1])
            
            entries.append((acc_name, amount))

        # 4. Validate Transactions
        self.ledger.validate_transaction(parsed_date, description, entries)

    def create_account(self, name, acc_type):
        self.ledger.create_account(name, acc_type)


#l1 = Ledger("ledger/testledger/")
#control = LedgerController(l1)

