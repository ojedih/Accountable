import unittest
from model.Ledger import Ledger
from model.Account import Account, AccType

l1 = Ledger("ledger/testledger/")

l1.createAccount("checking", AccType.ASSET)
l1.createAccount("credit", AccType.LIABILITY)
l1.createAccount("expenses", AccType.EXPENSE)
