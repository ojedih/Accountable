import os
import json
from pathlib import Path

class MainFileManager:
    def __init__(self, ledgers_dir):
        self.ledgers_dir = ledgers_dir

    def create_new_ledger(self, name):
        if not os.path.isdir(self.ledgers_dir + name): # check if directory exists
            os.makedirs(self.ledgers_dir + name) # create directories
            os.makedirs(self.ledgers_dir + name + "/ASSET")
            os.makedirs(self.ledgers_dir + name + "/LIABILITY")
            os.makedirs(self.ledgers_dir + name + "/INCOME")
            os.makedirs(self.ledgers_dir + name + "/EXPENSE")
            
            with open(self.ledgers_dir + name + "/config.json", mode="w", newline='') as file: # create file
                init_config = { # base config structure
                    'name': name,
                    'accounts': {
                        "ASSET": [],
                        "LIABILITY": [],
                        "INCOME": [],
                        "EXPENSE": []
                    }
                }
                json.dump(init_config, file, indent=4)
        else:
            raise FileExistsError(f"Ledger {name} already exists")
        
    def get_ledger_names(self):
        return [folder.name for folder in Path(self.ledgers_dir).iterdir() if folder.is_dir()]
    
    def get_ledger_dir(self):
        return self.ledgers_dir