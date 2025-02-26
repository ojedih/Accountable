from datetime import datetime
from model.Account import AccType

class InvalidDateError(Exception):
    pass

class InvalidDescriptionError(Exception):
    pass

class AccountDoesNotExistError(Exception):
    pass

class NoEntriesError(Exception):
    pass

class TallyError(Exception):
    pass

def validate_transaction(date:datetime, description:str, entries:list[tuple], accounts:dict):
    """Validates a transaction's date, description, and entries. Raises exception if invalid"""
    validate_date(date)
    validate_description(description)
    validate_entries(entries, accounts)
                
def validate_date(date: datetime):
    """Checks if the date is in the future"""
    if date > datetime.now():
        raise InvalidDateError("Date can't be in the future")

def validate_description(description: str):
    """Checks if the description is empty"""
    if len(description) == 0:
        raise InvalidDescriptionError("Description can't be empty")

def validate_entries(entries: list[tuple], accounts: dict):
    """Validates and tallies all the entries following the balance sheet identity (A = L + R - X)"""
    tally = 0

    if len(entries) == 0:
        raise NoEntriesError("No entries were provided")
    
    for entry in entries:
        acc_name = entry[0]
        amount = entry[1]

        if acc_name not in accounts.keys():
            raise AccountDoesNotExistError(f"Account {acc_name} doesn't exist")
        else:
            acc_type = accounts[acc_name].acc_type

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
        raise TallyError("Entries amounts don't tally")