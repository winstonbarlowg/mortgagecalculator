import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import isclose


def get_a_float(prompt):  # check for ValueError for each input
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print('Please enter a valid number e.g. 5000, or 5.5')
        else:
            break
    return value


property_price = get_a_float('Enter property price in GBP: ')
ltv = get_a_float('Enter the maximum LTV offered by your bank: ')

loan_amount = property_price*(ltv/100)
min_deposit = np.round((property_price*(1-(ltv/100))), 2)

print(f"The loan amount would be of: = £{loan_amount}")
print(f"At a LTV of {ltv}%, " +
      f"your minimum deposit would be of: = £{min_deposit}")

# deposit according to LTV or higher
deposit = float(input(
    'Enter amount of deposit, this can be higher to reduce your LTV and the amount of the loan: '))

while deposit < min_deposit:
    print(f"I'm sorry, but your deposit can't be lower that {min_deposit}")
    deposit = float(
        input(f'Enter a value that is equal or higher to £{min_deposit} '))
    if deposit > min_deposit:
        new_ltv = np.round((1-(deposit/property_price))*100, 2)
        deposit_percentage = np.round((deposit/property_price)*100, 2)
        print(f"With that deposit, the LTV would be of: = {new_ltv}%")
        print(
            f"And the deposit as a percentage of the value would be of: = {deposit_percentage}%")
        break

if isclose(deposit, min_deposit):
    print("Excellent! let's find out more about your mortgage")

# calculating monthly repayments based on interest and mortgage type in years
interest = float(input('Please enter the annual interest rate for the loan: '))
mortgage_type = int(
    input('Enter mortgage type in years, e.g. 15 for 15 years: '))

loan_term = int(12*mortgage_type)
monthly_interest = (interest/12)
# capital recovery factor
capital_rf = (1-(1+interest/(12*100))**(-loan_term))

monthly_repayments = np.round(loan_amount*((interest/(12*100))/capital_rf), 2)

# for calculating total interet paid
value_of_loan = np.round((monthly_repayments*loan_term), 2)
total_interest = np.round((value_of_loan - loan_amount), 2)

# summary of monthly payments, how many, interest to be paid
print(f"Your monthly repayments would be of: £{monthly_repayments}")
print(f"You have a total of {loan_term} monthly repayments" +
      f" which add up to a total value of the loan of £{value_of_loan}")
print(f"The total interest to be paid is of: £{total_interest}")

# interest curve
interest_monthly = []
month_starting_balance = []
month_ending_balance = []


# use range to generate sequence of numbers from 1 to the last loan month

# for a in range(1, loan_term+1):
#     interest = Loan_Amount*(R-1)
#     loan_amount = Loan_Amount - (X-Interest)
#     monthly_interest = np.append(Monthly_Interest,Interest)
#     monthly_balance = np.append(Monthly_Balance, Loan_Amount)
