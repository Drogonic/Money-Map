import streamlit as st
import requests
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


def hide_sidebar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)
