import streamlit as st
import requests
import folium
import polyline
from datetime import datetime
from streamlit_folium import folium_static
import plotly.express as px
import pandas as pd
import numpy as np

st.title("MoneyMap App")
st.header("Streamlit and Exchange Rate API")
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


# Income to Spend Ratio Calculator
def income_to_spend_ratio(income, expenses):
    return income / expenses if expenses > 0 else float('inf')


# Percentage Calculator
def spending_percentage(income, expenses):
    return (expenses / income) * 100 if income > 0 else 0


# Recommended values
recommended_ratio = 1.2  # Suggested income-to-spend ratio
recommended_spending_percentage = 80  # Suggested max spending as a percentage of income


def create_account_form():
    # Request the user's email via a text input widget in the sidebar.
    # The function st.sidebar.text_input displays a text box in the sidebar where users can enter their email.
    username = st.sidebar.text_input("Enter your username")

    # Create a button in the sidebar that users can click to submit their email and create an account.
    # The function st.sidebar.button returns True when the button is clicked, triggering the conditional.
    if st.sidebar.button("Create account"):
        # Check if the email variable contains any text, which indicates that the user has entered something.
        if username:
            # If an email is provided, update the session state to reflect that an account has been created.
            # st.session_state['create_account'] is a persistent variable that holds the state of account creation.
            st.session_state['create_account'] = True

            # Display a success message in the sidebar using st.sidebar.success to inform the user that the account was created successfully.
            st.sidebar.success("Account created successfully!")
        else:
            # If no email is entered (email string is empty), display an error message prompting the user to enter an email address.
            # This uses st.sidebar.error to show the message in the sidebar.
            st.sidebar.error("Please enter an username address.")


# Initialize the 'create_account' flag in the session state if it's not already set.
# This flag will keep track of whether a user has created an account.
if 'create_account' not in st.session_state:
    st.session_state['create_account'] = False

account_type = st.sidebar.selectbox("Please choose how you wish to continue", options=["Continue as a Guest",
                                                                                       "Create an Account"])
st.sidebar.info("If you choose to continue as a Guest your information will not be saved")

if account_type == "Continue as a Guest":

    task_type = st.sidebar.selectbox("Are we working on", options=["Income to Spend Ratio Calculator"
                                                                   "", "Currency Exchange Calculator"])

    if task_type == "Income to Spend Ratio Calculator":
        monthly_income = st.number_input("Please enter your Monthly Income", min_value=0.0)
        monthly_expenses = st.number_input("Please enter your Monthly Expenses", min_value=0.0)
        ratio = income_to_spend_ratio(monthly_income, monthly_expenses)
        percentage_spent = spending_percentage(monthly_income, monthly_expenses)
        amount_saved_or_spent = monthly_income - monthly_expenses  # Positive if saving, negative if overspending

        # Determine message color based on savings
        if amount_saved_or_spent < 0:
            message_color = "error"  # Red for overspending (negative savings)
            message_text = f"You are overspending by ${abs(amount_saved_or_spent):,.2f}."
        elif percentage_spent <= recommended_spending_percentage:
            message_color = "success"  # Green if spending within or below recommended amount
            message_text = f"Good job! You are saving ${amount_saved_or_spent:,.2f}."
        else:
            message_color = "warning"  # Yellow if spending over the recommended amount but still saving
            message_text = f"You are spending more than recommended, but saving ${amount_saved_or_spent:,.2f}."
        if st.button("Calculate"):
            # Display the results
            st.success(f"**Income to Spend Ratio**: {ratio:.2f}")
            st.info(
                f"You are spending {percentage_spent:.2f}% of your income, which means you are saving {100 - percentage_spent:.2f}%.")
            st.info(
                f"**Recommended Income to Spend Ratio**: {recommended_ratio:.2f} (Spending {recommended_spending_percentage}% of income or less).")
            if message_color == "success":
                st.success(message_text)
            elif message_color == "warning":
                st.warning(message_text)
            else:
                st.error(message_text)
    else:
        base_currency = st.selectbox("Select the currency to be exchanged:", currency_codes,
                                     index=currency_codes.index("USD"))
        target_currency = st.selectbox("Select the desired currency:", currency_codes,
                                       index=currency_codes.index("EUR"))
        amount = st.number_input("Enter the amount to convert:", min_value=0.0)
        if st.button("Convert"):
            rate = get_exchange_rate(base_currency, target_currency)
            if rate:
                converted_amount = convert_currency(amount, rate)
                st.success(f"{amount} {base_currency} is equal to {converted_amount:.2f} {target_currency}.")
