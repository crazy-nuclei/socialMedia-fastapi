

def cal_sum(num1:int, num2:int): 
    return num1+num2

class InsufficientFunds(Exception): 
    pass 

class BankAccount:
    def __init__(self, balance=0) -> None:
        self.balance = balance 
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if(amount > self.balance):
            raise InsufficientFunds("Insufficient Funds")
        self.balance -= amount 
    
    def collect_interest(self):
        self.balance *= 1.1