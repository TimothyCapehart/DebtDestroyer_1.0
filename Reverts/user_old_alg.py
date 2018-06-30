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

    def check_payoff(self):
        diff = self.calc_diff()
        found = False
        for account in self.accounts:
            if account.balance <= diff:
                found = True
        return found

    def reset_payments(self):
        for account in self.accounts:
            account.payment = 0.0

    # MAKE A FUNCTION TO PAYOFF A LOAN IF POSSIBLE AFTER PAYING ALL OTHER MINIMUMS

    def payoff(self) -> float:  # pre: self.apply_all_accrued(), self.apply_all_mins(), self.check_payoff == True
        if self.ammo == 0.0:
            raise Exception()

        if len(self.accounts) == 0:
            raise Exception()

        total_min = self.get_total_min()
        if total_min > self.ammo:
            raise Exception()
        total_paid = self.get_total_paid()
        diff = self.ammo - total_paid
        self.sort_accounts()
        for account in self.accounts:
            if account.balance <= diff:
                account.payment += account.balance
                total_paid += account.balance
                diff -= account.balance
                account.balance = 0.0
                account.calc_daily()
                break
            return float(diff)

    def update(self, diff):

        diff = float(diff)

        if self.ammo == 0.0:
            raise Exception()

        if len(self.accounts) == 0:
            raise Exception()

        total_min = self.get_total_min()
        if total_min > self.ammo:
            raise Exception()
        #diff = 0.0
        self.sort_accounts()
        if diff == 0.0:
            total_diff = self.ammo - total_min
            total_paid = self.get_total_paid()

            #for account in self.accounts:
             #   if account.balance <= total_diff:
              #      account.payment += account.balance
               #     account.balance = 0.0

            for i, account in enumerate(self.accounts):
                if i == 0:
                    target_amount = self.ammo - total_min + account.min
                    if account.balance >= target_amount:
                        account.payment += target_amount
                        total_paid += target_amount
                        account.balance -= target_amount
                        account.calc_daily()
                    else:
                        account.payment += account.balance
                        total_paid += account.balance
                        account.balance = 0.0
                        account.calc_daily()
                else:
                    if account.balance >= account.min:
                        account.balance -= account.min
                        account.payment += account.min
                        total_paid += account.min
                        account.calc_daily()
                    else:
                        account.payment += account.balance
                        total_paid += account.balance
                        account.balance = 0.0

            if total_paid < self.ammo:
                diff = self.ammo - total_paid
                more = 0
                self.sort_accounts()
                for i, account in enumerate(self.accounts):
                    if i == 0:
                        if account.balance >= diff:
                            account.balance -= diff
                            account.payment += diff
                            account.calc_daily()
                        else:
                            diff -= account.balance
                            account.payment += account.balance
                            account.balance = 0.0
                            account.calc_daily()
                            more = 1
                    else:
                        if more == 1:
                            if account.balance >= diff:
                                account.balance -= diff
                                account.payment += diff
                                account.calc_daily()
                                more = 0
                            else:
                                diff -= account.balance
                                account.payment += account.balance
                                account.balance = 0.0
                                account.calc_daily()
                                more = 1
                        else:
                            return
            self.sort_accounts()

        else:
            total_diff = diff
            ###
            total_paid = self.get_total_paid()

            for account in self.accounts:
                if account.balance <= total_diff:
                    account.payment += account.balance
                    total_paid += account.balance
                    total_diff -= account.balance
                    account.balance = 0.0
                    account.calc_daily()

                else:
                    account.balance -= total_diff
                    account.payment += total_diff
                    total_paid += total_diff
                    total_diff = 0.0
                    account.calc_daily()
                    break

            if total_diff > 0.0:
                self.sort_accounts()
                for account in self.accounts:
                    if account.balance >= total_diff:
                        account.balance -= total_diff
                        total_paid += total_diff
                        total_diff = 0.0
                        break
                return

    def report(self):
        done = 0
        month = 1
        diff = float(0.0)

        print("\nMonth " + str(month))
        try:
            self.apply_all_accrued()
        except:
            print("Error")
            return "Error"

        #if self.check_payoff():
         #   self.apply_all_mins()
          #  diff = self.payoff()
        try:
            self.update(diff)
        except:
            print("Error")
            return "Error"
        self.print()
        self.reset_payments()
        while done == 0:
            month += 1
            print("\nMonth " + str(month))
            diff = float(0.0)
            self.apply_all_accrued()
            #if self.check_payoff():
             #   self.apply_all_mins()
              #  diff = self.payoff()
               # self.sort_accounts()
            self.update(diff)
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
                "Account: " + account.name + "\tBalance: " + "%8.2f" % account.balance
                + "\tAPR: " + "%5.2f" % account.apr + "\tMin: " + "%5.2f" % account.min +
                "\tPayment: " + "% 8.2f" % account.payment + "\tD_Int: " + "%4.2f" % account.dailyInterest)

