import os
import csv
import json
import pandas as pd
from datetime import datetime
from model.Account import Account, AccType

class Ledger:
    def __init__(self, path):
        self.path = path
        self.config = {}
        self.accounts = {}
                
        self.loadConfig()
        self.initAccounts()
            
    def loadConfig(self): # loads config.json file into self.config
        try:
            with open(self.path + "config.json", "r") as file:
                self.config = json.load(file)
            print(f"Ledger {self.config['name']} initialized!")
        except Exception as e:
            raise FileNotFoundError(f"Error loading config.json: {e}")

    def initAccounts(self): # initializes self.accounts[] from the config.json and corresponding .csv
        try:
            for name in self.config["accounts"].keys():
                acc_type = self.config["accounts"][name]
                df = pd.read_csv(self.path + name + ".csv")
                self.accounts[name] = Account(name, acc_type, df)

            print(f"Accounts initialized: {self.accounts}")
        except Exception as e:
            raise RuntimeError(f"Error initializing accounts: {e}")
    
    def createAccount(self, name, type): # Creates an account with a name and type; creates new .csv file and updates config 
        if not os.path.exists(self.path + name) and not name in self.config["accounts"]:
            try:
                with open(self.path + name + ".csv", mode="w", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Date", "Description", "Amount"])

                self.config["accounts"][name] = str(type)
                self.updateConfigFile()
                
                print(f"New Account {name} Created")
            except Exception as e:
                print(f"Error while creating account: {e}")
        else:
            print(f"Error, account {name} already exists")

    def deleteAccount(self, name): # deletes account from 1. .csv file, 2. self.config. Updates config file and reinitializes accounts
        pass

    def validate_transaction(self, date, description, entries): # validates a transaction with a date, description, and entries
        result = True

        result = self.validate_date(date)
        result = self.validate_description(description)
        result = self.validate_entries(entries)

        if result:
            for entry in entries:
                self.writeTransaction(self, entry[0], description, entry[1], date)
            print("Transaction sucessfully commited. Changes are not saved yet.")
        else:
            print("Transaction failed.")
                
    def validate_date(self, date):
        if date > datetime.now():
            print("Date can't be in the future")
            return False
        return True
    
    def validate_description(self, description):
        if len(description) == 0:
            print("Description can't be empty")
            return False
        return True
    
    def validate_entries(self, entries):
        tally = 0
        
        for entry in entries:
            acc_name = entry[0]
            amount = entry[1]

            if acc_name not in self.accounts.keys():
                print(f"Account {acc_name} doesn't exist")
                return False
            else:
                acc_type = self.accounts[acc_name].type

                match acc_type: # Follows the accounting identity ASSETS = LIABILITIES + INCOME - EXPENSES.
                    case AccType.ASSET:
                        tally += amount
                    case AccType.LIABILITY:
                        tally -= amount
                    case AccType.INCOME:
                        tally -= abs(amount)
                    case AccType.EXPENSE:
                        tally += abs(amount)

        if tally == 0:
            return True
        
        print("Entries amounts don't tally")
        return False
    
    def writeTransaction(self, account_name, description, amount, date): # writes a transaction to an account
        self.accounts[account_name].writeTransaction(description, amount, date)

    def updateConfigFile(self):
        with open(self.path + "config.json", "w") as file:
            json.dump(self.config, file, indent=4)
        print("Config file updated")



    
