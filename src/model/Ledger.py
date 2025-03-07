
from decimal import Decimal
from datetime import datetime
from model.Account import Account, AccType
from control.LedgerFileManager import LedgerFileManager

class LedgerError(Exception):
    pass

class AccountNotFoundError(LedgerError):
    pass

class AccountExistsError(LedgerError):
    pass

# The Ledger has a name is responsible for managing all accounts, validating transactions, and recording entries within a transaction to the corresponding accounts
# A transaction consists of 2 or more entries. An entry affects one account
class Ledger:
    def __init__(self, path):
        self._file_manager = LedgerFileManager(path)
        self.name: str = self._file_manager.get_ledger_name()
        self.accounts: dict[str, Account] = self._file_manager.get_accounts()
    
    ####### Public methods ########

    def create_account(self, name: str, acc_type: str):
        """Creates an account with a name and type"""
        acc_type = acc_type.upper()

        if acc_type not in [e.name for e in AccType]: # if account type is invalid
            raise TypeError(f"Account type is invalid.")
        elif name in self.accounts.keys(): # if account already exists
            raise AccountExistsError(f"Account '{name}' already exists.")
        else:
            self.accounts[name] = Account(name, AccType(acc_type))
            self._file_manager.commit_new_account(self.accounts[name])
            
    def delete_account(self, name:str):
        """(not implemented) Deletes account from 1. .csv file, 2. self.config. Updates config file and reinitializes accounts"""
        pass

    def write_transaction(self, date:datetime, description:str, entries:list[tuple[str,Decimal]]):
        """Validates and writes a transaction to the corresponding set of accounts given in entries. entries = [(account_name, amount)] Raises exception if any input is invalid"""
        
        self._validate_transaction(date, description, entries) # will raise exception if errors found
        
        for entry in entries:
            self.accounts[entry[0]].write_transaction(description, entry[1], date)

    def get_balance(self):
        res = "ASSETS = LIABILITIES + INCOME - EXPENSES \n"

        total_assets = sum(acc.get_balance() for acc in self.accounts.values() if acc.acc_type == AccType.ASSET)
        total_liabilities = sum(acc.get_balance() for acc in self.accounts.values() if acc.acc_type == AccType.LIABILITY)
        total_income = sum(acc.get_balance() for acc in self.accounts.values() if acc.acc_type == AccType.INCOME)
        total_expenses = sum(acc.get_balance() for acc in self.accounts.values() if acc.acc_type == AccType.EXPENSE)

        total_right = total_liabilities + total_income - total_expenses

        res += f"${total_assets} = ${total_liabilities} + ${total_income} - ${total_expenses} \n"
        res += f"{total_assets} = {total_right} \n"

        return res + f"The accounts are {'correct' if total_assets == total_right else 'incorrect'}."

    def save_changes(self):
        self._file_manager.save_changes(self.accounts)

    ########## Private methods ############

    def _validate_transaction(self, date:datetime, description:str, entries:list[tuple]):
        """Validates a transaction's date, description, and entries. Raises exception if invalid"""
        self._validate_date(date)
        self._validate_description(description)
        self._validate_entries(entries)
                    
    def _validate_date(self, date: datetime):
        """Checks if the date is in the future"""
        if date > datetime.now():
            raise ValueError("Date can't be in the future")

    def _validate_description(self, description: str):
        """Checks if the description is empty"""
        if len(description) == 0:
            raise ValueError("Description can't be empty")

    def _validate_entries(self, entries: list[tuple]):
        """Validates and tallies all the entries following the balance sheet identity (A = L + R - X)"""
        tally = 0

        if len(entries) == 0:
            raise ValueError("No entries were provided")
        
        for entry in entries:
            acc_name = entry[0]
            amount = entry[1]

            if acc_name not in self.accounts.keys():
                raise FileNotFoundError(f"Account {acc_name} doesn't exist")
            else:
                acc_type = self.accounts[acc_name].acc_type

                match acc_type: # Follows the accounting identity ASSETS = LIABILITIES + INCOME - EXPENSES.
                    case AccType.ASSET:
                        tally += amount
                    case AccType.LIABILITY:
                        tally -= amount
                    case AccType.INCOME:
                        tally -= abs(amount)
                    case AccType.EXPENSE:
                        tally += abs(amount)

        if tally != 0:
            raise ArithmeticError("Entries amounts don't tally")
        
    ####### Overloading ########
    
    def __str__(self):
        result = f"Ledger: {self.name} \n"

        for value in AccType:
            result += f"\n{value.value} ACCOUNTS"
            has_account = False
            for account in self.accounts.values():
                if account.acc_type == value.value:
                    has_account = True
                    result += "\n" + "  - " + account.name
            if not has_account:
                result += "\n" + "  (empty)"

        return result