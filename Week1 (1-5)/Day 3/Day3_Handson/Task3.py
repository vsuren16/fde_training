# Financial Account Management System

class Customer:
    def __init__(self, cust_id, cust_name, cust_contact):
        self.__cust_id = cust_id
        self.__cust_name = cust_name
        self.__cust_contact = cust_contact

    def get_customer_info(self):
        return f"Customer Id: {self.__cust_id}, Name: {self.__cust_name}, Contact: {self.__cust_contact}"

# Base class Account
class Account:
    def __init__(self, acc_no, acc_balance, account_type):
        self.__acc_no = acc_no
        self.__acc_balance = acc_balance
        self.__account_type = account_type

    def get_account_info(self):
        return f"Account No: {self.__acc_no}, Balance: Rs.{self.__acc_balance}, Account Type: {self.__account_type}"

    def get_balance(self):
        return self.__acc_balance

    def deposit(self, amount):
        self.__acc_balance += amount
        print(f"Deposited Rs.{amount}. New Balance: Rs.{self.get_balance()}")

    def withdraw(self, amount):
        if self.__acc_balance >= amount:
            self.__acc_balance -= amount
            print(f"Withdrew Rs.{amount}. New Balance: Rs.{self.get_balance()}")
        else:
            print("Insufficient balance for withdrawal.")

# Derived class SavingsAccount
class SavingsAccount(Account):
    def __init__(self, acc_no, acc_balance):
        super().__init__(acc_no, acc_balance, "Savings")

# Derived class CurrentAccount
class CurrentAccount(Account):
    def __init__(self, acc_no, acc_balance):
        super().__init__(acc_no, acc_balance, "Current")

class Transaction:
    def __init__(self, trans_id, trans_amount, trans_type, account):
        self.__trans_id = trans_id
        self.__trans_amount = trans_amount
        self.__trans_type = trans_type 
        self.__account = account

    def execute_transaction(self):
        if self.__trans_type == "credit":
            self.__account.deposit(self.__trans_amount)
        elif self.__trans_type == "debit":
            self.__account.withdraw(self.__trans_amount)

class Bank:
    def __init__(self):
        self.accounts = []

    def show_account_info(self, account):
        print(account.get_account_info())

# Create customers
customer1 = Customer(101, 'Alice', '9876543210')
customer2 = Customer(102, 'Bob', '9876543211')

# Create accounts 
savings_account = SavingsAccount('ACC123', 5000)
current_account = CurrentAccount('ACC124', 3000)

# Add accounts to bank class
bank = Bank()
bank.accounts.append(savings_account)
bank.accounts.append(current_account)

# Display account info for both accounts
print("Showing Account Information for Alice:")
bank.show_account_info(savings_account)
bank.show_account_info(current_account)

# create transaction object for savings account
transaction1 = Transaction('T001', 1000, 'credit', savings_account)  
transaction2 = Transaction('T002', 500, 'debit', savings_account)   
transaction3 = Transaction('T003', 7000, 'debit', savings_account) 

# process transaction
transaction1.execute_transaction()  
transaction2.execute_transaction()  
transaction3.execute_transaction()  

# create transaction object for current account
transaction4 = Transaction('T004', 2000, 'debit', current_account)  
transaction5 = Transaction('T005', 4000, 'debit', current_account)  

# process transaction
transaction4.execute_transaction()  
transaction5.execute_transaction() 

# Final account details after all the transactions
print("\nShowing Account Information after transactions:")
bank.show_account_info(savings_account)
bank.show_account_info(current_account)
