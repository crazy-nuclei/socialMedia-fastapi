from app.calculations import cal_sum, BankAccount, InsufficientFunds
import pytest

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("x, y, res", [
    (1,2,3), (1,-1,0), (-1,2,1), (-1,-9,-10)
])
def test_sum(x, y, res):
    assert cal_sum(x, y) == res

def test_bank_account_default_balance(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_account_initial_balance(bank_account):
    assert bank_account.balance == 50

def test_bank_account_withdraw_function(bank_account): 
    bank_account.withdraw(30)
    assert bank_account.balance == 20

def test_bank_account_deposit_function(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80

def test_bank_account_collect_interest_method(bank_account): 
    bank_account.collect_interest()
    assert int(bank_account.balance) == 55

@pytest.mark.parametrize("deposit, withdraw, balance", [
    (100, 50, 50), (1,1,0), (4,2,2), (1000, 90, 910)
])
def test_bank_transaction(zero_bank_account, deposit, withdraw, balance): 
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == balance

def test_bank_account_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds): 
        bank_account.withdraw(100)