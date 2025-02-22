from datetime import datetime
from model.Account import AccType

def validate_transaction(date:datetime, description:str, entries:list[tuple], accounts:dict) -> bool:
    """Validates a transaction's date, description, and entries. Returns false if any are invalid."""

    return validate_date(date) and validate_description(description) and validate_entries(entries, accounts)
                
def validate_date(date: datetime) -> bool:
    """Returns false if the date is in the future. True otherwise"""
    if date > datetime.now():
        print("Date can't be in the future")
        return False
    return True

def validate_description(description: str) -> bool:
    """Returns false if the description is empty. True otherwise"""
    if len(description) == 0:
        print("Description can't be empty")
        return False
    return True

def validate_entries(entries: list[tuple], accounts: dict) -> bool:
    """Tallies all the entries following the balance sheet identity (A = L + R - X). Returns false if tally is not 0, true otherwise"""
    tally = 0

    if len(entries) == 0:
        print("No entries were provided")
        return False
    
    for entry in entries:
        acc_name = entry[0]
        amount = entry[1]

        if acc_name not in accounts.keys():
            print(f"Account {acc_name} doesn't exist")
            return False
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
        print("Entries amounts don't tally")
        return False

    return True