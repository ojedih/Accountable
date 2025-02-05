
import os
from datetime import datetime
import pandas as pd

FOLDER_PATH = "ledger/alejandro/"

class AccType:
    ASSET = 'ASSET'
    LIABILITY = 'LIABILITY'
    INCOME = 'INCOME'
    EXPENSE = 'EXPENSE'

class Account:
    def __init__(self, name, type, transactions):
        self.name = name
        self.type = type
        self.df = transactions

    def writeTransaction(self, desc, amount, date):
        pass

    def deleteTransaction(self, idx):
        if idx in self.df.index:
            self.df = self.df.drop([idx])
            print(f"Deleted entry at index {idx}")
        else:
            print(f"Couldn't find entry at {idx} to delete")

    def __str__(self):
        return str(self.df)

    

#g = Account("checking", AccType.ASSET)

#g.readEntries('2025-01-21')
#g.deleteEntry('2025-01-23')


# Read the CSV file into a DataFrame
#df = pd.read_csv(self.path)
#print(df)

#df['Date'] = pd.to_datetime(df['Date'])

# Filter rows where the Date is greater than or equal to the given start_date
#filtered_df = df[df['Date'] >= pd.to_datetime(start_date)]

# Display the result
#print(filtered_df)