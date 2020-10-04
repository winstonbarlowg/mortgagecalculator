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
app.secret_key = 'P\xfai\x0c\x91 \xb6g\xa7\x9f\xcc\x01t\xaf\xc4\xe1\xef4\xf8\xf9\xc3\x8a\xeb\xd3\xad\x17\xb2\xd7{+\xfd\x97'
app.permanent_session_lifetime = timedelta(minutes=15)


@app.route('/')
def basic_info_form():
    return render_template('calculator.html')


@app.route('/calculator', methods=['GET', 'POST'])
def calculator_data():
    if request.method == 'POST':
        session['property_price'] = float(request.form['propertyPrice'])
        session['ltv'] = float(request.form['inputLtv'])
        session['interest_rate'] = float(request.form['inputInterest'])
        session['mortgage_term'] = float(request.form['mortgageType'])
        session['deposit'] = float(request.form['deposit'])

        calc_1 = Calculator(session['property_price'], session['ltv'],
                            session['interest_rate'], session['mortgage_term'], session['deposit'])

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
