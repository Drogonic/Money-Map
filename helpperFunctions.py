import streamlit as st
import requests
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

api_key = "105693d8dc0fa3dc8b61fc35"

# Supported Currencies For Exchange
currency_codes = [
    "USD", "EUR", "GBP", "CAD", "AUD", "JPY", "INR", "CHF", "CNY", "SGD",
    "HKD", "NZD", "ZAR", "SEK", "NOK", "DKK", "MXN", "BRL", "RUB", "PLN"
]


# Exchange_API Currency Handler
def get_exchange_rate(base_currency, target_currency):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()

    # Checking for a successful response
    if data["result"] == "success":
        rate = data["conversion_rates"].get(target_currency)
        if rate:
            return rate
        else:
            st.error(f"Currency {target_currency} not found.")
            return None
    else:
        st.error("Failed to fetch exchange rates.")
        return None


# Currency Conversion Calculator
def convert_currency(amount, rate):
    return amount * rate


def income_to_spend_ratio(income, expenses):
    return income / expenses if expenses > 0 else float('inf')


# Percentage Calculator
def spending_percentage(income, expenses):
    return (expenses / income) * 100 if income > 0 else 0


def manage_income_sources():
    st.subheader("Monthly Income Sources")
    st.write("Add multiple income sources, specify pay periods, and mark if they are recurring.")

    # Data for multiple income sources
    income_sources = []
    num_sources = st.number_input("Enter the number of income sources:", min_value=1, max_value=10, value=1)

    for i in range(num_sources):
        source_name = st.text_input(f"Income Source #{i + 1} Name", key=f"source_name_{i}")
        amount = st.number_input(f"Amount for {source_name}", min_value=0.0, key=f"amount_{i}")
        pay_period = st.selectbox(f"Pay Period for {source_name}", ["Weekly", "Bi-Weekly", "Monthly", "Annually"],
                                  key=f"pay_period_{i}")
        recurring = st.checkbox(f"Is {source_name} recurring?", key=f"recurring_{i}")
        income_sources.append({"Source Name": source_name, "Amount": amount, "Pay Period": pay_period,
                               "Recurring": recurring})


def quick_payoff(pay_by, interest_rate, loan_amount):
    if pay_by == 0:
        return st.warning("Payoff months must be greater than 1")
    else:
        monthly_interest_rate = (interest_rate / 100) / 12
        if monthly_interest_rate > 0:
            funct1 = monthly_interest_rate*((1+monthly_interest_rate) ** pay_by)
            funct2 = ((1+monthly_interest_rate) ** pay_by) - 1
            monthly_payoff = loan_amount * (funct1/funct2)
            total_interest_paid = (monthly_payoff * pay_by) - loan_amount
            return st.success(f"Our suggestion is {round(pay_by)} monthly payments of ${round(monthly_payoff, 2)}. "
                              f" The total amount paid in interest is {round(total_interest_paid, 2)}. "
                              f"Please consult with your bank for any extra fees.")
        else:
            monthly_payoff = loan_amount / pay_by
            return st.success(f"Our suggestion is {round(pay_by)} monthly payments of ${round(monthly_payoff)}. "
                              f"Please consult with your loan servicer for any extra fees.")


def account_type():
    account_type = st.selectbox("Account Type", ("High-Yield", "Rewards", "Standard", "Money Market"))
    st.info("We will use the market average for compounding according to your Account Type")
    if account_type == "High-Yield":
        return "Daily"
    elif account_type == "Rewards":
        return "Monthly"
    elif account_type == "Standard":
        return "None"
    elif account_type == "Money Market":
        return "Daily"


def apy_calculator(amount, rate, compounding_type, checking_saving):
    compounding = 1
    if compounding_type == "Daily":
        compounding = 365
    elif compounding_type == "Monthly":
        compounding = 12
    elif compounding_type == "None" and checking_saving == "Checking":
        return st.warning("This account will not generate interest.")
    elif compounding_type == "None" and checking_saving == "Savings":
        compounding = 365
    elif compounding_type == "Quarterly":
        compounding = 4
    elif compounding_type == "Annual":
        compounding = 1
    rate_decimal = rate / 100
    apy_result = ((1+(rate_decimal/compounding))**compounding) - 1
    yearly_earning = amount * apy_result
    monthly_earning = amount * apy_result / 12

    return st.success(f"We estimate that your account will produce {round(monthly_earning, 2)} monthly earnings."
                      f" For a total of ${round(yearly_earning, 2)} a year.")


def hide_sidebar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)
