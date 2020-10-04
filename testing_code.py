annual_income = 40000
country = 'Scotland'
monthly_outgoings = 2500


def taxes():
    rate = None
    while country == 'Scotland':
        if annual_income <= 2049:
            rate = 0.19
        elif annual_income >= 2050 and annual_income <= 12444:
            rate = 0.2
        elif annual_income >= 12445 and annual_income <= 30930:
            rate = 0.21
        elif annual_income >= 30931 and annual_income <= 150000:
            rate = 0.4
        elif annual_income >= 150001:
            rate = 0.46
        else:
            break

    return rate


print(taxes())


class LendingCriteria:
    def __init__(self, annual_income, monthly_outgoings, country):
        self.annual_income = annual_income
        self.monthly_outgoings = monthly_outgoings
        self.country = country

    def tax_rate(self):
        rate = None
        if self.country == 'England' or self.country == 'Northern Ireland' or self.country == 'Wales':
            if self.annual_income <= 37500:
                rate = 0.2
            elif 37501 >= self.annual_income <= 150000:
                rate = 0.4
            elif self.annual_income >= 150001:
                rate = 0.45

        if self.country == 'Scotland':
            if self.annual_income <= 2049:
                rate = 0.19
            elif 2050 >= self.annual_income <= 12444:
                rate = 0.2
            elif 12445 >= self.annual_income <= 30930:
                rate = 0.21
            elif 30931 >= self.annual_income <= 150000:
                rate = 0.4
            elif self.annual_income >= 150001:
                rate = 0.46

        return rate


lending = LendingCriteria(annual_income, monthly_outgoings, country)
print(lending.tax_rate())
