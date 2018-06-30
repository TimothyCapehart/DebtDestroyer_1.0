class Account:
    name = ""
    balance = 0.0
    apr = 0.0
    min = 0.0
    dailyInterest = 0.0
    payment = 0.0
    accrued = 0.0

    def __init__(self, name, balance, apr, min):
        self.name = name
        self.balance = balance
        self.apr = apr
        self.min = min

    def calc_daily(self):
        self.dailyInterest = (float(self.balance) * float(self.apr)/100)/365

    def set_payment(self, payment):
        self.payment = payment

    def get_daily(self):
        return self.dailyInterest

    def apply_accrued(self):
        self.calc_daily()
        self.accrued = self.dailyInterest * 30
        self.balance = self.balance + self.accrued
