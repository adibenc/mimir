import argparse, traceback
from decimal import Decimal

from modeling.data import *


class DCF:
	def __init__(self):
		self._ticker = None
		self._ev_statement = None
		self._income_statement = None
		self._balance_statement = None
		self._cashflow_statement = None
		self._discount_rate = None
		self._forecast_period = None
		self._earnings_growth_rate = None
		self._cap_ex_growth_rate = None
		self._perpetual_growth_rate = None
		self._enterprise_value = None
		self._equity_value = None
		self._share_price = None
		self._date = None

	def set_ticker(self, ticker):
		self._ticker = ticker
		return self

	def set_statements(self, ev_statement, income_statement, balance_statement, cashflow_statement):
		self._ev_statement = ev_statement
		self._income_statement = income_statement
		self._balance_statement = balance_statement
		self._cashflow_statement = cashflow_statement
		return self

	def set_forecast_parameters(self, discount_rate, forecast_period, earnings_growth_rate, cap_ex_growth_rate, perpetual_growth_rate):
		self._discount_rate = discount_rate
		self._forecast_period = forecast_period
		self._earnings_growth_rate = earnings_growth_rate
		self._cap_ex_growth_rate = cap_ex_growth_rate
		self._perpetual_growth_rate = perpetual_growth_rate
		return self


	def _calculate_enterprise_value(self):
		self._enterprise_value = self._enterprise_value_calculation(self._income_statement,
																	self._cashflow_statement,
																	self._balance_statement,
																	self._forecast_period,
																	self._discount_rate,
																	self._earnings_growth_rate,
																	self._cap_ex_growth_rate,
																	self._perpetual_growth_rate)


	def _calculate_equity_value_and_share_price(self):
		self._equity_value, self._share_price = self._equity_value_calculation(self._enterprise_value,
																			self._ev_statement)
		self._date = self._income_statement[0]['date']

	def calculate_dcf(self):
		self._calculate_enterprise_value()
		self._calculate_equity_value_and_share_price()

		print('\nEnterprise Value for {}: ${}.'.format(self._ticker, '%.2E' % Decimal(str(self._enterprise_value))),
			'\nEquity Value for {}: ${}.'.format(self._ticker, '%.2E' % Decimal(str(self._equity_value))),
			'\nPer share value for {}: ${}.\n'.format(self._ticker, '%.2E' % Decimal(str(self._share_price))),
			)

		return {
			'date': self._date,
			'enterprise_value': self._enterprise_value,
			'equity_value': self._equity_value,
			'share_price': self._share_price
		}

	def _ulFCF(self, ebit, tax_rate, non_cash_charges, cwc, cap_ex):
		return ebit * (1 - tax_rate) + non_cash_charges + cwc + cap_ex

	def _get_discount_rate(self):
		return self._discount_rate # Placeholder -  Implement proper WACC calculation if needed


	def _equity_value_calculation(self, enterprise_value, enterprise_value_statement):
		equity_val = enterprise_value - enterprise_value_statement['+ Total Debt']
		equity_val += enterprise_value_statement['- Cash & Cash Equivalents']
		share_price = equity_val / float(enterprise_value_statement['Number of Shares'])
		return equity_val, share_price

	def _enterprise_value_calculation(self, income_statement, cashflow_statement, balance_statement, period, discount_rate, earnings_growth_rate, cap_ex_growth_rate, perpetual_growth_rate):
		#Implementation remains the same as in the original code
		# ... (rest of the enterprise_value function remains unchanged) ...
		if income_statement[0]['EBIT']:
			ebit = float(income_statement[0]['EBIT'])
		else:
			ebit = float(input(f"EBIT missing. Enter EBIT on {income_statement[0]['date']} or skip: "))
		tax_rate = float(income_statement[0]['Income Tax Expense']) / \
				float(income_statement[0]['Earnings before Tax'])
		non_cash_charges = float(cashflow_statement[0]['Depreciation & Amortization'])
		cwc = (float(balance_statement[0]['Total assets']) - float(balance_statement[0]['Total non-current assets'])) - \
			(float(balance_statement[1]['Total assets']) - float(balance_statement[1]['Total non-current assets']))
		cap_ex = float(cashflow_statement[0]['Capital Expenditure'])
		discount = discount_rate

		flows = []

		print('Forecasting flows for {} years out, starting at {}.'.format(period, income_statement[0]['date']),
			('\n         DFCF   |    EBIT   |    D&A    |    CWC     |   CAP_EX   | '))
		for yr in range(1, period + 1):

			ebit = ebit * (1 + (yr * earnings_growth_rate))
			non_cash_charges = non_cash_charges * (1 + (yr * earnings_growth_rate))
			cwc = cwc * 0.7  # TODO: evaluate this cwc rate? 0.1 annually?
			cap_ex = cap_ex * (1 + (yr * cap_ex_growth_rate))

			flow = self._ulFCF(ebit, tax_rate, non_cash_charges, cwc, cap_ex)
			PV_flow = flow / ((1 + discount) ** yr)
			flows.append(PV_flow)

			print(str(int(income_statement[0]['date'][0:4]) + yr) + '  ',
				'%.2E' % Decimal(PV_flow) + ' | ',
				'%.2E' % Decimal(ebit) + ' | ',
				'%.2E' % Decimal(non_cash_charges) + ' | ',
				'%.2E' % Decimal(cwc) + ' | ',
				'%.2E' % Decimal(cap_ex) + ' | ')

		NPV_FCF = sum(flows)

		final_cashflow = flows[-1] * (1 + perpetual_growth_rate)
		TV = final_cashflow / (discount - perpetual_growth_rate)
		NPV_TV = TV / (1 + discount) ** (1 + period)

		return NPV_TV + NPV_FCF



#Example Usage
"""
if __name__ == "__main__":
	#Fetch Data (replace with your actual data fetching)
	ticker = 'AAPL'
	apikey = '<YOUR_API_KEY>'  # Replace with your API Key
	ev_statement = get_EV_statement(ticker, apikey=apikey)
	ev_statement = get_EV_statement(ticker, apikey=apikey)[0]['enterpriseValue']  #Get most recent data
	income_statement = get_income_statement(ticker, apikey=apikey)['financials']
	balance_statement = get_balance_statement(ticker, apikey=apikey)['financials']
	cashflow_statement = get_cashflow_statement(ticker, apikey=apikey)['financials']

	#Build and run the DCF calculation
	dcf_calculator = DCF() \
		.set_ticker(ticker) \
		.set_statements(ev_statement, income_statement, balance_statement, cashflow_statement) \
		.set_forecast_parameters(discount_rate=0.1, forecast_period=5, earnings_growth_rate=0.05, cap_ex_growth_rate=0.045, perpetual_growth_rate=0.02)

	dcf_results = dcf_calculator.calculate_dcf()
	print(dcf_results)
"""

