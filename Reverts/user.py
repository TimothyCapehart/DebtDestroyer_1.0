class User:
    accounts = []
    ammo = 0.0

    def __init__(self):
        self.accounts = []
        self.ammo = 0.0

    def set_u_ammo(self, amount):
        self.ammo = amount

    def get_ammo(self):
        return self.ammo

    def sort_accounts(self):
        for account in self.accounts:
            account.calc_daily()
        self.accounts.sort(key=lambda x: x.get_daily(), reverse=True)

    def get_total_min(self):
        total = 0.0
        for account in self.accounts:
            total += account.min
        return total

    def get_total_paid(self):
        paid = 0.0
        for account in self.accounts:
            paid += account.payment
        return paid

    def calc_diff(self):
        diff = 0.0
        self.ammo - self.get_total_paid()
        return diff

    def apply_all_accrued(self):
        if len(self.accounts) == 0:
            raise Exception()

        for account in self.accounts:
            account.apply_accrued()

    def apply_all_mins(self):
        for account in self.accounts:
            if account.balance >= 0.0:
                account.balance -= account.min
                account.payment = account.min

    def reset_payments(self):
        for account in self.accounts:
            account.payment = 0.0

    def update(self):
        if self.ammo == 0.0:
            raise Exception()

        if len(self.accounts) == 0:
            raise Exception()

        ammo = self.ammo
        total_min = self.get_total_min()
        if total_min > self.ammo:
            raise Exception()

        self.sort_accounts()
        total_paid = self.get_total_paid()
        total_daily = 0.0
        for account in self.accounts:
            total_daily += account.dailyInterest

        for account in self.accounts:
            payment = account.dailyInterest/total_daily * self.ammo
            if payment < account.min:
                payment = account.min
            if ammo < payment:
                x = payment - ammo
                for acc in self.accounts:
                    if acc.payment > x:
                        acc.payment -= x
                        acc.balance += x
                        total_paid -= x
                        ammo += x
                        break

            if payment >= account.balance:
                account.payment += account.balance
                total_paid += account.balance
                ammo -= account.balance
                account.balance = 0.0
                account.calc_daily()
            else:
                account.payment += payment
                total_paid += payment
                ammo -= payment
                account.balance -= payment
                account.calc_daily()
        if ammo > 0.0:
            self.sort_accounts()
            for account in self.accounts:
                if account.balance >= ammo:
                    account.payment += ammo
                    total_paid += ammo
                    account.balance -= ammo
                    account.calc_daily()
                    break
        self.sort_accounts()

    def report(self):
        done = 0
        month = 1
        print("\nMonth " + str(month))
        try:
            self.apply_all_accrued()
        except:
            print("Error")
            return "Error"
        try:
            self.update()
        except:
            print("Error")
            return "Error"
        self.print()
        self.reset_payments()
        while done == 0:
            month += 1
            print("\nMonth " + str(month))
            self.apply_all_accrued()
            self.update()
            self.print()
            self.reset_payments()
            self.sort_accounts()
            for i, account in enumerate(self.accounts):
                if i == 0:
                    if account.balance == 0.0:
                        done = 1

    def print(self):
        self.sort_accounts()
        for account in self.accounts:
            print(
                "Account: " + account.name + "\t\tBalance: " + "%8.2f" % account.balance
                + "\tAPR: " + "%5.2f" % account.apr + "\tMin: " + "%5.2f" % account.min +
                "\tPayment: " + "% 8.2f" % account.payment + "\tD_Int: " + "%4.2f" % account.dailyInterest)

