import unittest
from model.Ledger import Ledger
from model.Account import Account, AccType

l1 = Ledger("ledger/testledger/")

entries_all_correct1 = [("checking", -10), ("credit", -10)]
entries_all_correct2 = [("credit", 10), ("expenses", 10)]
entries_all_correct3 = [("checking", -10), ("credit", 10), ("expenses", 20)]
entries_wrong_account_names = [("credit", 10), ("expense", 10)]
entries_wrong_tally = [("checking", -10), ("credit", 10), ("expenses", 10)]

class TestLedger(unittest.TestCase):
    def test_validate_entries(self):
        self.assertTrue(l1.validate_entries(entries_all_correct1))
        self.assertTrue(l1.validate_entries(entries_all_correct2))
        self.assertTrue(l1.validate_entries(entries_all_correct3))
        self.assertFalse(l1.validate_entries(entries_wrong_account_names))
        self.assertFalse(l1.validate_entries(entries_wrong_tally))

l1.createAccount("checking", AccType.ASSET)
l1.createAccount("credit", AccType.LIABILITY)
l1.createAccount("expenses", AccType.EXPENSE)
l1.createAccount("income", AccType.INCOME)

if __name__ == "__main__":
    unittest.main()