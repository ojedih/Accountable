from datetime import datetime
import pandas as pd
from enum import Enum

class AccType(Enum):
    ASSET = 'ASSET'
    LIABILITY = 'LIABILITY'
    INCOME = 'INCOME'
    EXPENSE = 'EXPENSE'

class Account:
    def __init__(self, name, acc_type, transactions):
        self.name: str = name
        self.acc_type: AccType = acc_type
        self.df: pd.DataFrame = transactions

    def write_transaction(self, description, amount, date):
        self.df.loc[len(self.df)] = [date.date(), description, amount]
        print(self.df)

    def delete_transaction(self, idx):
        if idx in self.df.index:
            self.df = self.df.drop([idx])
            print(f"Deleted entry at index {idx}")
        else:
            print(f"Couldn't find entry at {idx} to delete")

    def save_changes(self, path):
        try:
            self.df.to_csv(path + self.name + ".csv", index=False)
        except Exception as e:
            raise Exception(f"[Account:save_changes] Error: {e}")

    def __str__(self):
        return str(self.df)


    
#df = pd.read_csv("ledger/testledger/checking.csv")
#last_index = df.index[-1]
#g = Account("checking", AccType.ASSET, df)
#print(df)

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