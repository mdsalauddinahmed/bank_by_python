import random

class Bank:
    users = []
    admin_password = "admin123"
    loan_enabled = True

class User:
    def __init__(self, name, email, address, account_type, password):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.balance = 0
        self.account_number = random.randint(10000, 99999)
        self.transaction_history = []
        self.loan_taken = 0
        self.loan_limit = 2
        self.password = password

    def deposit(self, amount):
        self.balance += amount
        self.transaction_history.append(f"Deposited ${amount}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Withdrawal amount exceeded. Insufficient balance.")
        else:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew ${amount}")

    def check_balance(self):
        return self.balance

    def loan_request(self, amount):
        if Bank.loan_enabled and self.loan_limit > 0:
            self.balance += amount
            self.loan_taken += amount
            self.loan_limit -= 1
            self.transaction_history.append(f"Loan taken: ${amount}")
            print(f"Loan of ${amount} granted. Remaining loan limit: {self.loan_limit}")
        else:
            print("Loan feature is currently not available or loan limit exceeded.")

    def transfer(self, recipient, amount):
        if recipient in Bank.users:
            if amount <= self.balance:
                self.balance -= amount
                recipient.deposit(amount)
                self.transaction_history.append(f"Transferred ${amount} to {recipient.name}")
                print(f"Transfer successful. Remaining balance: ${self.balance}")
            else:
                print("Insufficient balance for the transfer.")
        else:
            print("Recipient account does not exist.")

class Admin:
    @staticmethod
    def create_account(name, email, address, account_type, password):
        user = User(name, email, address, account_type, password)
        Bank.users.append(user)
        print(f"Account created successfully. Account Number: {user.account_number}")

    @staticmethod
    def delete_account(account_number):
        for user in Bank.users:
            if user.account_number == account_number:
                Bank.users.remove(user)
                print(f"Account with Account Number {account_number} deleted successfully.")
                return
        print("Account not found.")

    @staticmethod
    def view_all_accounts():
        for user in Bank.users:
            print(f"Account Number: {user.account_number}, Name: {user.name}, Balance: ${user.balance}")

    @staticmethod
    def total_balance():
        total_balance = sum(user.balance for user in Bank.users)
        print(f"Total Available Balance in the bank: ${total_balance}")

    @staticmethod
    def total_loan_amount():
        total_loan = sum(user.loan_taken for user in Bank.users)
        print(f"Total Loan Amount in the bank: ${total_loan}")

    @staticmethod
    def toggle_loan_feature():
        Bank.loan_enabled = not Bank.loan_enabled
        status = "ON" if Bank.loan_enabled else "OFF"
        print(f"Loan feature is now {status}")

# User Registration
def user_registration():
    print("\n===== User Registration =====")
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    address = input("Enter your address: ")
    account_type = input("Enter your account type (Savings/Current): ").capitalize()
    password = input("Set your password: ")

    if any(user.email == email for user in Bank.users):
        print("User with this email already exists. Please log in.")
    else:
        Admin.create_account(name, email, address, account_type, password)

# User Login
def user_login():
    print("\n===== User Login =====")
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    user = next((u for u in Bank.users if u.email == email and u.password == password), None)
    if user:
        print(f"\nWelcome, {user.name}!")
        while True:
            print("\n===== User Options =====")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Check Balance")
            print("4. Request Loan")
            print("5. Transfer Money")
            print("6. View Transaction History")
            print("7. Logout")
            user_choice = int(input("Enter your choice: "))

            if user_choice == 1:
                amount = float(input("Enter the amount to deposit: "))
                user.deposit(amount)
            elif user_choice == 2:
                amount = float(input("Enter the amount to withdraw: "))
                user.withdraw(amount)
            elif user_choice == 3:
                print(f"Your current balance: ${user.check_balance()}")
            elif user_choice == 4:
                amount = float(input("Enter the loan amount: "))
                user.loan_request(amount)
            elif user_choice == 5:
                recipient_account_number = int(input("Enter the recipient's account number: "))
                recipient = next((u for u in Bank.users if u.account_number == recipient_account_number), None)
                if recipient:
                    amount = float(input("Enter the amount to transfer: "))
                    user.transfer(recipient, amount)
                else:
                    print("Recipient account does not exist.")
            elif user_choice == 6:
                print("\n===== Transaction History =====")
                for transaction in user.transaction_history:
                    print(transaction)
            elif user_choice == 7:
                print("Logout successful.")
                break
            else:
                print("Invalid choice. Please try again.")
    else:
        print("User not found. Please register.")

# Replica System
while True:
    print("\n===== Banking Management System =====")
    print("1. Register")
    print("2. User Login")
    print("3. Admin Login")
    print("4. Exit")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        user_registration()
    elif choice == 2:
        user_login()
    elif choice == 3:
        print("\n===== Admin Login =====")
        admin_password = input("Enter the admin password: ")

        if admin_password == Bank.admin_password:
            print("Admin login successful.")
            while True:
                print("\n===== Admin Options =====")
                print("1. Create Account")
                print("2. Delete Account")
                print("3. View All Accounts")
                print("4. Total Available Balance")
                print("5. Total Loan Amount")
                print("6. Toggle Loan Feature")
                print("7. Logout")
                admin_choice = int(input("Enter your choice: "))

                if admin_choice == 1:
                    name = input("Enter user's name: ")
                    email = input("Enter user's email: ")
                    address = input("Enter user's address: ")
                    account_type = input("Enter user's account type (Savings/Current): ").capitalize()
                    password = input("Enter user's password: ")
                    Admin.create_account(name, email, address, account_type, password)
                elif admin_choice == 2:
                    account_number = int(input("Enter the account number to delete: "))
                    Admin.delete_account(account_number)
                elif admin_choice == 3:
                    Admin.view_all_accounts()
                elif admin_choice == 4:
                    Admin.total_balance()
                elif admin_choice == 5:
                    Admin.total_loan_amount()
                elif admin_choice == 6:
                    Admin.toggle_loan_feature()
                elif admin_choice == 7:
                    print("Admin logout successful.")
                    break
                else:
                    print("Invalid choice. Please try again.")

        else:
            print("Invalid admin password. Access denied.")

    elif choice == 4:
        print("Exiting the Banking Management System. Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")