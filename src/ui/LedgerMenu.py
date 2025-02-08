from datetime import datetime
from decimal import Decimal
from model.Ledger import Ledger

msg_options = """
Select an option:
    [s] Save changes
    [n] New Transaction
    [d] Show accounts
    [c] Create Account
    [e] Go back to main menu
"""

class LedgerMenu:
    def __init__(self, ledger_path):
        try:
            self.ledger = Ledger(ledger_path)
            self.entry()
        except Exception as e:
            print(f"Failed initializing ledger: {e}")
    
    def entry(self):
        print(self.ledger)
        self.select_option()

    def select_option(self):
        while True:
            print(msg_options)
            
            option = input(":: ")
            option = option.split()
            
            match option[0]:
                case "s":
                    self.ledger.save_changes()
                case "n":
                    #print(self.ledger.get_accounts())
                    self.new_transaction()
                case "c":
                    return
                case "e":
                    return
                case _:
                    pass

    def new_transaction(self):
        # 1. date
        date_string = input("Date (mm-dd-yyyy): ")
        parsed_date = datetime.strptime(date_string, "%m-%d-%Y")

        # 2. description
        description = input("Description: ")

        # 3. Entries
        entries = []
        while True:
            entry = input("Entry [account] [amount]: ")
            
            if entry == "":
                break

            split_entry = entry.split()
            
            acc_name = split_entry[0]
            amount = Decimal(split_entry[1])
            
            entries.append((acc_name, amount))

        # 4. Validate Transactions
        self.ledger.validate_transaction(parsed_date, description, entries)


#l1 = Ledger("ledger/testledger/")
#control = LedgerController(l1)

