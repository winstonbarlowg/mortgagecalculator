from models import Calculator, IncomeAnalysis

from flask import Flask, Blueprint, request, render_template, send_file, redirect, url_for, session, escape
from flask_login import current_user, logout_user
from datetime import timedelta

# from flask import current_app as app
# from .assets import compile_auth_assets
# from flask_login import login_required

import requests

from openpyxl import Workbook
from flask_caching import Cache

import pandas as pd
import numpy as np

app = Flask(__name__)
app.secret_key = b'\xa8\xf0\xb9z\x93g\xdd\xbf\xb8\x97\xa8\x14\xa0\xeb\xc3\xe1\xe2\x98\x8f\xa2Q_\xf0\x06'
app.permanent_session_lifetime = timedelta(minutes=15)


@app.route('/')
def basic_info_form():
    return render_template('index.html')


@app.route('/amortization_calculator', methods=['GET', 'POST'])
def store_input():
    if request.method == 'POST':
        session['property_price'] = float(request.form['propertyPrice'])
        session['ltv'] = float(request.form['inputLtv'])
        session['interest_rate'] = float(request.form['inputInterest'])
        session['mortgage_type'] = int(request.form['mortgageType'])
        session['deposit'] = float(request.form['deposit'])
        return redirect(url_for('calculator_data'))
    else:
        return render_template('calculator.html')


@app.route('/amortization', methods=['GET', 'POST'])
def calculator_data():
    calc_1 = Calculator(session.get('property_price', None), session.get('ltv', None),
                        session.get('interest_rate', None), session.get('mortgage_type', None), session.get('deposit', None))

    df = calc_1.amortisation_table()

    # chart.js data
    labels = df.index.tolist()
    values_principal = df['Principal'].tolist()
    values_interest = df['Interest'].tolist()

    return render_template('schedule.html', labels=labels, values_principal=values_principal, values_interest=values_interest)


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
