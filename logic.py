import numpy as np
import numpy_financial as npf
import pandas as pd
from datetime import date, datetime
from math import isclose
from decimal import *

from flask import Flask, Blueprint, request, render_template

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

    # TO DO: integrate better to handle the input of the deposit value
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

    def basic_overview(self):
        loan_amount = float(self.property_price * (self.ltv / 100))
        loan_term = int(12*self.mortgage_type)

        # use npf for calculating monthly payment
        monthly_pmt = np.round(npf.pmt(
            (self.interest/100) / 12, self.mortgage_type * 12, self.property_price*(self.ltv/100)), 2)

        cost_of_loan = np.round((monthly_pmt*loan_term), 2)
        total_interest_paid = np.round((cost_of_loan + loan_amount), 2)

        return monthly_pmt, cost_of_loan, total_interest_paid, loan_term,

    def amortisation_table(self):
        total_terms = int(12 * self.mortgage_type)
        principal = self.property_price * (self.ltv/100)

        rng = pd.date_range(
            start=datetime.date(datetime.now()), periods=total_terms, freq='MS')
        rng.name = 'Payment_Date'

        # create pandas dataframe
        df = pd.DataFrame(index=rng, columns=[
                          'Payment', 'Principal', 'Interest', 'Balance', 'Cumulative Principal'], dtype='float')
        df.reset_index(inplace=True)
        df.index += 1
        df.index.name = 'Period'

        # values
        df['Payment'] = np.round(npf.pmt(
            (self.interest/100) / 12, self.mortgage_type * 12, self.property_price*(self.ltv/100)), 2)
        df['Principal'] = npf.ppmt(
            (self.interest/100)/12, df.index, total_terms, principal)
        df['Interest'] = npf.ipmt(
            (self.interest/100)/12, df.index, total_terms, principal)
        df['Cumulative Principal'] = df['Principal'].cumsum().clip(
            lower=-principal)
        df['Balance'] = principal + df['Cumulative Principal']

        df = df.round(2)

        return df


# mock input data for testing calculations
# calc_1 = Calculator(150000, 70, 4.5, 15, 45100)

# flask routes to get user input, make chart.js visualisations through templates
app = Flask(__name__)


@app.route('/')
def amortisation_viz():
    return render_template('calculator.html')

# TO DO: error handling for user input
# TO DO 2: send a request to backend for jsonified data
@app.route('/calculator', methods=['POST'])
def basic_info():
    property_price = float(request.form['propertyPrice'])
    ltv = float(request.form['inputLtv'])
    interest_rate = float(request.form['inputInterest'])
    mortgage_term = float(request.form['mortgageType'])
    deposit = float(request.form['deposit'])

    calc_1 = Calculator(property_price, ltv, interest_rate,
                        mortgage_term, deposit)

    df = calc_1.amortisation_table()

    # chart.js
    labels = df.index.tolist()
    values_principal = df['Principal'].tolist()
    values_interest = df['Interest'].tolist()

    return render_template('index.html', labels=labels, values_principal=values_principal, values_interest=values_interest)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
