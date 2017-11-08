import random

class Bank():

    no_of_banks = 0

    def __init__(self, name, location):
        self.id = Bank.no_of_banks + 1
        self.name = name
        self.location = location
        self.accounts = {}
        self.customers = {}
        self.tellers = {}
        self.loans = {}

        Bank.no_of_banks += 1
    def bank_details(self):
        print("/n BANKID: ",self.id,"/n NAME: ",self.name,
              "/n LOCATION: ",self.location)

class Teller():

    no_of_tellers = 0

    def __init__(self, name, bank):
        self.id = Teller.no_of_tellers + 1
        self.name = name
        self.bank = bank
        self.bank.tellers.update({self.id:self})
        Teller.no_of_tellers += 1
    def teller_info(self):
        print("/n TELLERID: ",self.id, "/n NAME: ",self.name,
              "/n BANK ",self.bank)

    def collect_money(self, account_id, amount):
        current_amount = self.bank.accounts[account_id]
        self.bank.accounts[account_id] = current_amount + amount
        
    def open_account(self, customer, account_type, amount):
        if account_type.lower() in ["savings", "checking"]:
            if not customer.id in self.bank.customers:
                self.bank.customers.update({customer.id:customer})

            if account_type.lower() == "savings":
                account = SavingsAccount(customer.id, amount)
                self.bank.accounts.update({account.id:account})
                return account.id
            else:
                account = CheckingAccount(customer.id, amount)
                self.bank.accounts.update({account.id: account})
                return account.id

        else:
            raise Exception("Invalid Account type")

    def close_account(self, account_id):
        del self.bank.accounts[account_id]

    def loan_request(self, customer, loan_type, amount):
        if not loan_type.lower() in ["short", "long"]:
            raise Exception("Invalid Loan Type")
        message = None
        if loan_type.lower() == "short":
            if amount < 100000:
                raise Exception("Minimum allowed short term loan is UGX 100,000.")
        if amount < 500000:
            raise Exception("Minimum allowed long term loan is UGX 500,000.")

        current_balance = self.bank.accounts[customer.account_id].account_balace
        if current_balance > 0.25*amount:
            loan = Loan(loan_type.lower(), customer.id, amount)
            self.bank.loans.update({loan.id:loan})
            return loan.id
        else:
            raise Exception("You must have at least a quarter of the loan amount in your account")

    def provide_info(self, customer):
        return str("-"*40 + "\n{} Customer Information\n".format(self.bank.name)) +  \
            str(("="*40 + "\nName: {}\nAccount Type: {}\nAccount Number: {}\nAccount Balance: {}\n" + "-"*40 + "\n\n").format(customer.name,self.bank.accounts[customer.account_id].type, self.bank.accounts[customer.account_id].account_no, self.bank.accounts[customer.account_id].account_balance))

    def issue_card(self, customer):
        print("Issuing card to", customer.name)



class Customer(Bank):
    AccountBal = 0
    LoanAmt = 0
    def __init__(self,Name,Address,PhoneNo,AcctNo):

        self.Name = Name
        self.Address = Address
        self.PhoneNo = PhoneNo
        self.AcctNo = AcctNo

    def detail(self):
        print("-"*60,
              "\n        NAME:",self.Name,
              "\n        ADDRESS:",self.Address,
              "\n        PHONE NO:",self.PhoneNo,
              "\n        AC\\NO:",self.AcctNo+"\n"+"-"*60
              )

    def general_inquiry(self, teller):
        return teller.provide_info(self)

    def deposit_money(self, teller, account_id, amount):
        teller.collect_money(account_id, amount, "deposit")

    def withdraw_money(self, teller, account_id, amount):
        pass

    def open_account(self, teller, account_type, initial_amount):
        self.account_id = teller.open_account(self, account_type, initial_amount)

    def close_account(self, teller, account_id):
        teller.close_account(self.account_id)
        self.account_id = None

    def apply_for_loan(self, teller, loan_type, amount):
        teller.loan_request(self, loan_type, amount)

    def request_card(self, teller):
        print("Requesting Card...")
        teller.issue_card(self)

class Account():

    no_of_accounts = 0
    account_nos = []

    def __init__(self, customer_id, amount, acc_type):
        self.id = Account.no_of_accounts + 1
        self.customer_id = customer_id
        self.account_balance = amount
        self.account_no = None
        self.type = acc_type
        while True:
            x = random.randint(1000000000,9999999999)
            if not x in Account.account_nos:
                self.account_no = x
                Account.account_nos.append(self.account_no)
                break
        Account.no_of_accounts += 1


class CheckingAccount(Account):
    def __init__(self, customer_id, amount):
        super(customer_id, amount, self).__init__("Checking")

class SavingsAccount(Account):
    def __init__(self, customer_id, amount):
        super(customer_id, amount, self).__init__("Savings")

class Loan():

    no_of_loans = 0

    def __init__(self, loan_type, customer_id, amount):
        self.id = Loan.no_of_loans + 1
        self.loan_type = loan_type
        self.amount = amount
        self.customer_id = customer_id
        self.rate = None
        self.time_period = None
        self.frequency = None
        self.payment = None

        if loan_type.lower() == "short":
            self.rate = 0.2
            self.time_period = 1
            self.frequency = self.amount // 12
            self.payment = self.amount + (self.amount * self.rate * self.time_period)

        else:
            self.rate = 0.1
            self.time_period = 6
            self.frequency = self.amount // 6
            self.payment = self.amount + (self.amount * self.rate * self.time_period)

        Loan.no_of_loans += 1

        def __str__(self):
            return "="*40 + \
                self.loan_type.title()
        
#banks 1 and 2    
B1 = Bank("bank 001","Mbarara")
B2 = Bank("bank 002","Masaka") 

#details of bank 1 and 2
B1.bank_details() 
B2.bank_details() 

# BANK 1 TELLERS
B1_T1 = Teller("Kirabo Sophie",B1)
B1_T2 = Teller("Nagaba Catherine",B1)
B1_T3 = Teller("Kansiime Racheal",B1)

B1_T1.teller_info()
B1_T2.teller_info()
B1_T3.teller_info()

# BANK 2 TELLERS
B2_T1 = Teller("Nyangoma Immaculate",B2)
B2_T2 = Teller("Namaganda Christine",B2)
B2_T3 = Teller("Amanya Juliet",B2)

B2_T1.teller_info()
B2_T2.teller_info()
B2_T3.teller_info()



### CUSTOMERS BANK 1
print("CUSTOMERS of ",B1.name,"\n","_"*40)
CS_B1 = [
    Customer("Nakyeyune Ruth","Kamwokya","0772525667","102458"),
    Customer("Kijjambu Henry","Lumumba RM 100","0778278782","100254"),
    Customer("Okwii Allan","Kavule","0786678096","102356"),
    Customer("Mujuzi Elisha","hostel RM 27","0757707933","124581"),
    Customer("Munye Ben ","hostel RM 13","0784537658","156874"),
    Customer("Kabasita Dorothy","Livinstone RM 253","0784525606","145789"),
    Customer("Tweteise Peter","hostel RM 15","0754525136","467753"),
    Customer("Natukunda Frances","Munyonyo","0754645459","569874"),
    Customer("Agaba Pauline","Africa RM 65","0774535450","547896"),
    Customer("Mugarura Esther","Africa RM 99","0752535457","223654")
    ]

for sc in CS_B1:    
    print(sc.detail())

#CUSTOMERS OF BANK 2
print("CUSTOMERS of ",B2.name,"\n","_"*40)
CS_B2 = [
    Customer("Kigula Rabiot","Kansanga","0772225607","751663"),
    Customer("Kisembo Howard","Lumumba RM 107","0778268784","56214"),
    Customer("Okello Ali","Katale","0756678136","25487"),
    Customer("Mukuye Edward","Africa RM 07","0757507966","236589"),
    Customer("Muzoora Benny ","Nkrumah RM 143","0784507618","236547"),
    Customer("Barasa Jerry","Livinstone RM 23","0784530306","417589"),
    Customer("Tamale Paul","Lumumba RM 15","0754991136","236647"),
    Customer("Gor Malek","Bwaise","0754545803","456987"),
    Customer("Akuru Priscilla","Africa RM 65","0772581750","214568"),
    Customer("Otim Mark","Bunamwaya","0752001457","458796")
    ]

for sc in CS_B2:    
    print(sc.detail())
