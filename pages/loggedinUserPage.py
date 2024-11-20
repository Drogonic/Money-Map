import datetime
import streamlit as st
import helpperFunctions
import DatabaseConnection as db_conn
import checking_account
import savings_account
import expenses_account
import income_account
import loans_account
import creditcard_account


helpperFunctions.hide_sidebar()
st.title("Money Map")

checking, saving, expenses, income, loans, credit, search, overview, financial_tools, settings = st.tabs(
    ["Checking", "Savings", "Expenses", "Income"
        , "Loans", "Credit Cards", "Search", "Overview", "Financial Tools", "Settings"])
with checking:
    checking_account.checking_account()

with saving:
    savings_account.saving_account()

with expenses:
    expenses_account.expenses_account()
with income:
    income_account.income_account()

with loans:
    loans_account.loan_accounts()

with credit:
    creditcard_account.credit_accounts()

with financial_tools:
    choice = st.selectbox("Choose Tool", ("Quick Payoff Calculator", "Currency Exchange Calculator"))
    if choice == "Quick Payoff Calculator":
        loan_Amount = st.number_input("Amount of loan")
        interest = st.number_input("Interest rate (APR%)")
        pay_by = st.number_input("Payoff in how many months", min_value=0)
        if st.button("Calculate Payment"):
            helpperFunctions.quick_payoff(pay_by, interest, loan_Amount)
    elif choice == "Currency Exchange Calculator":
        base_currency = st.selectbox("Select the currency to be exchanged:", helpperFunctions.currency_codes,
                                     index=helpperFunctions.currency_codes.index("USD"))
        target_currency = st.selectbox("Select the desired currency:", helpperFunctions.currency_codes,
                                       index=helpperFunctions.currency_codes.index("EUR"))
        amount = st.number_input("Enter the amount to convert:", min_value=0.0)
        convertButton = st.button("Convert")
        if convertButton and base_currency == target_currency:
            st.write("Please select two different currencies")
        else:
            rate = helpperFunctions.get_exchange_rate(base_currency, target_currency)
            if rate and convertButton:
                converted_amount = helpperFunctions.convert_currency(amount, rate)
                st.success(f"{amount:.2f} {base_currency} is equal to {converted_amount:.2f} {target_currency}.")

with search:
    st.write("WIP")
    # need to understand database
with overview:
    st.write("WIP")
    # need to understand database
with settings:
    if st.button("Log Out"):
        st.switch_page("Homepage.py")
