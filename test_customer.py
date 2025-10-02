#ტესტირება ბიუჯეტი სწორად მცირდება თუ არა
import pytest
from back import Customer

def test_budget_pay_for_booking():
    test_customer = Customer(name = "Elene", budget = 1000)
    payed = test_customer.pay_for_booking(500)
    assert test_customer.budget == 500
    assert test_customer.points >= 50

def test_insufficient_funds_pay_for_booking():
    test_customer = Customer(name = "Elene", budget = 1000)
    payed = test_customer.pay_for_booking(1500)
    assert test_customer.budget == 1000
    assert test_customer.points == 0
