from datetime import datetime
import pandas as pd
from enum import Enum
from decimal import Decimal, ROUND_HALF_UP

class AccType(Enum):
    ASSET = 'ASSET'
    LIABILITY = 'LIABILITY'
    INCOME = 'INCOME'
    EXPENSE = 'EXPENSE'

# An account has a name and type and stores entries in a pandas dataframe. 
# Entries have a date, description, and amount. The amount is a Decimal and can be positive or negative.
class Account:
    def __init__(self, name, acc_type: AccType, entries = pd.DataFrame(columns=["date", "description", "amount"])):
        self.name: str = name
        self.acc_type: AccType = acc_type
        self.entries: pd.DataFrame = entries

    def write_transaction(self, description:str, amount:Decimal, date:datetime):
        """Writes a transaction to the account. Expects validated input"""
        self.entries.loc[len(self.entries)] = [date.date(), description, amount]

    def delete_transaction(self, idx):
        """Deletes a transaction at specified index"""
        self.entries = self.entries.drop([idx])

    def get_balance(self):
        balance = self.entries['amount'].sum()
        balance = Decimal(str(balance))
        return balance.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def __str__(self):
        return str(self.entries)


    
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