import os
import csv
import json
import pandas as pd
from decimal import Decimal
from datetime import datetime
from model.Account import Account, AccType
from model.Validator import validate_transaction

class LedgerError(Exception):
    pass

class AccountExistsError(LedgerError):
    pass

class AccountTypeInvalidError(LedgerError):
    pass

class InvalidTransactionError(LedgerError):
    pass

class Ledger:
    def __init__(self, path):
        self.path = path
        self.config = {}
        self.accounts = {}
                
        self.load_config()
        self.load_accounts()
            
    def load_config(self):
        """Loads config.json file into self.config[]"""
        with open(self.path + "config.json", "r") as file:
            self.config = json.load(file)

    def load_accounts(self):
        """Initializes self.accounts[] from the config.json and corresponding account .csv"""
        for name in self.config["accounts"].keys():
            acc_type = self.config["accounts"][name]
            df = pd.read_csv(self.path + name + ".csv")
            self.accounts[name] = Account(name, acc_type, df)
    
    def create_account(self, name: str, acc_type: str):
        """Creates an account with a name and type; creates new .csv file and updates config (changes saved)"""
        acc_type = acc_type.upper()

        if acc_type not in [e.name for e in AccType]: # if account type is invalid
            raise AccountTypeInvalidError(f"Account type is invalid.")
        elif os.path.exists(self.path + name) or name in self.accounts.keys(): # if account already exists
            raise AccountExistsError(f"Account '{name}' already exists.")
        else:
            with open(self.path + name + ".csv", mode="w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Description", "Amount"])

            self.config["accounts"][name] = acc_type
            self.update_config_file()
            self.load_accounts()
            
    def delete_account(self, name:str):
        """(not implemented) Deletes account from 1. .csv file, 2. self.config. Updates config file and reinitializes accounts"""
        pass

    def write_transaction(self, date:datetime, description:str, entries:list[tuple[str,Decimal]]):
        """Validates and writes a transaction to the corresponding set of accounts given in entries. entries = [(account_name, amount)]Raises exception if any input is invalid"""
        
        validate_transaction(date, description, entries, self.accounts) # will raise exception if errors found
        
        for entry in entries:
            self.accounts[entry[0]].write_transaction(description, entry[1], date)

    def save_changes(self):
        """Saves changes in accounts' .csv"""
        for account in self.accounts.values():
            account.save_changes(self.path)

    def update_config_file(self):
        """Updates config.json file with new changes to self.config[]. To be called every time accounts are added or deleted"""
        with open(self.path + "config.json", "w") as file:
            json.dump(self.config, file, indent=4)

    def __str__(self):
        result = f"Ledger: {self.config['name']} \n"

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