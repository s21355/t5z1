import unittest
import math
from main import statement


class TestStatement(unittest.TestCase):
    def setUp(self):
        self.invoice = {
            "customer": "BigCo",
            "performances": [
                {"playID": "hamlet", "audience": 55},
                {"playID": "as-like", "audience": 35},
                {"playID": "othello", "audience": 40},
            ],
        }
        self.plays = {
            "hamlet": {"name": "Hamlet", "type": "tragedy"},
            "as-like": {"name": "As You Like It", "type": "comedy"},
            "othello": {"name": "Othello", "type": "tragedy"},
        }

    def test_tragedy_calculation(self):
        self.invoice["performances"] = [{"playID": "hamlet", "audience": 40}]
        result = statement(self.invoice, self.plays)
        self.assertEqual(result, "Statement for BigCo\n Hamlet: $500.00 (40 seats)\nAmount owed is $500.00\nYou earned 10 credits\n")

        self.invoice["performances"] = [{"playID": "hamlet", "audience": 55}]
        result = statement(self.invoice, self.plays)
        self.assertEqual(result, "Statement for BigCo\n Hamlet: $650.00 (55 seats)\nAmount owed is $650.00\nYou earned 25 credits\n")


    def test_comedy_calculation(self):
        self.invoice["performances"] = [{"playID": "as-like", "audience": 20}]
        result = statement(self.invoice, self.plays)
        self.assertEqual(result,
                         "Statement for BigCo\n As You Like It: $360.00 (20 seats)\nAmount owed is $360.00\nYou earned 4 credits\n")

        self.invoice["performances"] = [{"playID": "as-like", "audience": 30}]
        result = statement(self.invoice, self.plays)
        self.assertEqual(result,
                         "Statement for BigCo\n As You Like It: $540.00 (30 seats)\nAmount owed is $540.00\nYou earned 6 credits\n")

    def test_volume_credits(self):
        self.invoice["performances"] = [
            {"playID": "hamlet", "audience": 40},
            {"playID": "as-like", "audience": 30},
            {"playID": "othello", "audience": 40},
        ]
        total_amount = 0
        volume_credits = 0
        for perf in self.invoice['performances']:
            play = self.plays[perf['playID']]
            if play['type'] == "tragedy":
                this_amount = 40000
                if perf['audience'] > 30:
                    this_amount += 1000 * (perf['audience'] - 30)
            elif play['type'] == "comedy":
                this_amount = 30000
                if perf['audience'] > 20:
                    this_amount += 10000 + 500 * (perf['audience'] - 20)
                this_amount += 300 * perf['audience']
            volume_credits += max(perf['audience'] - 30, 0)
            if "comedy" == play["type"]:
                volume_credits += math.floor(perf['audience'] / 5)
            total_amount += this_amount
        result = statement(self.invoice, self.plays)
        self.assertEqual(result, "Statement for BigCo\n Hamlet: $500.00 (40 seats)\n As You Like It: $540.00 (30 seats)\n Othello: $500.00 (40 seats)\nAmount owed is ${:0,.2f}\nYou earned {} credits\n".format(total_amount/100,volume_credits))

if __name__ == '__main__':
    unittest.main()

