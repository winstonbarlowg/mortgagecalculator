from models import Calculator, IncomeAnalysis

from flask import Flask, Blueprint, request, render_template, send_file
import requests

from openpyxl import Workbook
from flask_caching import Cache

import pandas as pd
import numpy as np

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "simple",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)

app.config.from_mapping(config)
cache = Cache(app)


@app.route('/')
def basic_info_form():
    return render_template('calculator.html')

# TO DO 2: send a request to backend for jsonifiesd data
@app.route('/calculator', methods=['POST'])
@cache.cached(timeout=100)
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

    download_excel = df.to_excel("amortization_schedule.xlsx")

    return render_template('schedule.html', download_excel=download_excel, labels=labels, values_principal=values_principal, values_interest=values_interest)


@app.route('/criteria')
def criteria_info():
    return render_template('criteria.html')


@app.route('/criteria_result', methods=['POST', 'GET'])
def income_outgoings():
    annual_income = float(request.form['annualIncome'])
    monthly_outgoings = float(request.form['outgoingsMonthly'])
    tax_rate = request.form['tax_class']
    country_form = request.form['country']

    lending_check = IncomeAnalysis(
        annual_income, monthly_outgoings, country_form)
    tax_calc = lending_check.tax_rate()

    return render_template('criteria_overview.html', annual_income=annual_income, monthly_outgoings=monthly_outgoings, tax_rate=tax_rate, country_form=country_form, lending_check=lending_check.tax_rate())


@app.route('/dashboard', methods=['POST'])
def main():
    def amortisation_schedule():
        pass

    def fluctuation_pie():
        pass

    values_schedule = None
    labels_schedule = None

    values_fluc = None
    labels_fluc = None

    return render_template()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
