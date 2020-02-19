import numpy as np
from math import isclose

class Calculator: 
    def __init__(self, property_price, ltv, interest, mortgage_type, deposit):
        # these are all user input that need to be stored
        self.property_price = property_price
        self.ltv = ltv
        self.interest = interest
        self.mortgage_type = mortgage_type
        self.deposit = deposit

    def calc_loan_mindeposit(self):
        loan_amount = float(self.property_price * (self.ltv / 100))
        min_deposit = np.round((float(self.property_price * (1 - (self.ltv / 100)))), 2)
        return loan_amount, min_deposit

    def calc_deposit(self):
        deposit = np.round(float(self.deposit), 2)
        min_deposit = np.round((float(self.property_price * (1 - (self.ltv / 100)))), 2)

        while deposit < min_deposit:
            return False
            # add: enter new value for deposit so that it's True or else higher for recalculation
        else: 
            if deposit > min_deposit:
                new_ltv = np.round((1-(deposit / self.property_price)) * 100, 2)
                deposit_percentage = np.round((deposit / self.property_price) * 100, 2)
                return [new_ltv, deposit_percentage]
                    
        if isclose(deposit, min_deposit):
            return True
    
    def monthly_repayments(self):
        loan_amount = float(self.property_price * (self.ltv / 100))
        loan_term = int(12*self.mortgage_type)
        monthly_interest = (self.interest * 12)
        capital_rf = (1 - (1 + self.interest / (12 * 100))**(-loan_term))
        monthly_repayments = np.round((self.property_price * (self.ltv / 100)) * ((self.interest / (12 * 100)) /capital_rf), 2)
        value_of_loan = np.round((monthly_repayments*loan_term), 2)
        total_interest = np.round((value_of_loan - loan_amount), 2)

        return monthly_repayments, value_of_loan, total_interest, loan_term


calc_1 = Calculator(150000, 70, 4.5, 15, 46000)
print(calc_1.calc_loan_mindeposit())
print(calc_1.calc_deposit())


