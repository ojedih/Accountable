import json
import pandas as pd

from model.Account import Account, AccType

# Reads and Writes data from/to the ledger filesystem.
class LedgerFileManager:
    def __init__(self, path):
        self._path: str = path
        self._config = {}
        self._new_accounts: list[Account] = []

        self._load_config()
    
    def get_ledger_name(self):
        """Returns the name of the ledger from config.json"""
        return self._config["name"]
    
    def get_accounts(self) -> dict[str, Account]:
        """Returns a pupulated accounts dict from the file system. Requires config.json to be loaded (constructor does it)""" 
        accounts = {}
        for acc_type in self._config["accounts"].keys():
            for acc_name in self._config["accounts"][acc_type]:
                df = pd.read_csv(self._path + acc_type + "/" + acc_name + ".csv") # ledger_path/account_type/account_name.csv
                accounts[acc_name] = Account(acc_name, AccType(acc_type), df)        
        return accounts
    
    def commit_new_account(self, account):
        """Commits a new account to be added later to config and file system if changes are saved"""
        self._new_accounts.append(account)

    def save_changes(self, accounts: dict[str, Account]):
        """Saves all changes to file system. Creates new files for newly created accounts. Updates config file."""
        self._save_new_accounts_to_config()
        self._save_account_changes(accounts)
        self._save_config()

    def _load_config(self):
            """Loads self.config from the config.json file"""
            with open(self._path + "config.json", "r") as file:
                self._config = json.load(file)

    def _save_new_accounts_to_config(self):
        """Creates and populates a .csv file with the new account info AND adds their name to _config"""
        while len(self._new_accounts) > 0:
            new_account = self._new_accounts.pop()
            self._config["accounts"][new_account.acc_type.value].append(new_account.name)

    def _save_account_changes(self, accounts: dict[str, Account]):
        """Saves and commits account changes to the file system"""
        for account in accounts.values():
            account.entries.to_csv(self._path + account.acc_type.value + "/" + account.name + ".csv", index=False) # ledger_path/account_type/account_name.csv

    def _save_config(self):
        """Saves config.json file with new changes to _config."""
        with open(self._path + "config.json", "w") as file:
            json.dump(self._config, file, indent=4)



