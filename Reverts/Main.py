import tkinter as tk
from tkinter import ttk
from account import Account
from user import User

LARGE_FONT = ("Verdana", 12)


class DebtDestroyer(tk.Tk):
    user = User()

    def __init__(self, *args, **kwargs):
        super(DebtDestroyer, self).__init__()
        tk.Tk.wm_title(self, "Debt Destroyer")
        container = tk.Frame(self)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        super(StartPage, self).__init__()
        # tk.Frame__init__(self, parent)
        label = tk.Label(self, text="Debt DESTROYER", font=LARGE_FONT)
        label.grid(row=0, column=2, pady=10, padx=30, sticky="nsew")

        def set_ammo(self, *args):
            DebtDestroyer.user.set_u_ammo(in_ammo.get())
            print("$" + str(DebtDestroyer.user.get_ammo()) + " LOADED")

        def d_report(self, *args):
            DebtDestroyer.user.report()
            print("DESTROYED")

        in_ammo = tk.DoubleVar()

        ammo_label = tk.Label(self, text=" Ammo ")
        ammo_label.grid(row=1, column=1, pady=50, sticky="E")
        ammo_entry = tk.Entry(self, textvariable=in_ammo)
        ammo_entry.grid(row=1, column=2, columnspan=1)

        ammo_button = tk.Button(self, text="Load")
        ammo_button.bind("<Button-1>", set_ammo)
        ammo_button.grid(row=1, column=3)

        button1 = ttk.Button(self, text="Add Accounts",
                            command=lambda: controller.show_frame(PageOne))
        button1.grid(row=2, column=2)

        button2 = tk.Button(self, text="***DESTROY***")
        button2.bind("<Button-1>", d_report)
        button2.grid(row=3, column=2, pady=10)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        super(PageOne, self).__init__()
        label = tk.Label(self, text="Account Info", font=LARGE_FONT)
        label.grid(row=0, column=1, pady=15, padx=30, sticky="nsew")

        def get_data(*args):
            new = Account(name.get(), float(balance.get()), float(apr.get()), float(min.get()))
            new.calc_daily()
            DebtDestroyer.user.accounts.append(new)
            DebtDestroyer.user.sort_accounts()
            print("\nAccounts: " + str(len(DebtDestroyer.user.accounts)))
            for account in DebtDestroyer.user.accounts:
                print(
                    "Account: " + account.name + "\nBalance: " + "%.2f" % account.balance
                    + "\nAPR: " + str(account.apr) + "\nMin: " + str(account.min) +
                    "\nD_Int: " + "%.2f" % account.dailyInterest + "\n\n")
            name.set("Next")
            balance.set(0.0)
            apr.set(0.0)
            min.set(0.0)

        name = tk.StringVar()
        balance = tk.DoubleVar()
        apr = tk.DoubleVar()
        min = tk.DoubleVar()
        name.set("Name")
        balance.set(0.0)
        apr.set(0.0)
        min.set(0.0)

        label_1 = tk.Label(self, text=" Name ")
        label_1.grid(row=2, sticky="E")
        name_entry = tk.Entry(self, textvariable=name)
        name_entry.grid(row=2, column=1, columnspan=3)

        label_2 = tk.Label(self, text=" Balance ")
        label_2.grid(row=3, sticky='E')
        balance_entry = tk.Entry(self, textvariable=balance)
        balance_entry.grid(row=3, column=1, columnspan=3)

        label_3 = tk.Label(self, text=" APR %")
        label_3.grid(row=4, sticky='E')
        apr_entry = tk.Entry(self, textvariable=apr)
        apr_entry.grid(row=4, column=1)

        label_4 = tk.Label(self, text=" Minimum ")
        label_4.grid(row=5, sticky='E')
        min_entry = tk.Entry(self, textvariable=min)
        min_entry.grid(row=5, column=1)

        getDataButton = tk.Button(self, text="Add Account")
        getDataButton.bind("<Button-1>", get_data)
        getDataButton.grid(row=6, column=1, pady=15)

        button2 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button2.grid(row=9, column=1)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        super(PageTwo, self).__init__()
        label = ttk.Label(self, text="Page Two", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()


app = DebtDestroyer()
app.geometry("300x300")
app.mainloop()