import csv
import os
from datetime import datetime
import pandas as pd

FOLDER_PATH = "ledger/alejandro/"

class AccType:
    ASSET = 'ASSET'
    LIABILITY = 'LIABILITY'
    IND_EQUITY = 'IND EQUITY'

class Account:
    def __init__(self, name, type, path = None):
        self.name = name
        self.type = type
        
        if path == None:
            self.path = FOLDER_PATH + name + ".csv"
        else:
            self.path = path
        
        self.initialize_csv()

    def initialize_csv(self):
        if not os.path.exists(self.path):
            with open(self.path, mode="w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Description", "Category", "Amount"])
                print("New Account Created")
        
        print(f"Account {self.name} initialized")

    def writeEntry(self, desc, category, amount, date=datetime.today().strftime("%m-%d-%Y")):
        with open(self.path, mode="a") as ledger:
            writer = csv.writer(ledger, delimiter=',', quotechar='"')
            writer.writerow([date, desc, category, amount])

        print(f"Entry added to Account {self.name}")

    def deleteEntry(self, idx):
        df = pd.read_csv(self.path)

        if idx in df.index:
            df = df.drop([idx])
            df.to_csv(self.path, index=False)
            print(f"Deleted entry at index {idx}")
        else:
            print(f"Couldn't find entry at {idx} to delete")

    def readEntries(self, start_date):
        # Read the CSV file into a DataFrame
        df = pd.read_csv(self.path)
        #print(df)

        df['Date'] = pd.to_datetime(df['Date'])

        # Filter rows where the Date is greater than or equal to the given start_date
        filtered_df = df[df['Date'] >= pd.to_datetime(start_date)]

        # Display the result
        print(filtered_df)

        # Set 'Date' as the index
        #df.set_index('Date', inplace=True)

        # Group by the Date index and display each group
        #grouped = df.groupby(df.index)

        # Display the grouped rows
        #for _, group in grouped:
        #   print(group)
        #   print("-" * 70)  # Separator between groups

    

g = Account("checking", AccType.ASSET)

g.readEntries('2025-01-21')
g.deleteEntry('2025-01-23')