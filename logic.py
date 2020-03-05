import numpy as np
import numpy_financial as npf
import pandas as pd
from datetime import date, datetime
from math import isclose
from decimal import *

from flask import Flask, request, render_template
import requests


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
        min_deposit = np.round(
            (float(self.property_price * (1 - (self.ltv / 100)))), 2)
        return loan_amount, min_deposit

    def calc_deposit(self):
        deposit = np.round(float(self.deposit), 2)
        min_deposit = np.round(
            (float(self.property_price * (1 - (self.ltv / 100)))), 2)

        while deposit < min_deposit:
            return False
            # add: enter new value for deposit so that it's True or else higher for recalculation
        else:
            if deposit > min_deposit:
                new_ltv = np.round(
                    (1-(deposit / self.property_price)) * 100, 2)
                deposit_percentage = np.round(
                    (deposit / self.property_price) * 100, 2)
                return [new_ltv, deposit_percentage]

        if isclose(deposit, min_deposit):
            return True

    def monthly_repayments(self):
        loan_amount = float(self.property_price * (self.ltv / 100))
        loan_term = int(12*self.mortgage_type)

        # use npf for calculating monthly payment
        monthly_pmt = np.round(npf.pmt(
            (self.interest/100) / 12, self.mortgage_type * 12, self.property_price*(self.ltv/100)), 2)

        cost_of_loan = np.round((monthly_pmt*loan_term), 2)
        total_interest_paid = np.round((cost_of_loan - loan_amount), 2)

        return monthly_pmt, cost_of_loan, total_interest_paid, loan_term,


calc_1 = Calculator(150000, 70, 4.5, 15, 45100)

# amortisation schedule, principal vs interest


class AmortisationSchedule:
    def __init__(self):
        self

        # calculate interest at a given period 'per'
    def interest(self, interest_rate=calc_1.interest, total_terms=calc_1.monthly_repayments()[3],
                 loan_years=calc_1.mortgage_type, principal=calc_1.property_price*(calc_1.ltv/100)):
        per = 150
        ipmt = npf.ipmt((interest_rate/100) / 12,
                        per, total_terms, principal)
        return ipmt

    # calculate principal at a given period 'per'
    def principal(self, interest_rate=calc_1.interest, total_terms=calc_1.monthly_repayments()[3],
                  loan_years=calc_1.mortgage_type, principal=calc_1.property_price*(calc_1.ltv/100)):
        per = 150
        ppmt = npf.ppmt((interest_rate/100) / 12,
                        per, total_terms, principal)
        return ppmt

    def amortisation_table(self, interest_rate=calc_1.interest, total_terms=calc_1.monthly_repayments()[3],
                           principal=calc_1.property_price*(calc_1.ltv/100)):
        rng = pd.date_range(
            start=datetime.date(datetime.now()), periods=calc_1.monthly_repayments()[3], freq='MS')
        rng.name = 'Payment_Date'

        # create pandas dataframe
        df = pd.DataFrame(index=rng, columns=[
                          'Payment', 'Principal', 'Interest', 'Balance', 'Cumulative Principal'], dtype='float')
        df.reset_index(inplace=True)
        df.index += 1
        df.index.name = 'Period'

        # values
        df['Payment'] = calc_1.monthly_repayments()[0]
        df['Principal'] = npf.ppmt(
            (interest_rate/100)/12, df.index, total_terms, principal)
        df['Interest'] = npf.ipmt(
            (interest_rate/100)/12, df.index, total_terms, principal)
        df['Cumulative Principal'] = df['Principal'].cumsum().clip(
            lower=-principal)
        df['Balance'] = principal + df['Cumulative Principal']

        df = df.round(2)

        return df


print(calc_1.calc_loan_mindeposit())
print(calc_1.calc_deposit())
print(calc_1.monthly_repayments())
print(calc_1.deposit)

# flask routes to make chart.js visualisations and display templates

app = Flask(__name__)


@app.route('/')
def amortisation_viz():
    return render_template('calculator.html')


@app.route('/calculator', methods=['POST'])
def basic_info():
    property_price = request.form['propertyPrice']
    ltv = request.form['inputLtv']
    interest_rate = request.form['inputInterest']
    mortgage_term = request.form['mortgageType']
    deposit = request.form['deposit']

    calc_2 = Calculator(property_price, ltv, interest_rate,
                        mortgage_term, deposit)
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
