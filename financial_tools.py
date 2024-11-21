import streamlit as st
import helpperFunctions

def financial_tools():
    choice = st.selectbox("Choose Tool", ["Quick Payoff Calculator", "Currency Exchange Calculator", "Loan APR Calculator",
                                          "Interest Return APY Calculator"])
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
    elif choice == "Loan APR Calculator":
        loan_Amount = st.number_input("Amount of loan", min_value=0)
        interest = st.number_input("Interest rate (APR%)", min_value=0)
        interest_type = st.selectbox("APR type", ("Simple APR", "Compounding APR"))
        if interest_type == "Compounding APR":
            compounding_type = st.selectbox("What type of Compounding APR?", ("Monthly", "Quarterly", "Annually"))
        else:
            compounding_type = ""
        has_fees = st.checkbox("Has fees?")
        if has_fees:
            fees = st.number_input("Enter fees amount")
        else:
            fees = 0
        loan_term = st.number_input("Please enter the loan term in years.", min_value=0)
        if st.button("Calculate Payment"):
            helpperFunctions.apr_calculator(loan_Amount, interest, compounding_type, interest_type, fees, loan_term)
    elif choice == "Interest Return APY Calculator":
        account_amount = st.number_input("Amount in account", min_value=0)
        account_rate = st.number_input("APY%", min_value=0)
        checking_or_savings = st.selectbox("Is this for a Checking or Savings Account?", ("Checking", "Savings"))
        compounding_type = st.selectbox("Compounding Type",
                                        ["Daily", "Monthly", "Quarterly", "Annual", "Don't Know"])
        if compounding_type == "Don't Know":
            compounding_type = helpperFunctions.account_type()
        if st.button("Calculate Return"):
            helpperFunctions.apy_calculator(account_amount, account_rate,compounding_type,checking_or_savings)

