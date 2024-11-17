import datetime
import streamlit as st
import helpperFunctions
helpperFunctions.hide_sidebar()
# REMEMBER TO ADD LOGIC FOR IF THE INPUTS ARE EMPTY
st.title("Money Map")

checking, saving, expenses, income, loans, credit, search, overview,quick_payoff,settings = st.tabs(
    ["Checking", "Savings", "Expenses", "Income"
        , "Loans", "Credit Cards", "Search", "Overview","Quick Payoff Calculator", "Settings"])
with checking:
    checking_Name = st.text_input("Name of Checking Account")
    checking_Amount = st.number_input("Amount")
    fee = st.checkbox("Checking Account Fee")
    calculate_interest = st.checkbox("Calculate Checking Account Interest Return")
    if st.button("Save Checking Account"):
        another_checking = st.button("Add another checking account", type="primary")
    if fee:
        fee_period = st.selectbox("Checking Fee Period", ("Monthly", "Yearly"))
        checking_Fee = st.number_input("Checking Fee Amount")
    if calculate_interest:
        interest_rate_apy = st.number_input("Enter Interest Rate(APY%)")
        compounding_type = st.selectbox("Compounding Type", ("Daily", "Monthly", "Quarterly", "Annual", "Don't Know"))
        if compounding_type == "Don't Know":
            compounding_type = helpperFunctions.account_type()
        calculate = st.button("Calculate")
        if calculate:
            helpperFunctions.apy_calculator(checking_Amount, interest_rate_apy, compounding_type, "Checking")


with saving:
    saving_Name = st.text_input("Name of Saving Account")
    saving_Amount = st.number_input("Saving Amount")
    saving_fee = st.checkbox("Saving Account Fee")
    saving_calculate_interest = st.checkbox("Calculate Saving Account Interest Return")
    if saving_fee:
        saving_fee_period = st.selectbox("Saving Fee Period", ("Monthly", "Yearly"))
        checking_Fee = st.number_input("Saving Fee Amount")
    if saving_calculate_interest:
        interest_rate_apy = st.number_input("Enter Interest Rate(APY%)")
        compounding_type = st.selectbox("Compounding Type", ("Daily", "Monthly", "Quarterly", "Annual", "Don't Know"))
        if compounding_type == "Don't Know":
            compounding_type = helpperFunctions.account_type()
        calculate = st.button("Calculate")
        if calculate:
            helpperFunctions.apy_calculator(checking_Amount, interest_rate_apy, compounding_type, "Savings")
with expenses:
    expense_Name = st.text_input("Expense Name")
    expense_amount = st.number_input("Expense Amount")
    expense_date = st.date_input("Expense Occurred", max_value=datetime.date.today())
    expense_repeat = st.checkbox(" Expense Reoccurring")
    if expense_repeat:
        expense_period = st.selectbox("Time period", ("Daily", "Weekly", "Biweekly", "Monthly", "Biweekly", "Yearly"))
    if st.button("Submit Expense"):
        another_expense = st.button("Add another expense", type="Primary")
with income:
    income_Name = st.text_input("Income Name")
    income_amount = st.number_input("Income Amount")
    income_date = st.date_input("Income Occurred", max_value=datetime.date.today())
    income_repeat = st.checkbox(" Income Reoccurring")
    if income_repeat:
        income_period = st.selectbox("Time period", ("Daily", "Weekly", "Biweekly", "Monthly", "Biweekly", "Yearly"))
    if st.button("Submit Income"):
        another_income = st.button("Add another income")
with loans:
    loan_Name = st.text_input("Name of Loan")
    initial_loan_amount = st.number_input("Initial loan amount", min_value=0)
    loan_Amount_left = st.number_input("Amount left on loan", min_value=0)
    loan_Amount_monthly_payment = st.number_input("Monthly payment", min_value=0)
    loan_interest = st.number_input("Interest Rate (APR%)",min_value=0)
    loan_start_date = st.date_input("Enter Loan Start Date")
    loan_end_date = st.date_input("Enter Loan End Date")
    if st.button("Submit"):
        another_loan = st.button("Add another Loan")
with credit:
    credit_Name = st.text_input("Name of Card")
    credit_Amount = st.number_input("Statement Amount")
    credit_interest = st.number_input(" Credit Card Interest Rate")
    if st.checkbox("Has Annual Fee"):
        credit_fee = st.number_input("Enter Annual Fee", min_value=0.00)
    if st.button("Submit Credit Card"):
        another_card = st.button("Add another Credit Card")
with quick_payoff:
    loan_Amount = st.number_input("Amount of loan")
    interest = st.number_input("Interest rate (APR%)")
    pay_by = st.number_input("Payoff in how many months", min_value= 0)
    if st.button("Calculate Payment"):
        helpperFunctions.quick_payoff(pay_by,interest,loan_Amount)

with search:
    st.write("WIP")
    # need to understand database
with overview:
    st.write("WIP")
    # need to understand database
with settings:
    if st.button("Log Out"):
        st.switch_page("Homepage.py")
