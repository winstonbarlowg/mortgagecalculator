from models import Calculator, LendingCriteria

from flask import Flask, Blueprint, request, render_template
import requests

import pandas as pd
import numpy as np

app = Flask(__name__)


@app.route('/')
def basic_info_form():
    return render_template('calculator.html')

# TO DO: error handling for user input
# TO DO 2: send a request to backend for jsonified data
@app.route('/calculator', methods=['POST'])
def amortisation_visualisation():
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


@app.route('/criteria')
def criteria_info():
    return render_template('criteria.html')


@app.route('/criteria_result', methods=['POST', 'GET'])
def income_outgoings():
    annual_income = float(request.form['annualIncome'])
    monthly_outgoings = float(request.form['outgoingsMonthly'])
    tax_rate = request.form['tax_class']
    country_form = request.form['country']

    lending_check = LendingCriteria(
        annual_income, monthly_outgoings, country_form)
    tax_calc = lending_check.tax_rate()

    return render_template('criteria_overview.html', annual_income=annual_income, monthly_outgoings=monthly_outgoings, tax_rate=tax_rate, country_form=country_form, lending_check=lending_check.tax_rate())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
