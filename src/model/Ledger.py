import os
import csv
import json
import pandas as pd
from model.Account import Account

class Ledger:
    def __init__(self, path):
        self.path = path
        self.config = {}
        self.accounts = {}
        
        try:
            self.loadConfig()
            self.initAccounts()
        except Exception as e:
            print(f"Error initializing ledger: {e}")

    def loadConfig(self):
        with open(self.path + "config.json", "r") as file:
            self.config = json.load(file)
            print(f"Ledger {self.config['name']} initialized!")

    def initAccounts(self):
        for name in self.config["accounts"].keys():
            type = self.config["accounts"][name]
            df = pd.read_csv(self.path + name + ".csv")
            self.accounts[name] = Account(name, type, df)

        print(f"Accounts initialized: {self.accounts}")
    
    def createAccount(self, name, type):
        if not os.path.exists(self.path + name) and not name in self.config["accounts"]:
            try:
                with open(self.path + name + ".csv", mode="w", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Date", "Description", "Amount"])

                self.config["accounts"][name] = str(type)
                
                with open(self.path + "config.json", "w") as file:
                    json.dump(self.config, file, indent=4)
                
                print(f"New Account {name} Created")
            except Exception as e:
                print(f"Error while creating account: {e}")
        else:
            print(f"Error, account {name} already exists")

    def deleteAccount(self, name):
        pass

    def writeTransaction(self, account, description, amount, date):
        pass




l = Ledger("ledger/alejandro/")



    
